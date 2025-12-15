import shopify
from django.conf import settings

SHOP_URL = "your-store.myshopify.com"
API_VERSION = "2023-10"  # or latest version
API_KEY = "your_api_key"
PASSWORD = "your_api_password"

shop_url = f"https://{API_KEY}:{PASSWORD}@{SHOP_URL}/admin/api/{API_VERSION}"
shopify.ShopifyResource.set_site(shop_url)
