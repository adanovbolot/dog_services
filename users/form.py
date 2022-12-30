from django import forms
from django.contrib.auth import authenticate
from django.forms.models import inlineformset_factory
from .models import (
    ProfileEmployee,
    Schedule,
    Skills,
    ProfileClient
    )


class ProfileClientForm(forms.ModelForm):

    class Meta:
        model = ProfileClient
        fields = "__all__"


class SigUpForm(forms.Form):

    email = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'id': "inputEmail",
        }),
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'id': "inputPassword",
        }),
    )
    repeat_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'id': "ReInputPassword",
        }),
    )

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['repeat_password']

        if password != confirm_password:
            raise forms.ValidationError(
                'Пароли не совпадают'
            )

    def save(self, user_role):
        user = user_role.objects.create_user(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
        )
        user.save()
        auth = authenticate(**self.cleaned_data)
        return auth


class SignInForm(forms.Form):
    email = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'id': "inputUsername",
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control mt-2",
            'id': "inputPassword",
        })
    )


class ProfileEmployeeForm(forms.ModelForm):

    class Meta:
        model = ProfileEmployee
        fields = "__all__"
        exclude = ['user']
        # fields = ('name', 'image', 'description', 'content', 'achievements')

    name = forms.CharField(
        max_length=1000,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'subject',
            'placeholder': "Ваше имя",

        })
    )

    description = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'id': 'subject',
            'placeholder': "Описание",

        })
    )
    content = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'id': 'subject',
            'placeholder': "Опишите себя"
        })
    )
    achievements = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'id': 'subject',
            'placeholder': "Ваши достижения|необязательно"
        })
    )

    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            "id": "image_field",
            "style": "height: 40px ; width : 75px ;"
        })
    )


# class SkillsForm(forms.ModelForm):
#     class Meta:
#         model = Skills
#         exclude = ()



class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        exclude = ()


SkillsFormSet = inlineformset_factory(
    ProfileEmployee, Skills, fields="__all__", extra=4)

ScheduleFormSet = inlineformset_factory(
    ProfileEmployee, Schedule, fields="__all__", extra=7)

