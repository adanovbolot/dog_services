from django.shortcuts import render
from django.views import View
from .models import ContentEmployee


def index(request):
    return render(request, 'index.html')


class ContentEmployeeView(View):
    def get(self, request, *args, **kwargs):
        contentemployee = ContentEmployee.objects.all()
        return render(request, 'utils/employee.html', context={
            'contentemployee': contentemployee
        })
