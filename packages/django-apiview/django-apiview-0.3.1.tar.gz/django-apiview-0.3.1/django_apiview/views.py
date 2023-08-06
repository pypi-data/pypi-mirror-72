import time
import logging
import functools

import bizerror
from fastutils.funcutils import get_inject_params
from fastutils.typingutils import Number
from fastutils.typingutils import smart_cast
from django.http import JsonResponse

from .utils import SimpleJsonEncoder
from .utils import get_request_data
from .pack import SimpleJsonResultPacker

logger = logging.getLogger(__name__)

simple_json_result_packer = SimpleJsonResultPacker()

class View(object):
    """Process class of apiview.
    """
    def __init__(self, request, **kwargs):
        self.request = request
        self.kwargs = kwargs
        self.data = get_request_data(self.request, self.kwargs)
        self.data["_django_apiview_view_instance"] = self

    def process(self, func):
        try:
            return func(_django_apiview_view_instance=self)
        except TypeError as error:
            if not str(error).endswith("got an unexpected keyword argument '_django_apiview_view_instance'"):
                raise error
            else:
                params = get_inject_params(func, self.data)
                return func(**params)

def apiview(func):
    """Turn the view function into apiview function. Must use as the first decorator.
    """
    def wrapper(request, **kwargs):
        view = View(request,**kwargs)
        package = {}
        try:
            result = view.process(func)
            package = simple_json_result_packer.pack_result(result)
        except Exception as error:
            logger.exception("apiview process failed: {}".format(str(error)))
            package = simple_json_result_packer.pack_error(error)
        return JsonResponse(package, encoder=SimpleJsonEncoder, json_dumps_params={"ensure_ascii": False, "allow_nan": True, "sort_keys": True})
    wrapper.csrf_exempt = True
    return functools.wraps(func)(wrapper)

def requires(*parameter_names):
    """Throw bizerror.MissingParameter exception if required parameters not given.
    """
    def wrapper_outer(func):
        def wrapper(_django_apiview_view_instance):
            view = _django_apiview_view_instance
            missing_names = []
            for name in parameter_names:
                if not name in view.data:
                    missing_names.append(name)
            if missing_names:
                raise bizerror.MissingParameter(missing_names)
            return view.process(func)
        return functools.wraps(func)(wrapper)
    return wrapper_outer

def choices(field, choices, annotation=None, allow_none=False):
    """Make sure field's value in choices.
    """
    def wrapper_outer(func):
        def wrapper(_django_apiview_view_instance):
            view = _django_apiview_view_instance
            if callable(choices):
                params = get_inject_params(choices, view.data)
                values = choices(**params)
            else:
                values = choices
            value = view.data.get(field, None)
            if annotation:
                value = smart_cast(annotation, value)
            if (allow_none and value is None) or (value in choices):
                return view.process(func)
            else:
                raise bizerror.BadParameter("field {0}'s value '{1}' is not in choices {2}.".format(field, value, values))
        return functools.wraps(func)(wrapper)
    return wrapper_outer

def between(field, min, max, include_min=True, include_max=True, annotation=Number, allow_none=False):
    """Make sure field's numeric value is in range of [min, max].
    """
    def wrapper_outer(func):
        def wrapper(_django_apiview_view_instance):
            view = _django_apiview_view_instance
            if callable(min):
                params = get_inject_params(min, view.data)
                min_value = min(**params)
            else:
                min_value = min
            if callable(max):
                params = get_inject_params(max, view.data)
                max_value = max(**params)
            else:
                max_value = max
            value = view.data.get(field, None)
            value = smart_cast(Number, value)
            if (allow_none and value is None) or ((include_min and min_value <= value or min_value < value) and (include_max and max_value >= value or max_value > value)):
                return view.process(func)
            else:
                raise bizerror.BadParameter("field {0}'s value '{1}' is not in range of {2}{3}, {4}{5}.".format(
                    field, value,
                    include_min and "[" or "(", 
                    min_value, max_value,
                    include_max and "]" or ")",
                    ))
        return functools.wraps(func)(wrapper)
    return wrapper_outer
