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
            context['ticker'] = form.cleaned_data['ticker'].upper()
            # DATA FETCHING BASED ON FORM INPUT GOES HERE
            # os.remove and shutil.copy to work with image
            context['open'] = 20
            context['close'] = 30
            context['high'] = 40
            context['low'] = 10
            context['pred_conf'] = 80
    else:
        form = InputForm()
        context = {}
        context['form'] = form
        context['open'] = "--"
        context['close'] = "--"
        context['high'] = "--"
        context['low'] = "--"
        context['pred_conf'] = "X"
    
    return render(request, 'index.html', context)