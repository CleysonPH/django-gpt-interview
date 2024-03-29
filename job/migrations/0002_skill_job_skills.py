# Generated by Django 4.2 on 2023-04-13 17:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("job", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Skill",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name="job",
            name="skills",
            field=models.ManyToManyField(related_name="jobs", to="job.skill"),
        ),
    ]
