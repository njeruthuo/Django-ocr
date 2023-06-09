from django import forms
from .models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title', 'file')


class DocumentEditForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title', 'document_text')
        widgets = {
            'document_text': forms.Textarea(attrs={'style': 'width: 100%; height:50%;'}),
        }
