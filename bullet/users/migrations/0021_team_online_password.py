# Generated by Django 4.1.3 on 2022-11-20 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0020_alter_emailcampaign_team_statuses"),
    ]

    operations = [
        migrations.AddField(
            model_name="team",
            name="online_password",
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
