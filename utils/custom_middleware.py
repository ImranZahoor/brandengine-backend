import logging


class Log500ErrorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code >= 500:
            logger = logging.getLogger("django.request")
            logger.error(
                "Server Error: %s %s", request.method, request.path, exc_info=True
            )
        return response
