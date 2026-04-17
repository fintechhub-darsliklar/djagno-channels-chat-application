from django import forms
from users.models import CustomUser as User

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    # Biz o'zimiz bitta password maydoni yaratamiz
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        # Parolni shifrlab saqlash uchun set_password ishlatamiz
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user