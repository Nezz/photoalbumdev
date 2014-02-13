from django.http import Http404
from django.shortcuts import get_object_or_404
from photoalbum.models import Slide
import md5

secret_key = "1fff5d006fb58357dfac5f24c8c6e2b7"

def rest_helper(getResponse, postResponse, request, *extraArgs):
    if request.method == 'GET':
        if getResponse is not None:
            if extraArgs is not None:
                return getResponse(request, *extraArgs)
            else:
                return getResponse(request)
        else:
            return HttpResponseNotAllowed(['GET']) # TODO: Return usable request names
    elif request.method == 'POST':
        if postResponse is not None:
            if extraArgs is not None:
                return postResponse(request, *extraArgs)
            else:
                return postResponse(request)
        else:
            return HttpResponseNotAllowed(['GET'])

def get_slide_or_404(album, slide_id):
    slide_id = int(slide_id)
    if len(album.get_slide_order()) < slide_id:
        raise Http404();

    return get_object_or_404(Slide, pk=album.get_slide_order()[slide_id - 1])

def get_payment_checksum(pid):
    checksum_str = "pid=%s&sid=%s&amount=%s&token=%s"%(pid, "vladimirorekhov", 10, secret_key)
    m = md5.new(checksum_str)
    return m.hexdigest()

def validate_payment(pid, ref, checksum):
    checksum_str = "pid=%s&ref=%s&token=%s"%(pid, ref, secret_key)
    m = md5.new(checksum_str)
    return m.hexdigest() == checksum
