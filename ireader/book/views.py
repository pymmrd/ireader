# Create your views here.

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request, tmpl='index.html'):
	return render_to_response(tmpl, context_instance=RequestContext(request, {
	
	}))

def show_content(request, tmpl="book/content.html"):
	return render_to_response(tmpl, context_instance=RequestContext(request, {
	
	}))

def show_detail(request, pk, tmpl="book/detail.html"):
	return render_to_response(tmpl, context_instance=RequestContext(request, {
	}))

def show_category(request, pk, tmpl="book/category.html"):
	return render_to_response(tmpl, context_instance=RequestContext(request, {
	
	}))
