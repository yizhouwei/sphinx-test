from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from django.conf import settings
from importlib import import_module
from http.cookies import SimpleCookie
from revproxy.views import ProxyView
# Create your views here.

@login_required(login_url='/login')
def home(request):
	#return redirect("http://ec2-52-90-85-204.compute-1.amazonaws.com:3000")
	return render(request, 'login/home.html', {})

def login(request):
    return render(request, 'login/login.html', {})

@login_required(login_url='/login')
def logout(request):
	auth_logout(request)
	return redirect('/')



class GraphanaProxyView(ProxyView):
    upstream = "http://%s:%d" % (settings.GRAFANA_HOST, settings.GRAFANA_PORT)
    def get_proxy_request_headers(self, request):
        headers = super(GraphanaProxyView, self).get_proxy_request_headers(request)
        headers['X-WEBAUTH-USER'] = request.user.username
        return headers
