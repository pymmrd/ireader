# -*- coding:utf-8 -*-

from django.contrib import admin
from book.models import Book, FeatureBook, \
	Category

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name',)

class BookAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'status')
	list_filter = ('status',)

class FeatureBookAdmin(admin.ModelAdmin):
	list_display = ('book', 'page' )
	list_filter = ('page',)

admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(FeatureBook, FeatureBookAdmin)

	
