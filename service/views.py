from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView


from blog.models import Blog
from service.models import MailingSettings, Client, Message, Log
from service.forms import MailingSetingForm, MessageForm, ClientForm, MaillinngSettingsModeratorForm


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'service/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing_count = 0
        mailing_status = MailingSettings.objects.all()
        blog = Blog.objects.all().order_by('?')[:3]
        client = Client.objects.all().count()
        mailings = MailingSettings.objects.all().count()
        for mail in mailing_status:
            if mail.status != 'Завершена':
                mailing_count += 1
        context['mailing_count'] = mailing_count
        context['mailing'] = mailings
        context['client'] = client
        context['blogs'] = blog

        return context


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'service/clients.html'


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('service:clients_list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.user = self.request.user
            new_mat.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('service:clients_list')

    def get_form_class(self):
        """Получение формы для редактирования продукта"""
        if self.request.user.is_superuser:
            return ClientForm

        elif self.request.user == self.get_object().user:
            return ClientForm

        else:
            raise PermissionDenied

class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    success_url = reverse_lazy('service:clients_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('service:clients_list')




class MailingListView(LoginRequiredMixin, ListView):
    model = MailingSettings
    template_name = 'service/mailing_list.html'


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = MailingSettings
    form_class = MailingSetingForm
    success_url = reverse_lazy('service:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save(commit=False)
            new_mat.user = self.request.user
            new_mat.save()
        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = MailingSettings
    template_name = 'service/mailing_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clients = MailingSettings.objects.get(pk=self.kwargs['pk']).clients.all()
        client_all = [{'FIO': client.FIO, 'email': client.email} for client in clients]
        log = Log.objects.filter(mailing_list=self.kwargs['pk'])
        context['logs'] = log
        context['clients'] = client_all

        return context


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingSettings
    form_class = MailingSetingForm
    success_url = reverse_lazy('service:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.user = self.request.user
            new_mat.save()
        return super().form_valid(form)

    def get_form_class(self):
        """Получение формы для редактирования продукта"""
        if self.request.user.is_superuser:
            return MailingSetingForm
        elif self.request.user.is_staff and self.request.user.has_perm('service.change_status'):
            return MaillinngSettingsModeratorForm

        elif self.request.user == self.get_object().user:
            return MailingSetingForm

        else:
            raise PermissionDenied


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingSettings
    template_name = 'service/mailing_confirm_delete.html'
    success_url = reverse_lazy('service:mailing_list')



class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('service:mailing_list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.user = self.request.user
            new_mat.save()
        return super().form_valid(form)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('service:message_list')

    def get_form_class(self):
        """Получение формы для редактирования продукта"""
        if self.request.user.is_superuser:
            return MessageForm

        elif self.request.user == self.get_object().user:
            return MessageForm

        else:
            raise PermissionDenied


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    permission_required = 'service.delete_message'


