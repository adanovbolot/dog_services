from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.template.context_processors import request
from django.views.generic import CreateView
from .form import SigUpForm, SignInForm, ProfileEmployeeForm, ScheduleFormSet, SkillsFormSet, ProfileClientForm
from django.views import View
from .models import ProfileEmployee, ProfileClient, Employee, Client, UserAccount


class ClientSigUpFormView(View):

    def get(self, request, *args, **kwargs):
        form = SigUpForm()
        return render(request, 'auth/register_cl.html', context={
            "form": form,
        })

    def post(self, request, *args, **kwargs):
        form = SigUpForm(request.POST)
        if form.is_valid():
            user = form.save(Client)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'auth/register_cl.html', context={
            "form": form,
        })


class ClientSignInView(View):

    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(request, 'auth/authorization_cl.html', context={
            "form": form,
        })

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'auth/authorization_cl.html', context={
            "form": form,
        })


class EmployeeSigUpFormView(View):

    def get(self, request, *args, **kwargs):
        form = SigUpForm()
        return render(request, 'auth/register_em.html', context={
            "form": form,
        })

    def post(self, request, *args, **kwargs):
        form = SigUpForm(request.POST)
        if form.is_valid():
            user = form.save(Employee)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'auth/register_em.html', context={
            "form": form,
        })


class SignInView(View):

    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(request, 'auth/authorization_em.html', context={
            "form": form,
        })

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'auth/authorization_em.html', context={
            "form": form,
        })


class ProfileEmployeeList(View):

    def get(self, request, *args, **kwargs):
        profileemployee = ProfileEmployee.objects.all()
        return render(request, 'utils/profilesemployee.html', context={
            'profileemployee': profileemployee,
        })


class ProfileEmployeeDetail(View):

    def get(self, request, pk, *args, **kwargs):
        profileemloyee = get_object_or_404(ProfileEmployee, pk=pk)
        skills = profileemloyee.profile_skills.only('skills')
        schedule = profileemloyee.profile_schedule.only('choice_schedule', 'time')
        return render(request, 'utils/profilesemployeedetail.html', context={
            'profileemloyee': profileemloyee,
            'skills': skills,
            'schedule': schedule
        })


class ProfileClientCreateView(CreateView):

    model = ProfileClient
    template_name = 'utils/client_profile.html'
    fields = '__all__'
    success_url = "/"



class ProfileEmployeeInlineCreate(CreateView):
    model = ProfileEmployee
    form_class = ProfileEmployeeForm
    template_name = 'utils/employee_profile.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        profile_skills = SkillsFormSet()
        return self.render_to_response(
            self.get_context_data(form=form, profile_skills=profile_skills))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        profile_skills = SkillsFormSet(self.request.POST)
        if (form.is_valid() and profile_skills.is_valid()):
            return self.form_valid(form, profile_skills)
        else:
            return self.form_invalid(form, profile_skills)

    def form_valid(self, form, profile_skills):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        self.object = form.save()
        profile_skills.instance = self.object
        profile_skills.instance.user = self.request.user
        profile_skills.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, profile_skills):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form, profile_skills=profile_skills))


# class ProfileClientList(View):

    # def get(self, request, *args, **kwargs):
    #     profileemployee = ProfileEmployee.objects.all()
    #     return render( request, 'utils/profilesemployee.html', context={
    #         'profileemployee': profileemployee,
    #     })


