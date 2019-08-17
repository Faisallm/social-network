from  django.http import HttpResponseBadRequest

def ajax_required(f):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()  # if not ajax request raise error
        return f(request, *args, **kwargs)  # if ajax request run function
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__

    return wrap

