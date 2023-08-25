from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

from users.forms import LoginForm, SignUpForm, CounselorSignUpForm, ChangeForm, patient_form_set, patient_new_form_set
from users.models import Patient, Counselor
from users.permissions import counselor_group, patient_group


def save_user_to_group(user, group):
    user.groups.add(group)


# Create your views here.
def login_patient_view(request):
    return login_view(request, patient_group)


def login_counselor_view(request):
    return login_view(request, counselor_group)


def login_view(request, group):
    if request.user.is_authenticated:
        return redirect('My-Page')
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            group, _ = Group.objects.get_or_create(name=group.name)
            if group in user.groups.all():
                login(request, user)
                # return redirect('board:articles')
                return redirect('My-Page')
            else:
                form.add_error(None, '입력하신 사용자는 존재하지 않습니다')
        context = {
            "form": form,
        }
    else:
        form = LoginForm()
        context = {
            "form": form,
        }
    template_name = f"users/{'Counselor' if group == counselor_group else 'Patient'}-Login.html"
    return render(request, template_name, context)


def signup_patient(request):
    if request.method == "POST":
        form = SignUpForm(data=request.POST, files=request.FILES)
        formset = patient_form_set(
            request.POST,
            prefix='patientForm'
        )
        if form.is_valid() and formset.is_valid():
            saved_user = form.save()
            save_user_to_group(saved_user, patient_group)
            saved_formset = formset.save(commit=False)
            for saved_patient in saved_formset:
                saved_patient.p_user = saved_user
                saved_patient.save()
            return redirect('users:login-patient')
        else:
            form.add_error(None, '입력하신 정보는 올바르지 않습니다')
    else:
        form = SignUpForm()
        formset = patient_new_form_set(
            queryset=Patient.objects.none(),
            prefix='patientForm'
        )
    empty_form = formset.empty_form
    empty_form.prefix = 'patientForm-__prefix__'
    context = {
        "form": form,
        "formset": formset,
        "empty_form": empty_form
    }
    return render(request, "users/Patient-signup.html", context)


def signup_counselor(request):
    if request.method == "POST":
        form = SignUpForm(data=request.POST, files=request.FILES)
        form_counselor = CounselorSignUpForm(data=request.POST, files=request.FILES)
        if form.is_valid() and form_counselor.is_valid():
            saved_user = form.save()
            save_user_to_group(saved_user, counselor_group)
            saved_counselor = form_counselor.save(commit=False)
            saved_counselor.c_user = saved_user
            saved_counselor.save()
            return redirect('users:login-counselor')
        else:
            form.add_error(None, '입력하신 정보는 올바르지 않습니다')
    else:
        form = SignUpForm()
        form_counselor = CounselorSignUpForm()
    context = {
        "form": form,
        "form_counselor": form_counselor,
    }
    return render(request, "users/Counselor-signup.html", context)


@login_required(login_url='users:choose_your_type')
def logout_view(request):
    logout(request)
    return redirect('My-Page')


def change(request):
    if request.method == "POST":
        form = ChangeForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('My-Page')
        else:
            form.add_error(None, '입력하신 정보는 올바르지 않습니다')
    else:
        form = ChangeForm(instance=request.user)
        patients = Patient.objects.filter(p_user=request.user)
        formset = patient_form_set(queryset=patients, prefix='patientForm') if patients.exists() else None
        counselor = request.user.counselor_set.first()
        form_counselor = CounselorSignUpForm(instance=counselor) if counselor else None
    context = {
        "form": form,
        "formset": formset,
        "form_counselor": form_counselor,
    }
    return render(request, "users/User-Change.html", context)
