from django.shortcuts import render
from django.shortcuts import HttpResponse
from backend.models import MenuItem


def index(request):
    """
    Function for template file handle
    """

    title = MenuItem.objects.get(url=request.path).title
    return render(request, "template.html", {
        "url_title": title,
        "heading": title
    })


def other(request):
    """
    Function for template file handle
    """

    if MenuItem.objects.filter(url=request.path).count():
        title = MenuItem.objects.get(url=request.path).title
        return render(request, "template.html", {
            "url_title": title,
            "heading": title
        })
    return HttpResponse("Error")
