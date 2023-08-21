from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

from users.forms import LoginForm, SignUpForm, PatientFormSet, CounselorSignUpForm
from users.models import COUNSELOR_GROUP, PATIENT_GROUP, Patient


# Create your views here.
def login_patient_view(request):
    return login_view(request, PATIENT_GROUP)


def login_counselor_view(request):
    return login_view(request, COUNSELOR_GROUP)


def login_view(request, group_name):
    if request.user.is_authenticated:
        return redirect('')
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            group, _ = Group.objects.get_or_create(name=group_name)
            if group in user.groups.all():
                login(request, user)
                return redirect('board:articles')
            else:
                form.add_error(None, '입력하신 사용자는 존재하지 않습니다')
        context = {
            "form": form,
        }
        return render(request, 'users/login.html', context)
    else:
        form = LoginForm()
        context = {
            "form": form,
        }
        template_name = f"users/{'Counselor' if group_name == COUNSELOR_GROUP else 'Patient'}-Login.html"
        return render(request, template_name, context)


# Create your views here.
def signup_patient(request):
    if request.method == "POST":
        form = SignUpForm(data=request.POST, files=request.FILES)
        formset = PatientFormSet(
            request.POST,
            prefix='patientForm'
        )
        if form.is_valid() and formset.is_valid():
            saved_user = form.save()
            saved_formset = formset.save(commit=False)
            for saved_patient in saved_formset:
                saved_patient.p_user = saved_user
                saved_patient.save()
            return redirect('users:login-patient')
        else:
            form.add_error(None, '입력하신 사용자는 존재하지 않습니다')
    else:
        form = SignUpForm()
        formset = PatientFormSet(
            queryset=Patient.objects.none(),
            prefix='patientForm'
        )
    empty_form = formset.empty_form
    empty_form.prefix = '__prefix__'
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
            saved_counselor = form_counselor.save(commit=False)
            saved_counselor.c_user = saved_user
            return redirect('users:login-counselor')
        else:
            form.add_error(None, '입력하신 상담사 사용자는 존재하지 않습니다')
    else:
        form = SignUpForm()
        form_counselor = CounselorSignUpForm()
    context = {
        "form": form,
        "form_counselor": form_counselor,
    }
    return render(request, "users/Counselor-signup.html", context)
