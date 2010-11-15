from django import forms
from a2b_satchmo.customer.function_def import *
from django.forms import ModelForm
from django.contrib import *
from django.contrib.admin.widgets import *
from uni_form.helpers import *
from django.utils.translation import ugettext_lazy as _
from satchmo_store.accounts.forms import RegistrationForm
#from django.shortcuts import render_to_response
#from datetime import *

class PostPaidForm(forms.Form):
    dial_no = forms.IntegerField(required=True, help_text=_("Enter Destination Phone Number"))
