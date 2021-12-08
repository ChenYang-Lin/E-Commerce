from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('history/', views.history, name='history'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.editProfile, name='edit-profile'),
    path('add-product/', views.addProduct, name='add-product'),
]