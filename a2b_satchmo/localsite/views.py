from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from satchmo_store.contact.models import Contact
from satchmo_store.shop.models import Order, OrderItem
from satchmo_utils.views import bad_or_missing
from livesettings import config_value
from a2b_satchmo.localsite.forms import PostPaidForm
import operator

def order_tracking(request, order_id):
    form = PostPaidForm()            
    order = None
    try:
        contact = Contact.objects.from_request(request, create=False)
        try:
            order = Order.objects.get(id__exact=order_id, contact=contact)
            orderitem = OrderItem.objects.get(order__exact=order_id)
            if request.method == 'POST':                
                order.total =  order.total + 1
                orderitem.quantity = orderitem.quantity + 1
                order.save()
                orderitem.save()
        except Order.DoesNotExist:
            pass
    except Contact.DoesNotExist:
        contact = None

    if order is None:
        return bad_or_missing(request, _("The order you have requested doesn't exist, or you don't have access to it."))

    ctx = RequestContext(request, {
        'default_view_tax': config_value('TAX', 'DEFAULT_VIEW_TAX'),
        'contact' : contact,
        'order' : order,
        'form':form,
        })

    return render_to_response('shop/order_tracking.html', context_instance=ctx)

order_tracking = login_required(order_tracking)