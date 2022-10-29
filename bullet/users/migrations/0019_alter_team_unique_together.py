# Generated by Django 4.1.2 on 2022-10-29 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("competitions", "0025_venue_is_reviewed"),
        ("education", "0006_school_search"),
        ("users", "0018_emailcampaign"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="team",
            unique_together={
                ("venue", "number"),
                ("venue", "school", "in_school_symbol"),
            },
        ),
    ]
