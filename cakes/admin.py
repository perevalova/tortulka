from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from cakes.models import Image, Product, Category, Subscriber, NewsLetter


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 20


class ImageAdmin(admin.ModelAdmin):
    list_per_page = 20
    ordering = ('product',)


class ImageInline(admin.TabularInline):
    model = Image


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'added',)
    list_filter = ('added', 'title')
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 20
    inlines = [ImageInline,]


class NewsLetterAdmin(SummernoteModelAdmin, admin.ModelAdmin):
    list_display = ('subject',)
    list_filter = ('subject',)
    search_fields = ('subject',)
    list_per_page = 20
    summernote_fields = ('message',)


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email',)
    list_filter = ('email',)
    search_fields = ('email',)
    list_per_page = 20


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(NewsLetter, NewsLetterAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
