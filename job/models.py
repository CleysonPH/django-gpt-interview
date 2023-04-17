from enum import Enum

from django.db import models
from django.urls import reverse


class JobLevel(Enum):
    JUNIOR = "Júnior"
    PLENO = "Pleno"
    SENIOR = "Sênior"

    @classmethod
    def choices(cls):
        return [(key.value, key.value) for key in cls]


class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    responsibilities = models.TextField()
    level = models.CharField(max_length=10, choices=JobLevel.choices())
    skills = models.ManyToManyField("job.Skill", related_name="jobs")

    def __str__(self):
        return self.title

    def requirements_list(self):
        return self.requirements.split("\n")

    def responsibilities_list(self):
        return self.responsibilities.split("\n")

    def get_absolute_url(self):
        return reverse("job:details", kwargs={"pk": self.pk})


class Skill(models.Model):
    title = models.CharField(max_length=100, unique=True, blank=False, null=False)

    def __str__(self):
        return self.title
