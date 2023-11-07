from django import forms
from datetime import datetime
from django.forms import DateTimeInput, DateInput
from django.views.generic.edit import FormMixin
from publications.models import Publication
# from publications.models import (MailingSettings, MessageToMailing, Client)

# //////////////////////////////////////////////////////////////////
class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class PublicationForm(forms.ModelForm, StyleFormMixin):
    class Meta:
        model = Publication
        fields = ('header', 'content', 'image', 'video')
    # def __init__(self, *args, **kwargs):
    #     """Делаем поле 'email' and 'phone' - Readonly"""
    #     super(StyleFormMixin, self).__init__(*args, **kwargs)
    #     # instance = getattr(self, 'instance', None)
    #     self.fields['body'].widget.attrs.update({'class': 'form-control'})
    #
    # def __init__(self, *args,  **kwargs):
    #     super().__init__(*args, **kwargs)
        # self.fields['date_of_create'].widget = DateInput(attrs={'type': 'datetime-local'})
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'



# //////////////////////////////////////////////////////////////////


# class ContactForm(forms.Form):
#     from_email = forms.EmailField(label='Email', required=True)
#     subject = forms.CharField(label='Тема', required=True)
#     message = forms.CharField(label='Сообщение', widget=forms.Textarea, required=True)


# class FormMixin:
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control-10'




# class MailingSettingsFormNotUser(forms.ModelForm):
#
#     def __init__(self, *args, user=None, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['mailing_start_time'].widget = DateInput(attrs={'type': 'datetime-local'})
#         self.fields['mailing_end_time'].widget = DateInput(attrs={'type': 'datetime-local'})
#         self.user = user
#         self.fields['clients'].queryset = Client.objects.filter(owner=self.user)
#         self.fields['mail'].queryset = MessageToMailing.objects.filter(owner=self.user)
#
#     class Meta:
#         model = MailingSettings
#         fields = '__all__'
#         # exclude = ('mailing_status', 'owner',)


# class MailingFilterForm(forms.Form):
#     status_choices = MailingSettings.STATUS_CHOICES
#
#     status = forms.ChoiceField(choices=[('', 'Все')] + list(status_choices),
#                                required=False,
#                                widget=forms.Select(attrs={'id': 'status'}))
