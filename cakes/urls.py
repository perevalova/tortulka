from django.urls import path

from cakes.views import MainPageView, ContactsView, CategoryView, ProductList, \
    ProductDetail

urlpatterns = [
    path('', MainPageView.as_view(), name='home'),
    path('products/', CategoryView.as_view(), name='products'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('<slug:slug>/', ProductList.as_view(), name='product_list'),
    path('<slug:category>/<slug:product>', ProductDetail.as_view(), name='product_detail'),
]
