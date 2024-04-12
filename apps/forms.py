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


class MaxQueryNumberForm(forms.Form):
    max_query_number = forms.IntegerField()

    def clean(self):
        cleaned_data = super().clean()
        max_query_number = cleaned_data.get('max_query_number')

        if not max_query_number:
            raise forms.ValidationError("Поле має бути заповнене")


class RegularUsersUpdatePeriodForm(forms.Form):
    regular_users_update_period = forms.IntegerField()

    def clean(self):
        cleaned_data = super().clean()
        regular_users_update_period = cleaned_data.get('regular_users_update_period')

        if not regular_users_update_period:
            raise forms.ValidationError("Поле має бути заповнене")


class VipUsersUpdatePeriodForm(forms.Form):
    vip_users_update_period = forms.IntegerField()

    def clean(self):
        cleaned_data = super().clean()
        vip_users_update_period = cleaned_data.get('vip_users_update_period')

        if not vip_users_update_period:
            raise forms.ValidationError("Поле має бути заповнене")
