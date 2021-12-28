from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [
    path('list/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('item/<int:pk>/', views.order_create, name='order-create'),
    path('mybooks/', views.UserBooks.as_view(), name='user-books'),
    path('orders/<int:pk>/delete/', views.OrderDelete.as_view(), name='order-delete'),
    path('orders/<int:pk>/update/', views.OrderUpdate.as_view(), name='order-update'),
    path('manage/orders/', views.ManageOrders.as_view(), name='manage-orders'),
    path('manage/books/', views.ManageOrders.as_view(), name='manage-books'),

]
