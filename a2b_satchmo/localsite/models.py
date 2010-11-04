from payment.forms import SimplePayShipForm
from payment.listeners import form_terms_listener
from signals_ahoy.signals import form_init
from satchmo_store.shop.views import orders

form_init.connect(form_terms_listener, sender=SimplePayShipForm)
