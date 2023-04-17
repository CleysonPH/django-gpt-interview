from django.shortcuts import render, get_object_or_404

from job.models import Job


def list(request):
    return render(
        request,
        "job/list.html",
        {
            "page_title": "Lista de vagas",
            "jobs": Job.objects.prefetch_related("skills").all(),
        },
    )


def details(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(
        request,
        "job/details.html",
        {
            "page_title": job.title,
            "job": job,
        },
    )
