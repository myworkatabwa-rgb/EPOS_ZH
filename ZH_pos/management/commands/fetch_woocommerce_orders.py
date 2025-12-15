# ZH_pos/management/commands/fetch_woocommerce_orders.py
from django.core.management.base import BaseCommand
from ZH_pos.woocommerce_api import wcapi
from ZH_pos.models import Order, Customer
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Fetch orders from WooCommerce REST API"

    def handle(self, *args, **options):
        page = 1
        logger.info("Starting WooCommerce orders sync")
        while True:
            resp = wcapi.get("orders", params={"per_page": 50, "page": page})
            if resp.status_code != 200:
                self.stdout.write(self.style.ERROR(f"WC API error {resp.status_code}: {resp.text}"))
                logger.error("WC API error %s: %s", resp.status_code, resp.text)
                break
            data = resp.json()
            if not data:
                break
            for o in data:
                # map fields as per your Order model
                customer_data = o.get("billing", {})
                cust_email = customer_data.get("email")
                customer = None
                if cust_email:
                    customer, _ = Customer.objects.get_or_create(
                        email=cust_email,
                        defaults={"name": f"{customer_data.get('first_name','')} {customer_data.get('last_name','')}".strip()}
                    )

                Order.objects.update_or_create(
                    order_id=o["id"],
                    defaults={
                        "customer": customer,
                        "status": o.get("status"),
                        "total": o.get("total"),
                        "source": "woocommerce",
                    }
                )
            page += 1
        logger.info("Finished WooCommerce orders sync")
        self.stdout.write(self.style.SUCCESS("WooCommerce orders sync finished"))
