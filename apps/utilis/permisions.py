from django.shortcuts import redirect, render
from django.http.response import Http404, HttpResponse
from django.contrib.auth.mixins import AccessMixin


class UserAuthenticateRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("register_login")
        elif self.request.user.role == 'admin':
            return super().dispatch(request, *args, **kwargs)
        elif self.request.user.role == 'shop':
            return super().dispatch(request, *args, **kwargs)
        raise Http404
