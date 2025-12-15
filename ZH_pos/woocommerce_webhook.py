# ZH_pos/webhooks.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Order, Customer, Product

@csrf_exempt
def woocommerce_webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Example: print order info
            order_id = data.get('id')
            total = data.get('total')
            status = data.get('status')
            customer_data = data.get('billing', {})

            customer, _ = Customer.objects.get_or_create(
                email=customer_data.get('email', ''),
                defaults={
                    'name': customer_data.get('first_name', '') + ' ' + customer_data.get('last_name', ''),
                    'phone': customer_data.get('phone', '')
                }
            )

            Order.objects.update_or_create(
                order_id=str(order_id),
                defaults={
                    'customer': customer,
                    'total': total,
                    'status': status,
                    'source': 'woocommerce'
                }
            )

            # Return 200 OK to WooCommerce
            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
