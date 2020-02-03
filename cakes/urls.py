from django.urls import path

from cakes.views import MainPageView, ContactsView, CategoryView, CakeList, \
    CakeDetail

urlpatterns = [
    path('', MainPageView.as_view(), name='home'),
    path('products/', CategoryView.as_view(), name='product_list'),
    path('category/', CakeList.as_view(), name='category_list'),
    # path('<slug:category>/', CakeList.as_view(), name='category_list'),
    path('detail/', CakeDetail.as_view(), name='cake_detail'),
    # path('<slug:category>/<slug:slug>', CakeDetail.as_view(), name='cake_detail'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
]
