from stripe import StripeClient
from django.conf import settings
from paymentsystem.models import Order, Item

class StripeService:
    def __init__(self):
        self.client_stripe = StripeClient(settings.STRIPE_API_KEY_SECRET, proxy=settings.PROXY)

    def create_checkout_session_order(self, order: Order):
        line_items = []

        for item in order.items.all():
            line_items.append({
                "price_data": {
                    "currency": "rub",
                    "product_data": {
                        "name": item.name,
                    },
                    "unit_amount": item.price * 100,
                },
                "quantity": 1,
                "tax_rates": [order.tax.stripe_tax_id] if order.tax else []
            })

        session_data = {
            "line_items": line_items,
            "mode": "payment",
            "success_url": settings.SUCCESS_URL,
            "cancel_url": settings.CANCEL_URL,
        }

        if order.discount:
            session_data["discounts"] = [{
                "coupon": order.discount.stripe_coupon_id
            }]

        return self.client_stripe.v1.checkout.sessions.create(session_data)
    
    def create_checkout_session_product(self, item: Item):
        session = self.client_stripe.v1.checkout.sessions.create(
        params={
        'line_items': [{
        'price_data': {
          'currency': 'rub',
          'product_data': {
            'name': item.name,
          },
          'unit_amount': item.price * 100,
        },
        'quantity': 1,
      }],
      'mode': 'payment',
      'success_url': settings.SUCCESS_URL,
      "cancel_url": settings.CANCEL_URL
    },
  )
        return session


stripe_service = StripeService()