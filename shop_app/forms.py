from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Comments, Profile, Checkout


class CommentsForm(forms.ModelForm):
    """Comment form"""

    class Meta:
        model = Comments
        fields = [
            "nickname",
            "description_comment",
            "email",
            "rating_products",
            "product",
        ]
        widgets = {
            "nickname": forms.TextInput(),
            "email": forms.EmailInput(),
            "description_comment": forms.Textarea(),
            "rating_products": forms.RadioSelect(),
        }


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "password1",
            "password2",
        )


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = ["address", "city", "country", "postcode", "product_to_buy", "profile"]
        widgets = {
            "address": forms.TextInput(),
            "city": forms.TextInput(),
            "country": forms.TextInput(),
            "postcode": forms.TextInput(),
        }
