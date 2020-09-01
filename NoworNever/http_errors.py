from django.shortcuts import render,redirect
from django.core.exceptions import PermissionDenied


def error_404(request,exception):
  return render(request,"templates/HTTP/base_error.html")
