from django.http import Http404
from django.shortcuts import get_object_or_404
from photoalbum.models import Slide

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

def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None

def get_slide_or_404(album, slide_id):
    slide_id = int(slide_id)
    if len(album.get_slide_order()) < slide_id:
        raise Http404();

    return get_object_or_404(Slide, pk=album.get_slide_order()[slide_id - 1])
