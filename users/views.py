from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db import transaction
from django.shortcuts import render, redirect

from users.forms import LoginForm, SignUpForm, CounselorSignUpForm, ChangeForm, patient_form_set, patient_new_form_set, \
    UserPasswordChangeForm
from users.models import Patient, Counselor
from users.permissions import UserGroups


def save_user_to_group(user, group):
    user.groups.add(group)


# Create your views here.
def login_patient_view(request):
    return login_view(request, UserGroups.patient_group)


def login_counselor_view(request):
    return login_view(request, UserGroups.counselor_group)


def login_view(request, group):
    if request.user.is_authenticated:
        return redirect('users:My-Page')
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
                return redirect('users:My-Page')
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
    template_name = f"users/{'Counselor' if group == UserGroups.counselor_group else 'Patient'}-Login.html"
    return render(request, template_name, context)


def signup_patient(request):
    if request.method == "POST":
        form = SignUpForm(data=request.POST, files=request.FILES)
        formset = patient_form_set(
            request.POST,
            prefix='patientForm'
        )
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                saved_user = form.save()
                save_user_to_group(saved_user, UserGroups.patient_group)
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
            with transaction.atomic():
                saved_user = form.save()
                save_user_to_group(saved_user, UserGroups.counselor_group)
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
    return redirect('users:choose_your_type')


def _validate_forms(*forms):
    return all(form is None or form.is_valid() for form in forms)


@login_required(login_url='users:choose_your_type', redirect_field_name='users:change')
def change(request):
    if request.method == "POST":
        form = ChangeForm(data=request.POST, files=request.FILES, instance=request.user)
        patients = Patient.objects.filter(p_user=request.user)
        formset = patient_form_set(data=request.POST, files=request.FILES, queryset=patients,
                                   prefix='patientForm') if patients.exists() else None
        counselor = getattr(request.user, 'counselor', None)
        form_counselor = CounselorSignUpForm(data=request.POST, files=request.FILES,
                                             instance=counselor) if counselor else None
        if _validate_forms(form, formset, form_counselor):
            form.save()
            if formset:
                formset.save()
            if form_counselor:
                form_counselor.save()
            return redirect('users:My-Page')
        else:
            form.add_error(None, '입력하신 정보는 올바르지 않습니다')
    else:
        form = ChangeForm(instance=request.user)
        patients = Patient.objects.filter(p_user=request.user)
        formset = patient_form_set(queryset=patients, prefix='patientForm') if patients.exists() else None
        counselor = getattr(request.user, 'counselor', None)
        form_counselor = CounselorSignUpForm(instance=counselor) if counselor else None
    context = {
        "form": form,
        "formset": formset,
        "form_counselor": form_counselor,
    }
    return render(request, "users/choose_your_change.html", context)


@login_required(login_url='users:choose_your_type', redirect_field_name='users:change')
def change_information(request):
    if request.method == "POST":
        form = ChangeForm(data=request.POST, files=request.FILES, instance=request.user)
        patients = Patient.objects.filter(p_user=request.user)
        formset = patient_form_set(data=request.POST, files=request.FILES, queryset=patients,
                                   prefix='patientForm') if patients.exists() else None
        counselor = getattr(request.user, 'counselor', None)
        form_counselor = CounselorSignUpForm(data=request.POST, files=request.FILES,
                                             instance=counselor) if counselor else None
        if _validate_forms(form, formset, form_counselor):
            form.save()
            if formset:
                formset.save()
            if form_counselor:
                form_counselor.save()
            return redirect('users:My-Page')
        else:
            form.add_error(None, '입력하신 정보는 올바르지 않습니다')
    else:
        form = ChangeForm(instance=request.user)
        patients = Patient.objects.filter(p_user=request.user)
        formset = patient_form_set(queryset=patients, prefix='patientForm') if patients.exists() else None
        counselor = getattr(request.user, 'counselor', None)
        form_counselor = CounselorSignUpForm(instance=counselor) if counselor else None
    context = {
        "form": form,
        "formset": formset,
        "form_counselor": form_counselor,
    }
    return render(request, "users/information_change.html", context)


@login_required(login_url='users:choose_your_type', redirect_field_name='users:change')
def change_password(request):
    if request.method == "POST":
        form = UserPasswordChangeForm(request.user, data=request.POST, files=request.FILES)
        if _validate_forms(form):
            form.save()
            return redirect('users:My-Page')
        else:
            form.add_error(None, '입력하신 정보는 올바르지 않습니다')
    else:
        form = UserPasswordChangeForm(request.user)
    context = {
        "form": form,
    }
    return render(request, "users/password_change.html", context)


@login_required(login_url='users:login-patient', redirect_field_name='users:my_page')
def my_page(request):
    return render(request, 'users/My-Page.html')
