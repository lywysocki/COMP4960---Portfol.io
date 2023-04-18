from django.shortcuts import render
from Algorithm.arima import forecast
from Database.database import market_data
from .forms import InputForm
from datetime import date
from dateutil.relativedelta import relativedelta

# Create your views here.

def generate_page(request):
    render_page = 'index.html'
    # request has a filled form
    if request.method == 'POST':
        # "bind" the form data
        form = InputForm(request.POST)
        if form.is_valid():
            context = dict(**form.cleaned_data)
            context['form'] = form
            try:
                conf_and_rec = do_forecast(form.cleaned_data['ticker'], form.cleaned_data['hist'], form.cleaned_data['future'])
                context.update(**conf_and_rec)
            except ValueError as pred_err:
                context['pred_err'] = str(pred_err)
                render_page = 'error.html'
            except Exception as tick_err:
                # MySQL error: 1146 Table 'tablename' doesn't exist
                if str(tick_err).startswith("1146"):
                    context['tick_err'] = "Ticker does not exist in database."
                else:
                    context['tick_err'] = str(tick_err)
                render_page = 'error.html'
            finally:
                market_dict = market_data(form.cleaned_data['ticker'].upper())
                context['open'] = market_dict['Open']
                context['high'] = market_dict['High']
                context['low'] = market_dict['Low']
                context['cur_price'] = market_dict['Current Price']
                context['mkt_cap'] = market_dict['Mkt Cap']
                context['pe_rat'] = market_dict['P/E Ratio']
                context['div_yield'] = market_dict['Div Yield']
                context['52h'] = market_dict['52-wk High']
                context['52l'] = market_dict['52-wk Low']
                context['graph_img'] = 'graph.png'
    else:
        form = InputForm()
        context = {}
        context['form'] = form
        context['pred_conf'] = "X"
        context['open'] = "--"
        context['high'] = "--"
        context['low'] = "--"
        context['cur_price'] = "--"
        context['mkt_cap'] = "--"
        context['pe_rat'] = "--"
        context['div_yield'] = "--"
        context['52h'] = "--"
        context['52l'] = "--"
    return render(request, render_page, context)

def do_forecast(ticker, hist, future):
    current_day = date.today()
    hist_day = ''
    future_day = ''
    if hist == '5yH':
        hist_day = current_day - relativedelta(years=5)
    elif hist == '1yH':
        hist_day = current_day - relativedelta(years=1)
    elif hist == '6mH':
        hist_day = current_day - relativedelta(months=6)
    elif hist == '1mH':
        hist_day = current_day - relativedelta(months=1)
    else:
        #should never run
        raise Exception("Invalid historical timeframe selected!")
    if future == '1yF':
        future_day = current_day + relativedelta(years=1)
    elif future == '6mF':
        future_day = current_day + relativedelta(months=6)
    elif future == '3mF':
        future_day = current_day + relativedelta(months=3)
    elif future == '1mF':
        future_day = current_day + relativedelta(months=1)
    else:
        #should never run
        raise Exception("Invalid future timeframe selected!")
    # returns stats dictionary
    return forecast(ticker, (current_day-hist_day).days, (future_day-current_day).days)
