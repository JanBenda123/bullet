from address.models import AddressField
from django.db import models

from django.db.models import IntegerChoices
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class School(models.Model):
    class SchoolType(IntegerChoices):
        # TODO all school types
        HIGH_SCHOOL = 1, _('High school')
        ELEMENTARY_SCHOOL = 2, _('Elementary school')

    name = models.CharField(max_length=256)
    type = models.IntegerField(choices=SchoolType.choices)

    address = AddressField()
    izo = models.CharField(max_length=128, unique=True)


class Team(models.Model):
    contact_name = models.CharField(max_length=256)
    contact_email = models.EmailField()
    contact_phone = PhoneNumberField(null=True)
    secret_link = models.CharField(max_length=48, unique=True)

    school = models.ForeignKey('users.School', on_delete=models.SET_NULL, null=True)
    # TODO language enum or code
    language = models.IntegerField()

    registered_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True)
    approved_at = models.DateTimeField(null=True)

    competition_site = models.ForeignKey('competitions.CompetitionSite', on_delete=models.CASCADE)
    number = models.IntegerField(null=True)
    in_school_symbol = models.CharField(max_length=1, null=True)

    is_official = models.BooleanField(default=True)

    is_reviewed = models.BooleanField(default=False)

    class Meta:
        unique_together = [
            ('competition_site', 'number'),
            ('school', 'in_school_symbol')
        ]


class Participant(models.Model):
    team = models.ForeignKey('users.Team', on_delete=models.CASCADE, related_name='participants')

    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    graduation_year = models.IntegerField()
    birth_year = models.PositiveIntegerField()
