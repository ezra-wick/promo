from django.http import HttpResponseRedirect
from .models import Redirect

class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info.lstrip('/')
        is_root = not path

        try:
            if is_root:
                redirect_obj = Redirect.objects.get(is_root_redirect=True)
            else:
                redirect_obj = Redirect.objects.get(old_path=path)

            return HttpResponseRedirect(f'/{redirect_obj.new_path.path}')
        except Redirect.DoesNotExist:
            pass

        response = self.get_response(request)
        return response
