# Generated by Django 4.2 on 2023-04-14 02:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("job", "0003_alter_job_level"),
    ]

    operations = [
        migrations.CreateModel(
            name="Chat",
            fields=[
                (
                    "uuid",
                    models.UUIDField(editable=False, primary_key=True, serialize=False),
                ),
                ("title", models.CharField(editable=False, max_length=100)),
                ("completed", models.BooleanField(default=False)),
                (
                    "job",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="chats",
                        to="job.job",
                    ),
                ),
            ],
        ),
    ]