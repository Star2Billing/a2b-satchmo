# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from satchmo_store.contact.models import Contact
from django.utils.translation import ugettext_lazy as _

from payment.forms import SimplePayShipForm
from payment.listeners import form_terms_listener

from signals_ahoy.signals import form_postsave, form_init

from satchmo_store.contact.forms import ContactInfoForm
from satchmo_store.accounts.forms import RegistrationForm
from django import forms
from django.forms import ModelForm
from satchmo_store.accounts.signals import  *
from a2b_satchmo.localsite.listeners import *
import datetime


# Extension to the models of the contact form

class LocalContact(models.Model):
    """Contact model extension to store extra Messer info."""
    contact = models.OneToOneField(Contact, verbose_name=_('Base Contact'))
    age = models.CharField(verbose_name=_('Age') , max_length=30)
    
    def  __unicode__(self):
        return self.age


class LocalContactAdmin(admin.ModelAdmin) :
    list_display = ('contact','age',)

form_postsave.connect(messer_contact_form_postsave, sender=ContactInfoForm)
form_init.connect(messer_contact_add_form_fields, sender=None)

admin.site.register(LocalContact,LocalContactAdmin)

form_init.connect(form_terms_listener, sender=SimplePayShipForm)

form_init.connect(form_age_listener, sender=RegistrationForm)