# -*- coding: utf-8 -*-
from appInvite.models import waitingInviteUser, InvitedUser
from django import forms


class writeInvite(forms.Form):
    name = forms.CharField(label='Имя', required=True)
    email = forms.EmailField(label='e-mail', required=True)

    def clean_email(self):
        email = self.cleaned_data['email']
        if waitingInviteUser.objects.filter(email=email):
            raise forms.ValidationError('Пользователю с таким email уже послан инвайт')
        if InvitedUser.objects.filter(email=email):
            raise forms.ValidationError('Пользователь с таким email получил инвайт')
        return email

    def clean_name(self):
        name = self.cleaned_data['name']
        if not name.strip():
            raise forms.ValidationError('имя пользователя не может быть пустым')
        return name


class changePswd(forms.Form):
    newpswd = forms.CharField(widget=forms.PasswordInput, label='Введите пароль')
    name = forms.CharField(widget=forms.HiddenInput)
    email = forms.CharField(widget=forms.HiddenInput)