from django.urls import path

from cakes.views import MainPageView, ContactsView, CategoryView, ProductList, \
    ProductDetail, SearchView, RulesView

urlpatterns = [
    path('', MainPageView.as_view(), name='home'),
    path('products/', CategoryView.as_view(), name='products'),
    path('rules/', RulesView.as_view(), name='rules'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('search/', SearchView.as_view(), name='search'),
    path('products/<slug:slug>/', ProductList.as_view(), name='product_list'),
    path('products/<slug:category>/<slug:product>', ProductDetail.as_view(), name='product_detail'),
]
