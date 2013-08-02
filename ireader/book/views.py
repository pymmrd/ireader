# Create your views here.

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request, tmpl='index.html'):
	return render_to_response(tmpl, context_instance=RequestContext(request, {}))

def book_content(request, pk):
	return render_to_response(tmpl, context_instance=RequestContext(request, {}))

def show_bookitem(request, pk):
	return render_to_response(tmpl, context_instance=RequestContext(request, {}))
