from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from satchmo_store.contact.models import Contact
from django.contrib.sites.models import Site
from satchmo_store.shop.models import Order, OrderItem, Config
from satchmo_utils.views import bad_or_missing
from livesettings import config_value
from a2b_satchmo.localsite.forms import PostPaidForm
import operator

##To run python script
#import subprocess
#from a2b_satchmo.settings import DIRNAME

def make_call(request):
    form = PostPaidForm()    
    order = None    
    try:
        user_data = Contact.objects.get(user=request.user.id)
        contact = Contact.objects.from_request(request, create=False)
        try:
            orders = Order.objects.filter(contact=contact).order_by('-time_stamp')
            order_id=73
            order = Order.objects.get(id__exact=order_id, contact=contact)
            orderitem = OrderItem.objects.get(order__exact=order_id)
            if request.method == 'POST':
                order.total =  order.total + 1
                order.sub_total =  order.sub_total + 1

                orderitem.quantity = orderitem.quantity + 1
                orderitem.line_item_price = orderitem.line_item_price + 1

                order.save()
                orderitem.save()

                ## Run Python script
                #subprocess.call(["python", DIRNAME + "server_version.py"])#, "arg1", "arg2"
        except Order.DoesNotExist:
            pass
    except Contact.DoesNotExist:
        contact = None
        user_data = None
    
    #if order is None:
    #    return bad_or_missing(request, _("The order you have requested doesn't exist, or you don't have access to it."))

    ctx = RequestContext(request, {        
        'form':form,
        'user_data': user_data,
        'orders' : orders,
        })

    return render_to_response('shop/make_call.html', context_instance=ctx)

make_call = login_required(make_call)


def invoice(request, order_id):
    order = None
    try:
        contact = Contact.objects.from_request(request, create=False)
        try:
            order = Order.objects.get(id__exact=order_id, contact=contact)
            orderitem = OrderItem.objects.get(order__exact=order_id)            
            shopDetails = Config.objects.get_current()            
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
        'shopDetails':shopDetails,
        })

    return render_to_response('shop/invoice.html', context_instance=ctx)

invoice = login_required(invoice)