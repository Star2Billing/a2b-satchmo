from a2b_satchmo.customer.models import *
from datetime import *
from random import *
import string
import calendar


def country_list():
    list = Country.objects.all()
    return ((l.countrycode, l.countryname) for l in list)

def customer_id_list():
    list = Card.objects.all().order_by('id')
    return ((l.id, l.id) for l in list)

def speed_dial_range():
    LIST = range(0,9)
    list = map(lambda x:(x,x),LIST)
    return list

def get_unique_id():
    """get unique id"""
    length=8
    chars="abcdefghijklmnopqrstuvwxyz1234567890"
    return ''.join([choice(chars) for i in range(length)])

def pass_gen():
    char_length=2
    digit_length=6
    chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digit="1234567890"
    pass_str_char = ''.join([choice(chars) for i in range(char_length)])
    pass_str_digit = ''.join([choice(digit) for i in range(digit_length)])
    return pass_str_char+pass_str_digit

def config_value(key):
    val = Config.objects.get(config_key=key)
    return val.config_value

def call_type_list():
    CALL_TYPE_LIST= ( (-1,'ALL CALLS'),(0,'STANDARD'),
                      (1,'SIP/IAX'),(2,'DIDCALL'),
                      (3,'DID_VOIP'),(4,'CALLBACK'),(5,'PREDICT'), )
    return CALL_TYPE_LIST

def dial_status_list():
    DIAL_STATUS_LIST= ((0,'ALL'),(1,'ANSWERED'),
                       (2,'NOT COMPLETED'),(3,'NO ANSWER'),
                       (4,'BUSY'),(5,'CONGESTIONED'),
                       (6,'CHANNEL UNAVAILABLE'),(7,'CANCELED'),)
    return DIAL_STATUS_LIST

def day_range():
    DAYS = range(1,32)
    days = map(lambda x:(x,x),DAYS)
    return days

def purchase_amount_list():
    purchase_amount_arr = config_value('purchase_amount').split(":")
    purchase_amount = map(lambda x:(x,x),purchase_amount_arr)
    return purchase_amount

def purchase_amount_str():
    purchase_amount_str = config_value('purchase_amount').replace(":","-")
    purchase_amount_str = purchase_amount_str + ' ' + config_value('base_currency').upper()
    return purchase_amount_str

def validate_days(year,month,day):
    total_days = calendar.monthrange(year,month)
    if day > total_days[1]:
        return total_days[1]
    else:
        return day

def month_year_range():
    tday = datetime.today()
    year_actual = tday.year
    YEARS = range(year_actual-1, year_actual+1)
    YEARS.reverse()
    m_list = []
    for n in YEARS:
        if year_actual == n:
            month_no = tday.month + 1
        else:
            month_no = 13
        months_list = range(1,month_no)
        months_list.reverse()
        for m in months_list:
            name = datetime(n, m,1).strftime("%B")
            str_year = datetime(n, m,1).strftime("%Y") 
            str_month = datetime(n, m,1).strftime("%m")
            sample_str = str_year+"-"+str_month
            sample_name_str = name + "-" + str_year
            m_list.append( (sample_str,sample_name_str) )
    return m_list


def currency_list():
    list = Currencies.objects.all()
    return ( (l.currency,l.name+"  -  ("+str(l.value)+")") for l in list)


def currency_value(currency_name):
    cur_row = Currencies.objects.get(currency=currency_name)
    return cur_row


def timezone_list():
    list = Timezone.objects.all()
    return ((l.id, l.gmtzone) for l in list)


#variable check with request
def variable_value(request,field_name):
    if request.method == 'GET':
        if field_name in request.GET:
            field_name = request.GET[field_name]
        else:
            field_name = ''

    if request.method == 'POST':
        if field_name in request.POST:
            field_name = request.POST[field_name]
        else:
            field_name = ''

    return field_name


#source_type/destination_type filed check with request
def source_desti_field_chk(base_field,base_field_type,field_name):
    kwargs = {}
    if base_field != '':
        if base_field_type == '1':
            kwargs[field_name + '__exact']      = base_field
        if base_field_type == '2':
            kwargs[field_name + '__startswith'] = base_field
        if base_field_type == '3':
            kwargs[field_name + '__contains']   = base_field
        if base_field_type == '4':
            kwargs[field_name + '__endswith']   = base_field
    return kwargs

# call record page admin side search form common para function
def call_record_common_fun(request, form_require="no"):

    phone_no = variable_value(request,'phone_no')
    phone_no_type = variable_value(request,'phone_no_type')
    
    if "fromday_chk" in request.POST:
        fromday_chk     = 'on'        
        from_day        = int(request.POST['from_day'])
        from_month_year = request.POST['from_month_year']
        from_year       = int(request.POST['from_month_year'][0:4])
        from_month      = int(request.POST['from_month_year'][5:7])
        from_day        = validate_days(from_year,from_month,from_day)
        start_date      = datetime(from_year,from_month,from_day)
    else:
        fromday_chk     = ''
        from_day        = ''
        from_month_year = ''
        from_year       = ''
        from_month      = ''
        from_day        = ''
        start_date      = ''

    if "today_chk" in request.POST:
        today_chk       = 'on'
        to_day          = int(request.POST['to_day'])
        to_month_year   = request.POST['to_month_year']
        to_year         = int(request.POST['to_month_year'][0:4])
        to_month        = int(request.POST['to_month_year'][5:7])
        to_day          = validate_days(to_year,to_month,to_day)
        end_date        = datetime(to_year,to_month,to_day)
    else:
        today_chk       = ''
        to_day          = ''
        to_month_year   = ''
        to_year         = ''
        to_month        = ''
        to_day          = ''
        end_date        = ''

    call_type = variable_value(request,'call_type')
    show = variable_value(request,'show')
    result = variable_value(request,'result')
    currency = variable_value(request,'currency')
    
    calledstation = source_desti_field_chk(phone_no,phone_no_type,'calledstation')
        
    from a2b_satchmo.customer.forms import SearchForm
    if form_require == "yes":
        form = SearchForm(initial={'fromday_chk':fromday_chk,'from_day':from_day,'from_month_year':from_month_year,'today_chk':today_chk,'to_day':to_day,'to_month_year':to_month_year,'phone_no':phone_no,'phone_no_type':phone_no_type,'call_type':call_type,'currency':currency,'show':show,'result':result})
        return form

    else:
        kwargs = {}        
        if fromday_chk == 'on' and today_chk == 'on':
            kwargs[ 'starttime__range' ] = (start_date, end_date)
        if fromday_chk == 'on' and today_chk != 'on' :
            kwargs[ 'starttime__gte' ] = start_date
        if today_chk == 'on' and fromday_chk != 'on':
            kwargs[ 'starttime__lte' ] = end_date
        
        for i in calledstation:
            kwargs[i] = calledstation[i]
        
        if call_type != '' and call_type != '-1':
            calltype_list = call_type_list()
            for i in calltype_list:
                if int(i[0]) == int(call_type) :
                    kwargs[ 'sipiax' ] = call_type

        dlist = dial_status_list()
        if show == '0' or show == '':
            kwargs[ 'terminatecauseid__in' ] = (l[0]  for l in dlist)        
        else:
            kwargs[ 'terminatecauseid' ] = show
    
        if len(kwargs) == 0 or request.method == 'GET':
            tday = datetime.today()
            kwargs[ 'starttime__gte' ] = datetime(tday.year, tday.month, tday.day)
            
        return kwargs