from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, DetailView, UpdateView

from users.forms import UserRegisterForm, UserProfileForm, PasswordForm
from users.models import User
from django.contrib.auth.models import Group

from users.services import get_vrification
from users.token import account_activation_token


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:register_info')

    def form_valid(self, form):
        # Сохранение пользователя
        user = form.save(commit=False)
        get_vrification(self.request, user)

        return super().form_valid(form)

    def form_invalid(self, form):
        form = UserRegisterForm
        return super().form_invalid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True

        user.save()

        #group = Group.objects.get(name='Право на изменение')
        #user.groups.add(group)
        return redirect(reverse('users:register_done'))
    else:
        return redirect(reverse('users:register_error'))


class UserPasswordReset(PasswordResetConfirmView):
    form_class = PasswordForm
    success_url = reverse_lazy("users:password_reset_complete")
    template_name = "users/password_reset_confirm.html"
