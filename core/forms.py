# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from core.models import Profile


class FormStylingMixin:
    """A mixin to apply consistent Tailwind CSS classes to form fields."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'block w-full rounded-md border-0 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'
            })


class CustomUserCreationForm(FormStylingMixin, UserCreationForm):
    monthly_income = forms.DecimalField(max_digits=10, decimal_places=2,
                                        help_text="Your estimated monthly take-home pay.")
    hours_worked_weekly = forms.IntegerField(help_text="Average hours you work per week.")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')


class CustomAuthenticationForm(FormStylingMixin, AuthenticationForm):
    pass


class UserUpdateForm(FormStylingMixin, forms.ModelForm):
    """
    A form for users to update their personal information.
    """

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileUpdateForm(FormStylingMixin, forms.ModelForm):
    """
    A form for users to update their financial information.
    """

    class Meta:
        model = Profile
        fields = ('monthly_income', 'hours_worked_weekly')
        help_texts = {
            'monthly_income': 'Your estimated monthly take-home pay.',
            'hours_worked_weekly': 'Average hours you work per week.',
        }
