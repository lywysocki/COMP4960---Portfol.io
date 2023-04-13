from django.shortcuts import render
from Algorithm.arima import forecast
from .forms import InputForm
import os

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
            # try:
            # forecast function expects a date, not a number of days in the past
            # if image problems try deleting here before calling
            forecast(form.cleaned_data['ticker'], 365, 31)
            #     raise Exception("Test ticker error message")
            # except ValueError as pred_err:
            #     context['pred_err'] = str(pred_err)
            # except Exception as tick_err:
            #     context['tick_err'] = str(tick_err)
            # finally:
            #     context['open'] = "--"
            #     context['close'] = "--"
            #     context['high'] = "--"
            #     context['low'] = "--"
            #     return render(request, 'error.html', context)
            context['open'] = 20
            context['close'] = 30
            context['high'] = 40
            context['low'] = 10
            context['pred_conf'] = 80
            context['graph_img'] = 'graph.png'
        # add an else here so context is defined when ticker is invalid   
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

def error_page(request):
    form = InputForm()
    context = {}
    context['form'] = form
    context['open'] = "--"
    context['close'] = "--"
    context['high'] = "--"
    context['low'] = "--"
    context['pred_conf'] = "X"
    return render(request, 'error.html', context)
