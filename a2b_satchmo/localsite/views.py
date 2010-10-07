from django.shortcuts import render_to_response
from django.template import RequestContext

def example(request):
    ctx = RequestContext(request, {})
    return render_to_response('localsite/example.html', context_instance=ctx)

def shop_terms(request):
    ctx = RequestContext(request, {})
    return render_to_response('localsite/shop-terms.html',
        context_instance=ctx)
