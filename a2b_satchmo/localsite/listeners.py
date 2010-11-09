# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _
from django import forms
import models

def messer_contact_form_postsave(sender, object=None, formdata=None, form=None, **kwargs):
    if object is None:
        return
    try:
        local_contact = models.LocalContact.objects.get(contact=object)
    except models.LocalContact.DoesNotExist:
        local_contact = models.LocalContact(contact=object)
    try :
        local_contact.age = formdata['age']
    except :
        local_contact.age = ""        
    local_contact.save()

def messer_contact_add_form_fields(sender, form=None, **kwargs):
    """Adds some extra fields to the contact form"""
    age = ''
    try :
        if form._contact:
            if getattr(form._contact, 'localcontact', None):
                age = form._contact.localcontact.age                
        form.fields['age'] = forms.CharField( label=_('Age'), required=False,max_length=100,  initial=vat_number)
    except :
        pass






