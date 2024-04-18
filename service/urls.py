from django.urls import path
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from service.apps import ServeceConfig
from service.views import MailingCreateView, MailingListView, ClientListView, MessageCreateView, MailingDetailView, \
    MailingUpdateView, MailingDeleteView, MessageListView, MessageDetailView, MessageUpdateView, MessageDeleteView, \
    ClientCreateView, ClientUpdateView, ClientDeleteView, HomeView, ClientDetailView

app_name = ServeceConfig.name

urlpatterns = [
    path('clients/', ClientListView.as_view(), name='clients_list'),
    path('clients/create/', ClientCreateView.as_view(), name='clients_create'),
    path('clients/edit/<int:pk>/', ClientUpdateView.as_view(), name='clients_update'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='clients_detail'),
    path('clients/delete/<int:pk>/', cache_page(30)(ClientDeleteView.as_view()), name='clients_delete'),
    path('', HomeView.as_view(), name='home'),
    path('mailing/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/create', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/<int:pk>/', cache_page(10)(MailingDetailView.as_view()), name='mailing_detail'),
    path('mailing/edit/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/delete/<int:pk>/', cache_page(30)(MailingDeleteView.as_view()), name='mailing_delete'),
    path('message/', MessageListView.as_view(), name='message_list'),
    path('message/create_message', MessageCreateView.as_view(), name='create_message'),
    path('message/<int:pk>/', cache_page(10)(MessageDetailView.as_view()), name='message_detail'),
    path('message/edit/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message/delete/<int:pk>/', cache_page(30)(MessageDeleteView.as_view()), name='message_delete'),

]
