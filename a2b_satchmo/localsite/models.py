from payment.forms import SimplePayShipForm
from payment.listeners import form_terms_listener
from signals_ahoy.signals import form_init

form_init.connect(form_terms_listener, sender=SimplePayShipForm)

