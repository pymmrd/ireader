# -*- coding:utf-8 -*-

from django.contrib import admin
from book.models import Book, FeatureBook, \
	Category, BookPart, BookItem0, \
	BookItem1, BookItem2, BookItem3, \
	BookItem4, BookItem5, BookItem6, \
	BookItem7, BookItem8, BookItem9

class BookItemAdmin(admin.ModelAdmin):
	list_display = ('book', 'name')

class BookPartAdmin(admin.ModelAdmin):
	list_display = ('book', 'name')

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
admin.site.register(BookPart, BookPartAdmin)
admin.site.register(BookItem0, BookItemAdmin)
admin.site.register(BookItem1, BookItemAdmin)
admin.site.register(BookItem2, BookItemAdmin)
admin.site.register(BookItem3, BookItemAdmin)
admin.site.register(BookItem4, BookItemAdmin)
admin.site.register(BookItem5, BookItemAdmin)
admin.site.register(BookItem6, BookItemAdmin)
admin.site.register(BookItem7, BookItemAdmin)
admin.site.register(BookItem8, BookItemAdmin)
admin.site.register(BookItem9, BookItemAdmin)
