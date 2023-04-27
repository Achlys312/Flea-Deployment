from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout 
from item.models import Category, Item
from django.http import HttpResponse
from .forms import SignupForm

from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    'request_count', 'Total request count', ['method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'request_latency_seconds', 'Request latency', ['method', 'endpoint', 'http_status']
)


@REQUEST_LATENCY.time()
def my_view(request):
    # Your view code here

    # Increment the request count and record the request duration
    REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
    return response

def metrics(request):
    from prometheus_client import generate_latest

    # Expose the Prometheus metrics
    return HttpResponse(generate_latest(), content_type='text/plain; version=0.0.4')



def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })

@login_required
def logout_user(request):
    logout(request)
    return redirect('dashboard:index')