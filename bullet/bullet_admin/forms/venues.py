import re

from bullet_admin.forms.utils import get_country_choices, get_language_choices
from competitions.models import Competition, Venue
from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateTimeInput, ModelForm
from users.models import User

prefix_re = re.compile("^[A-Z]+$")


class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = [
            "shortcode",
            "name",
            "address",
            "capacity",
            "category",
            "email",
            "country",
            "accepted_languages",
            "local_start",
            "registration_flow_type",
        ]
        labels = {
            "shortcode": "Barcode prefix",
            "category": "Category",
            "registration_flow_type": "Registration flow",
        }
        help_texts = {
            "local_start": "YYYY-MM-DD HH:MM:SS",
            "email": "Responses to automatic emails from this venue will be "
            "sent there.",
            "accepted_languages": "These languages can be selected when teams "
            "register.",
            "registration_flow_type": "Only change if you know what you are doing.",
        }

        widgets = {
            "accepted_languages": forms.CheckboxSelectMultiple(),
            "local_start": DateTimeInput(attrs={"type": "datetime"}),
        }

    def __init__(self, competition: Competition, user: User, **kwargs):
        super().__init__(**kwargs)

        categories = []
        for c in competition.category_set.order_by("identifier"):
            categories.append((c.id, c.identifier.title()))
        self.fields["category"].choices = categories
        self.fields["country"].choices = get_country_choices(competition, user)
        self.fields["accepted_languages"].choices = get_language_choices(
            competition.branch
        )

        if user.get_competition_role(competition).venues:
            self.fields.pop("country")

        if not user.get_branch_role(competition.branch).is_admin:
            self.fields.pop("shortcode")

    def clean_shortcode(self):
        data = self.cleaned_data["shortcode"]
        if not prefix_re.match(data):
            raise ValidationError("Barcode prefix must contain only capital letters.")
        return data
