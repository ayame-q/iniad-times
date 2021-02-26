from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect

class StaffOnlyMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        print(request.path)
        if request.path.startswith("/staff/") and (not request.user.is_authenticated or not request.user.staff):
            if not request.user.is_authenticated:
                return HttpResponseRedirect("/auth/google/login?next=" + request.path)
            return HttpResponseRedirect("/")
        return response
