from django.urls import path

from cakes.views import MainPageView, ContactsView, CategoryView, ProductList, \
    ProductDetail, SearchView, RulesView, AboutView, subscription_confirmation, \
    unsubscribe

urlpatterns = [
    path('', MainPageView.as_view(), name='home'),
    path('products/', CategoryView.as_view(), name='products'),
    path('rules/', RulesView.as_view(), name='rules'),
    path('about/', AboutView.as_view(), name='about'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('search/', SearchView.as_view(), name='search'),
    path('subscribe/confirm/', subscription_confirmation, name='subscription_confirmation'),
    path('unsubscribe/', unsubscribe, name='unsubscribe'),
    path('products/<slug:slug>/', ProductList.as_view(), name='product_list'),
    path('products/<slug:category>/<slug:product>', ProductDetail.as_view(), name='product_detail'),
]
