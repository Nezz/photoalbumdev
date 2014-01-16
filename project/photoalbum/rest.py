def rest_helper(getResponse, putResponse, postResponse, deleteResponse, request, extraArgs=None):
    if request.method == 'GET':
        if getResponse is not None:
            if extraArgs is not None:
                return getResponse(request, *extraArgs)
            else:
                return getResponse(request)
        else:
            return HttpResponseNotAllowed(['GET']) # TODO: Return usable request names
    elif request.method == 'PUT':
        if putResponse is not None:
            if extraArgs is not None:
                return putResponse(request, *extraArgs)
            else:
                return putResponse(request)
        else:
            return HttpResponseNotAllowed(['GET'])
    elif request.method == 'POST':
        if postResponse is not None:
            if extraArgs is not None:
                return postResponse(request, *extraArgs)
            else:
                return postResponse(request)
        else:
            return HttpResponseNotAllowed(['GET'])
    elif request.method == 'DELETE':
        if deleteResponse is not None:
            if extraArgs is not None:
                return deleteResponse(request, *extraArgs)
            else:
                return deleteResponse(request)
        else:
            return HttpResponseNotAllowed(['GET'])