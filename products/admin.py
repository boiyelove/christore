from django.contrib import admin

# Register your models here.
from .models import Product, ProductImage, Catalog, CatalogCategory, Variation

class ProductAdmin(admin.ModelAdmin):
	date_hierarcy = 'timestamp' #updated
	search_fields = ['title', 'description']
	list_display = ['title', 'price', 'active', 'updated']
	list_editable = ['price', 'active']
	list_filter = ['price',  'active']
	readonly_fields = ['updated', 'timestamp']
	prepopulated_fields = {"slug": ("title",)}

	class Meta:
		model = Product

class CatalogAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)}

	class Meta:
		model = Catalog

class CatalogCategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)}
	class Meta:
		model = CatalogCategory

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Catalog, CatalogCategoryAdmin)
admin.site.register(Variation)
admin.site.register(CatalogCategory, CatalogCategoryAdmin)