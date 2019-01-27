from django import forms

from .models import Contact_Form


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact_Form
        fields = ('first_name','email', 'message')
        widgets = {
            'first_name': forms.TextInput(attrs={'id': "form_name", 'name': "first_name", 'class': "form-control", 'required':
                "required", 'data-error': "Firstname is required."}),

            'email': forms.TextInput(attrs={'id': "form_email", 'name': "name", 'class': "form-control", 'required':
                "required", 'data-error': "Firstname is required."}),

            'message': forms.Textarea(
                attrs={'id': "form_message", 'name': "message", 'class': "form-control", 'required':
                    "required", 'data-error': "Firstname is required.", 'rows':'4'}),
        }
