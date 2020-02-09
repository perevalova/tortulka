from django.contrib import admin

from cakes.models import Image, Product, Category


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 20


class ImageInline(admin.TabularInline):
    model = Image


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'added',)
    list_filter = ('added', 'title')
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 20
    inlines = [ImageInline,]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
