from django import forms
from datetime import datetime
from django.forms import DateTimeInput, DateInput
from django.views.generic.edit import FormMixin
from publications.models import Publication
# from publications.models import (MailingSettings, MessageToMailing, Client)

# //////////////////////////////////////////////////////////////////


class PublicationForm(forms.ModelForm):
    # def __init__(self, *args,  **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['date_of_create'].widget = DateInput(attrs={'type': 'datetime-local'})

    class Meta:
        model = Publication
        fields = ('header', 'content', 'image', 'video')
        # fields = '__all__'

        # widgets = {
        #     'date_of_create': forms.DateInput(
        #         attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}
        #     )
        # }
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

class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

#
# class MessageToMailingForm(FormMixin, forms.ModelForm):
#     class Meta:
#         model = MessageToMailing
#         fields = '__all__'
#         exclude = ('owner',)
#
#
# class MailingSettingsForm(forms.ModelForm):
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
#         exclude = ('mailing_status', 'owner',)
#
#
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


# class ClientForm(FormMixin, forms.ModelForm):
#     class Meta:
#         model = Client
#         fields = '__all__'
#         exclude = ('owner',)
#
#
# class MailingFilterForm(forms.Form):
#     status_choices = MailingSettings.STATUS_CHOICES
#
#     status = forms.ChoiceField(choices=[('', 'Все')] + list(status_choices),
#                                required=False,
#                                widget=forms.Select(attrs={'id': 'status'}))
#
#
# class MailingSettingsUpdateFormModerator(StyleFormMixin, forms.ModelForm):
#     class Meta:
#         model = MailingSettings
#         # fields = '__all__'
#         fields = ('title', 'mailing_start_time',)

