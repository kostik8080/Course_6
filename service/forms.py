from django.forms import ModelForm
from django import forms

from service.models import MailingSettings, Message, Client


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control rounded '


class ClientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class MailingSetingForm(StyleFormMixin, ModelForm):
    start_time = forms.DateTimeField(label='Дата начала рассылки',
                                     widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end_time = forms.DateTimeField(label='Дата окончания рассылки',
                                   widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = MailingSettings
        exclude = ('status',)



class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
