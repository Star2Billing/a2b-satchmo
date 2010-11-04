from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_str
from django.views.decorators.cache import never_cache
from satchmo_store.contact.models import Contact
from satchmo_store.shop.models import Order, OrderItem, Config
from satchmo_utils.views import bad_or_missing
from a2b_satchmo.localsite.forms import PostPaidForm
from livesettings import config_value
import os
import urllib
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

def invoice_print(request, id):
    import trml2pdf
    order = get_object_or_404(Order, pk=id)
    shopDetails = Config.objects.get_current()
    filename_prefix = shopDetails.site.domain
    filename = "%s-invoice.pdf" % filename_prefix
    template = "invoice.rml"

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    icon_uri = config_value('SHOP', 'LOGO_URI')
    t = loader.get_template(os.path.join('shop/pdf', template))
    c = Context({
                'filename' : filename,
                'iconURI' : icon_uri,
                'shopDetails' : shopDetails,
                'order' : order,
                })
    pdf = trml2pdf.parseString(smart_str(t.render(c)))
    response.write(pdf)
    return response

invoice_print = login_required(never_cache(invoice_print))