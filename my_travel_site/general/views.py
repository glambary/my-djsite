from django.shortcuts import render


# Create your views here.
def index(request):
    context = {'title': 'General',
               }

    return render(request, 'general/index.html', context=context)


