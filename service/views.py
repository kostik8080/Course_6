from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from service.models import MailingSettings, Client, Message
from service.forms import MailingSetingForm, MessageForm, ClientForm


class ClientListView(ListView):
    model = Client
    template_name = 'service/clients.html'


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('service:clients_list')


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('service:clients_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('service:clients_list')


class MailingListView(ListView):
    model = MailingSettings
    template_name = 'service/mailing_list.html'


class MailingCreateView(CreateView):
    model = MailingSettings
    form_class = MailingSetingForm
    success_url = reverse_lazy('service:mailing_list')


class MailingDetailView(DetailView):
    model = MailingSettings
    template_name = 'service/mailing_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clients = MailingSettings.objects.get(pk=self.kwargs['pk']).clients.all()
        client_all = [{'FIO': client.FIO, 'email': client.email} for client in clients]
        context['clients'] = client_all

        return context


class MailingUpdateView(UpdateView):
    model = MailingSettings
    form_class = MailingSetingForm
    success_url = reverse_lazy('service:mailing_list')


class MailingDeleteView(DeleteView):
    model = MailingSettings
    template_name = 'service/mailing_confirm_delete.html'
    success_url = reverse_lazy('service:mailing_list')


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('service:mailing_list')


class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('service:message_list')


class MessageDeleteView(DeleteView):
    model = Message

    success_url = reverse_lazy('service:message_list')
