from rest_framework.views import exception_handler
from django.http import HttpResponse


def custom_exception_handler(exc, context):

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    # print(response.data)
    print(exc)
    if response is not None:
        fields = []
        for field, value in response.data.items():
            fields.append("{} : {}".format(field, " ".join(value)))

        response.data = {}
        response.data['fields'] = fields
        response.data['exception'] = str(exc)
        response.data['status'] = response.status_code
        response.data['error_class_name'] = exc.__class__.__name__
    else:
        response = HttpResponse(
            '{"exception":"' + str(exc) + '"}',
            content_type="application/json",
            status=500)

    return response
