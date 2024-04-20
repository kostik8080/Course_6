import pytz
import datetime
from django import forms
from django.forms import ModelForm
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
        exclude = ('user',)


class MailingSetingForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = MailingSettings
        exclude = ('status', 'user')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['clients'] = forms.ModelMultipleChoiceField(queryset=Client.objects.filter(user=user), label='Клиенты',
                                                        widget=forms.CheckboxSelectMultiple)
        self.fields['mailing_list'] = forms.ModelChoiceField(queryset=Message.objects.filter(user=user),
                                                             label='Сообщение',
                                                             widget=forms.RadioSelect)

    get_tz = pytz.timezone('UTC')
    current_time = datetime.datetime.now(get_tz)
    start_time = forms.DateTimeField(
        label='Дата и время начала рассылки',
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        initial=current_time
    )

    end_time = forms.DateTimeField(label='Дата окончания рассылки',
                                   widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))



    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        if start_time > end_time:
            raise forms.ValidationError('Дата окончания рассылки должна быть больше даты начала рассылки')


class MaillinngSettingsModeratorForm(StyleFormMixin, ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

    STATUS_CHOICES = [
        ('Завершена', "Завершена"),
        ('Создана', "Создана"),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, label='Статус рассылки', )

    class Meta:
        model = MailingSettings
        fields = ('status',)
        exclude = ('user',)


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
        exclude = ('user',)
