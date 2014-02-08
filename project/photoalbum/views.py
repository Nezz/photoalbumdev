from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext

def custom_404_view(request):
    c = {}
    return render_to_response("404.html", RequestContext(request, c))

def custom_error_view(request):
    return render_to_response("500.html")