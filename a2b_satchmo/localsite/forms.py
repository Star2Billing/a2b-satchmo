from django import forms
from a2b_satchmo.customer.function_def import *
from django.forms import ModelForm
from django.contrib import *
from django.contrib.admin.widgets import *
from uni_form.helpers import *
from django.utils.translation import ugettext_lazy as _
#from django.shortcuts import render_to_response
#from datetime import *


class PostPaidForm(forms.Form):
    no_of_use_service = forms.IntegerField(required=True, help_text=_("How many times have you used service?"))
    