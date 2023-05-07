from django.http import HttpResponse
from rest_framework import status

import ujson as json


class CommonResponse(HttpResponse):
    def __init__(self, data, status=None, message=None):
        super().__init__(content_type='application/json', status=status)
        self.data = data
        self.message = message
        self.content = self.render_content()

    def render_content(self):
        if self.message is None and 200 <= self.status_code < 300:
            self.message = 'OK'
        response = {
            'meta': {'code': self.status_code, 'message': self.message},
            'data': self.data
        }
        return json.dumps(response)


class CommonResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)

            if isinstance(response, CommonResponse):
                return response

            status_code = response.status_code
            data = response.data
            message = response.reason_phrase
            return CommonResponse(status=status_code,
                                  message=message,
                                  data=data)
        except Exception:
            data = None
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = f'Internal Server Error'
            return CommonResponse(status=status_code,
                                  message=message,
                                  data=data)
