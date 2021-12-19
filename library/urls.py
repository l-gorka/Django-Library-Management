from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [
    path('list/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('item/<int:pk>/', views.order_create, name='order-create')
]
