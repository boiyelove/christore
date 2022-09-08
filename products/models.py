from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.
class Catalog(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=150)
	description = models.TextField(null=True, blank = True)
	pub_date = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.name

class CatalogCategory(models.Model):
	catalog = models.ForeignKey('Catalog',
	                         related_name='categories')
	parent = models.ForeignKey('self', blank=True, null=True,
	                         related_name='children')
	name = models.CharField(max_length=300)
	slug = models.SlugField(max_length=150)
	description = models.TextField(blank=True)
	featured = models.BooleanField(default = None)
	timestamp = models.DateTimeField(auto_now_add=False, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	active = models.BooleanField(default=True)

	def __str__(self):
		if self.parent:
		    return '%s: %s - %s' % (self.catalog, self.parent, self.name)
		return '%s: %s' % (self.catalog, self.name)


class Product(models.Model):
	title = models.CharField(max_length=60)
	category = models.ForeignKey('CatalogCategory')
	slug = models.SlugField(unique=True)
	description = models.TextField(null=True, blank = True)
	direction = models.TextField(null=True, blank = True)
	warning = models.TextField(null=True, blank = True)
	ingredient = models.TextField(null=True, blank = True)
	review = models.TextField(null=True, blank = True)
	price = models.DecimalField(max_digits=10, decimal_places=2, default=99.99)
	sale_price = models.DecimalField(decimal_places=2, max_digits=10, null = True, blank = True)
	timestamp = models.DateTimeField(auto_now_add=False, auto_now=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	active = models.BooleanField(default = True)
	update_defaults = models.BooleanField(default = False)

	def __str__(self):
		return self.title

	class Meta:
		unique_together=('title', 'slug')

	def get_price(self):
		return self.price

	def get_absolute_url(self):
		return reverse("single", kwargs={"slug": self.slug})

class ProductImage(models.Model):
	product = models.ForeignKey('Product')
	image = models.ImageField(upload_to='img/products')
	featured = models.BooleanField(default=False)
	thumbnail = models.BooleanField(default=False)
	active = models.BooleanField(default=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __str__(self):
		return self.product.title

# def product_defaults(sender, instance, created, *args, **kwargs):
# 	if instance.update_defaults:
# 		categories = instance.category.all()
# 		print (categories)
# 		for cat in categories:
# 			print (cat.id)
# 			if cat.id == !


class VariationManager(models.Manager):
	def all(self):
		return super(VariationManager, self).filter(active=True)

	def sizes(self):
		return self.all().filter(category='size')

	def colors(self):
		return self.all().filter(category='color')


VAR_CATEGORIES = (
	('size', 'size'),
	('color', 'color'),
	('package', 'package'),
	)


class Variation(models.Model):
	product = models.ForeignKey(Product)
	category = models.CharField(max_length=120, choices=VAR_CATEGORIES, default='size')
	title = models.CharField(max_length=120)
	image = models.ForeignKey(ProductImage, null=True, blank=True)
	price = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	active = models.BooleanField(default=True)

	objects = VariationManager()

	def __str__(self):
		return self.title







