# ZH_pos/tasks.py
from celery import shared_task
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, name="zh_pos.run_fetch_orders_cmd")
def run_fetch_orders_cmd(self):
    """
    Run the Django management command that fetches orders from WooCommerce.
    Using call_command keeps logic inside your management command.
    """
    try:
        logger.info("Starting fetch_woocommerce_orders management command")
        # If your command is named 'fetch_woocommerce_orders' use that.
        # If your existing command is called 'process_external_command' pass appropriate args.
        call_command('fetch_woocommerce_orders')  # <- change if your command name differs
        logger.info("Finished fetch_woocommerce_orders command")
    except Exception as exc:
        logger.exception("Error running fetch_woocommerce_orders: %s", exc)
        # Re-raise if you want celery to retry based on config
        raise
