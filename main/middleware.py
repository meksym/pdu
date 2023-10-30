from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from typing import Callable
from django.shortcuts import render


class BlockMiddleware:
    def __init__(self, get_response: Callable) -> None:
        self._get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.path.startswith('/admin/'):
            return self._get_response(request)

        return render(request, 'block.html')
