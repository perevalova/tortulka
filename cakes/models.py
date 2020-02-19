from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='categories/', blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    def save(self,  *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_list', kwargs={'slug': self.slug})


class Product(models.Model):
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ManyToManyField(Category, blank=True)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-added']

    def __str__(self):
        return self.title

    def save(self,  *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        category = self.category.all()[0].slug
        kwargs = {
            'category': category,
            'product': self.slug,
        }
        return reverse('product_detail', kwargs=kwargs)


class Image(models.Model):
    image = models.ImageField(upload_to='products/', blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        ordering = ['-image']
