# -*- coding:utf-8 -*-

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
	name = models.CharField(u'标题',
							max_length=50,
							unique=True
						)
	parent = models.ForeignKey('self',
							related_name='children',
							verbose_name=u'父分类',
							null=True,
							blank=True
						)
	ancestors = models.ManyToManyField('self', 
							symmetrical=False, 
							editable=False, 
							related_name="descendants",  
							db_index=True,
							verbose_name=u'子分类'
						)   
	meta_keywords = models.CharField(u'元关键字', 
							max_length=255, 
							blank=True
						)   
	meta_description = models.CharField(u'元描述',
								max_length=255, 
								blank=True
							)   
	level = models.IntegerField(default=0)
	order = models.IntegerField(default=0)
	
	class Meta:
		db_table = 'category'
		verbose_name = u'分类'
		verbose_name_plural = u'分类'

	def path(self, seq=" > ", field="name"):
		path = [o[field] for o in self.ancestors.all().values(field)]
		path.extend([getattr(self, field),])
		return seq.join(path)

	def _flatten(self, L):
		"""
		Taken from a python newsgroup post
		"""
		if type(L) != type([]): return [L]
		if L == []: return L
		return self._flatten(L[0]) + self._flatten(L[1:])

	def _recurse_for_children(self, node, only_active=False):
		children = []
		children.append(node)
		for child in node.children.active():
			if child != self:
				children_list = self._recurse_for_children(child, only_active=only_active)
				children.append(children_list)
		return children

	def get_active_children(self, include_self=False):
		"""
		Gets a list of all of the children categories which have active Creations.
		"""
		return self.get_all_children(only_active=True, include_self=include_self)

	def get_all_children(self, only_active=False, include_self=False):
		"""
		Gets a list of all of the children categories.
		"""
		children_list = self._recurse_for_children(self, only_active=only_active)
		if include_self:
			ix = 0
		else:
			ix = 1
		flat_list = self._flatten(children_list[ix:])
		return flat_list

	def _recurse_for_parents(self, cat_obj):
		p_list = []
		if cat_obj.parent_id:
			p = cat_obj.parent
			p_list.append(p)
			if p != self:
				more = self._recurse_for_parents(p)
				p_list.extend(more)
		if cat_obj == self and p_list:
			p_list.reverse()
		return p_list

	def parents(self):
		return self._recurse_for_parents(self)

	def get_active_children_pk(self, include_self=False):
		children = self.get_active_children(include_self)
		childs = [obj.pk for obj in children]
		return childs

	@classmethod
	def top_level(self, *args, **kw):
		return self.objects.filter(is_active=True, parent__isnull=True, *args, **kw)

	def save(self, ancestors=None):
		if ancestors is None:
			ancestors = []
		if self.parent and self.id:
			assert self.parent not in self.descendants.all(), "prevent loop reference"

		if self.parent:
			self.level = self.parent.level + 1 
		else:
			self.level = 0 
		super(self.__class__, self).save()
		self.ancestors.clear()
		if self.parent:
			if not ancestors:
				ancestors = list(self.parent.ancestors.all())
				ancestors.extend([self.parent,])
			self.ancestors.add(*ancestors)
		childs_ancestors = ancestors.extend([self, ])
		for child in self.children.all():
			child.save(ancestors=childs_ancestors)

	def __unicode__(self):
		return self.path()

class Book(models.Model):
	FINISHED = 1
	UNFINISHED = 2
	BOOK_STATUS = (
		(FINISHED, u'完成'),
		(UNFINISHED, u'连载'),
	)
	category = models.ForeignKey(Category, verbose_name=u'分类')
	name = models.CharField(max_length=100)
	author = models.CharField(max_length=30)
	word_num = models.CharField(max_length=15)
	created_date = models.DateTimeField(auto_now=True)
	update_date = models.DateTimeField(auto_now=True)
	status = models.BooleanField(
									choices=BOOK_STATUS, 
									default=UNFINISHED,
									db_index=True,
								)
	weight = models.IntegerField(default=0, db_index=True)
	has_part = models.BooleanField(default=False)
	cover = models.CharField(max_length=15, blank=True)
	intro = models.TextField(blank=True)
	class Meta:
		db_table = 'book'
		verbose_name = u'书'
		verbose_name_plural = u'书'

	def __unicode__(self):
		return '%s--->%s' % (self.category.name, self.name)

class BookPart(models.Model):
	book = models.ForeignKey(Book, verbose_name=u'书籍')
	name = models.CharField(max_length=80)

	class Meta:
		db_table = 'bookpart'
		verbose_name = u'部分'
		verbose_name_plural = u'部分'
		
	
	def __unicode__(self):
		return self.name

class BookItem(models.Model):
	book = models.ForeignKey(Book, verbose_name=u'书籍')
	part = models.ForeignKey(BookPart, 
							verbose_name=u'部分', 
							blank=True, null=True)
	name = models.CharField(max_length=80)
	content = models.CharField(max_length=80)
	
	class Meta:
		abstract = True
		db_table = 'bookitem'
		verbose_name = u'章节'
		verbose_name_plural = u'章节'


class FeatureBook(models.Model):
	INDEX = 0
	MAGIC = 1
	SORD = 2
	DUSHI = 3
	LOVER = 4
	TIME_TRAVEL = 5
	GAME = 6
	MONSTER = 7
	SCIENCE = 8
	OTHER = 9
	INDEX_MAGIC = 10
	INDEX_SORD = 11
	INDEX_DUSHI = 12 
	INDEX_LOVER = 13
	INDEX_TIME_TRAVEL = 14
	INDEX_GAME = 15
	INDEX_MONSTER = 16
	INDEX_SCIENCE = 17
	INDEX_OTHER = 18
	PAGE_FEATURE = (
		(INDEX, 'index'),
		(MAGIC, 'magic'),
		(SORD, 'sord'),
		(DUSHI, 'dushi'),
		(LOVER, 'lover'),
		(TIME_TRAVEL, 'time_travel'),
		(GAME, 'game'),
		(MONSTER, 'monster'),
		(SCIENCE, 'science'),
		(OTHER, 'other'),
		(INDEX_MAGIC, 'index_magic'),
		(INDEX_SORD, 'index_sord'),
		(INDEX_DUSHI, 'index_dushi'),
		(INDEX_LOVER, 'index_lover'),
		(INDEX_TIME_TRAVEL, 'index_time_travel'),
		(INDEX_GAME, 'index_game'),
		(INDEX_MONSTER, 'index_monster'),
		(INDEX_SCIENCE, 'index_science'),
	)
	book = models.ForeignKey(Book)
	page = models.IntegerField(choices=PAGE_FEATURE)

	class Meta:
		verbose_name = u'推荐书籍'
		verbose_name_plural = u'推荐书籍'
		db_table = 'featurebook'
		
	

def create_partition_models(base, partition):
	import sys
	_current_module = sys.modules[__name__]
	for i in xrange(partition):
		name = base.__name__+str(i)
		if _current_module.__dict__.has_key(name):
			continue
		new_model  = type(name, (base,), {'__module__':__name__})
		new_model._meta.db_table = name.lower()
		_current_module.__dict__[name] = new_model
create_partition_models(BookItem, settings.BOOKITEM_PARTITION)

