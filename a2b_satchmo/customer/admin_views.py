# Create your views here.
from django.http import  Http404, HttpResponseRedirect #,HttpRequest,HttpResponse,
from django.template import *
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import logout #authenticate, login ,
from django.views.decorators.csrf import csrf_protect
from a2b_satchmo.customer.forms import *
from a2b_satchmo.customer.models import *
from django.contrib.sessions import *
from datetime import *
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.signals import payment_was_successful
from uni_form.helpers import FormHelper, Submit, Reset
from grid import ExampleGrid
from a2b_satchmo.helpers import json_encode
from django.contrib.admin.views.decorators import staff_member_required
#from django.template.loader import get_template
#import sys, string, random
#import operator
#from django.db import connection


@staff_member_required
def my_admin_language_view(request):
    language_list = Language.objects.all();
    data = {
        'language_list' : language_list,
    }
    return render_to_response('admin/language_list_template.html',data,context_instance=RequestContext(request))

@staff_member_required
def my_admin_card_view(request):
    card_list = Card.objects.all();
    data = {
        'card_list' : card_list,
    }
    return render_to_response('admin/card_list_template.html',data,context_instance=RequestContext(request))

@staff_member_required
def my_admin_cdr_view(request):
    call_list = Call.objects.all();
    data = {
        'call_list' : call_list,
    }
    return render_to_response('admin/call_list_template.html',data,context_instance=RequestContext(request))