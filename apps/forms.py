from django import forms


class ContactForm(forms.Form):
    contact_info = forms.CharField(label='Контактні дані відправника', max_length=200)
    subject = forms.CharField(label='Тема повідомлення', max_length=200)
    description = forms.CharField(label='Опис', widget=forms.Textarea)

    def clean(self):
        cleaned_data = super().clean()
        contact_info = cleaned_data.get('contact_info')
        subject = cleaned_data.get('subject')
        description = cleaned_data.get('description')

        if not contact_info or not subject or not description:
            raise forms.ValidationError("Всі поля мають бути заповнені")