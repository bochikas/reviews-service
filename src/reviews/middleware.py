from django.utils.timezone import now


class LastActivityMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):

        response = self._get_response(request)
        user = request.user
        if request.user.is_authenticated:
            user.last_activity = now()
            user.save()
        return response
