from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .forms import InputForm

# Create your views here.

def base_page(request):
    # request has a filled form
    if request.method == 'POST':
        # "bind" the form data
        form = InputForm(request.POST)
        if form.is_valid():
            context = dict(**form.cleaned_data)
            context['form'] = form
            # DATA FETCHING BASED ON FORM INPUT GOES HERE
            return render(request, 'index.html', context)
    else:
        form = InputForm()
    
    return render(request, 'index.html', {'form': form})