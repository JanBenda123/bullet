# Generated by Django 4.1 on 2022-08-06 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "competitions",
            "0014_remove_categorydescription_category_category_order_and_more",
        ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="categorycompetition",
            options={"ordering": ("order",)},
        ),
        migrations.AlterUniqueTogether(
            name="categorycompetition",
            unique_together=set(),
        ),
        migrations.AddField(
            model_name="categorycompetition",
            name="identifier",
            field=models.SlugField(default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="categorycompetition",
            name="order",
            field=models.IntegerField(default=0),
        ),
        migrations.AddConstraint(
            model_name="categorycompetition",
            constraint=models.UniqueConstraint(
                models.F("competition"),
                models.F("identifier"),
                name="competitions_category_competition_identifier_unique",
            ),
        ),
        migrations.RemoveField(
            model_name="categorycompetition",
            name="category",
        ),
        migrations.DeleteModel(
            name="Category",
        ),
    ]
