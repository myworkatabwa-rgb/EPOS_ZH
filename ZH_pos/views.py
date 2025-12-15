from django.shortcuts import render
from .models import Product, Order, Customer

def dashboard(request):
    orders = Order.objects.all().order_by('-created_at')[:5]
    products = Product.objects.all()[:5]
    customers = Customer.objects.all()[:5]
    return render(request, 'dashboard.html', {
        'orders': orders,
        'products': products,
        'customers': customers,
    })
