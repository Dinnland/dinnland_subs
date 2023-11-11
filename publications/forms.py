from django import forms
from publications.models import Publication


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class PublicationForm(forms.ModelForm, StyleFormMixin):
    class Meta:
        model = Publication
        fields = ('header', 'content', 'image', 'video', 'is_paid')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


