import os
from django import forms
from a2b_satchmo.customer.function_def import *
from django.forms import ModelForm
from django.contrib import *
from django.contrib.admin.widgets import *
from django.utils.translation import ugettext_lazy as _
from satchmo_store.accounts.forms import RegistrationForm
from uni_form.helpers import FormHelper, Submit, Reset
from uni_form.helpers import *
#from django.shortcuts import render_to_response
#from datetime import *

class LoginForm(forms.Form):
	username = forms.CharField(max_length=100,required=True,)
	password = forms.CharField(widget=forms.PasswordInput(),max_length=100,required=True,)
        
class CardForm(ModelForm):
    country  = forms.ChoiceField(choices=country_list())
    id_timezone = forms.ChoiceField(choices=timezone_list(),label='Timezone',required=True)
    class Meta:
        model = Card
        fields = ['lastname', 'firstname', 'address','city','state','country','zipcode','id_timezone','phone','fax']

"""
class UserCreationFormExtended(RegistrationForm):
    age = forms.CharField(label=_('Age'),max_length=30, required=True)
    def __init__(self, *args, **kwargs):
        super(UserCreationFormExtended, self).__init__(*args, **kwargs)
    class Meta:
        model = User
"""

#Default ModelForm of Config Model is override 
class ConfigForm(ModelForm):
    config_title  = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}),required=False,help_text=_("Title of the configuration variable."))
    config_key = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}),required=False,help_text=_("Key name of the configuration variable."))
    config_value = forms.CharField(help_text=_("Insert the Value."),required=True,error_messages={'required': 'Please enter Config Value'}, )
    config_description = forms.CharField(widget=forms.Textarea(attrs={'readonly':'readonly'}),required=False,)
    
    class Meta:
        model = Config
        fields = ['config_group_title', 'config_title','config_key','config_value','config_description',]
    """
    def clean_config_value(self):
        config_value = self.cleaned_data["config_value"]
        if config_value == '':
            raise forms.ValidationError('Plase enter the Config Value !!')
        return config_value
    """

class SearchForm(forms.Form):
    fromday_chk = forms.BooleanField(label=u'FROM :',required=False,)
    from_day = forms.ChoiceField(label=u'',choices=day_range(),required=False,)
    from_month_year= forms.ChoiceField(label=u'',choices=month_year_range(),required=False,)
    today_chk = forms.BooleanField(label='TO :',required=False,)
    to_day = forms.ChoiceField(label=u'',choices=day_range(),required=False,)
    to_month_year = forms.ChoiceField(label=u'',choices=month_year_range(),required=False,)
    phone_no = forms.CharField(label=u'PHONE NO :',widget=forms.TextInput(attrs={'size': 15}),required=False,)
    phone_no_type = forms.TypedChoiceField(coerce=bool,choices=((1, 'Exact'), (2, 'Begins with'), (3, 'Contains'), (4, 'Ends with')),widget=forms.RadioSelect,required=False,label=u'PHONE NO TYPE :',)
    call_type = forms.ChoiceField(label=u'CALL TYPE :',choices=call_type_list(),required=False,)
    show = forms.TypedChoiceField(label=u'SHOW :',coerce=bool,choices=dial_status_list(),required=False,)#,widget=forms.RadioSelect
    result = forms.TypedChoiceField(label=u'RESULT :',coerce=bool,choices=(('min', 'Minutes'), ('sec', 'Seconds')),widget=forms.RadioSelect,required=False,)
    currency  = forms.ChoiceField(label=u'CURRENCY :',choices=currency_list(),required=False,)

class CardListForm(forms.Form):
    card_list = forms.ChoiceField(label=u'CUSTOMER :',choices=customer_id_list(combo="yes"),required=False,)

class CardHistoryForm(SearchForm,CardListForm):
    """
    layout = Layout(
        Fieldset(
                '',
                Row(
                    Column('fromday_chk','from_day','from_month_year','today_chk','to_day','to_month_year'),                    
                ),                 
        ),        
    )

    # Attach a formHelper to your forms class.
    helper = FormHelper()

    submit = Submit('search', _('Search'))
    helper.add_input(submit)
    helper.use_csrf_protection = True
    helper.add_layout(layout)
    
    """
    def __init__(self, *args, **kwargs):
        super(CardHistoryForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['card_list','fromday_chk', 'from_day','from_month_year','today_chk','to_day','to_month_year']


class CheckoutPaymentForm(forms.Form):
    payment_method = forms.TypedChoiceField(coerce=bool,choices=(('paypal', 'PayPal'), ),widget=forms.RadioSelect)#('moneybookers', 'Moneybookers.com'), ('plugnpay', 'PlugnPay')
    purchase_amount = forms.ChoiceField(label=u'Total Amount:')#,choices=purchase_amount_list()

class CustImport(forms.Form):
    csv_file = forms.FileField(label=_('File '),required=True, error_messages={'required': 'Please upload File'},)
    
    def clean_file(self):
        filename = self.cleaned_data["csv_file"]
        file_exts = ('.csv',)        
        if not str(filename).split(".")[1].lower() in file_exts:
            raise forms.ValidationError(_(u'Document types accepted: %s' % ' '.join(file_exts)))
        else:
            return filename

class CalleridForm(ModelForm):        
    cid = forms.CharField(label=_('Caller ID'), widget=forms.TextInput(attrs={'size': 15}))
    #id_cc_card = forms.IntegerField()
    id_cc_card = forms.ChoiceField(label=_('Card ID'),choices=customer_id_list(),required=False,help_text=_("Define the card number ID to use."))
    #activated = forms.TypedChoiceField(label=_('Status'),required=False,coerce=bool,widget=forms.RadioSelect,)
    class Meta:
        model = Callerid
        fields = ['cid','activated','id_cc_card',]

class SpeeddiaForm(ModelForm):
    speeddial = forms.ChoiceField(label=_('Speed dial'),required=False,choices=speed_dial_range(),)
    name = forms.CharField(label=_('Name'),widget=forms.TextInput(attrs={'size': 15}),required=False,help_text=_("Enter the name or label that will identify this speed dial."))
    phone = forms.CharField(label=_('Phone'),widget=forms.TextInput(attrs={'size': 15}),required=False,help_text=_("Enter the phone number for the speed dial."))
    id_cc_card = forms.ChoiceField(label=_('Card ID'),choices=customer_id_list(),required=False,help_text=_("Define the card number ID to use."))
    class Meta:
        model = Speeddial
        fields = ['speeddial','name','phone','id_cc_card']