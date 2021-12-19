from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [
    path('list/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('item/<int:pk>/', views.order_create, name='order-create'),
    path('mybooks/reserved/', views.UserReserved.as_view(), name='user-reserved'),
    path('mybooks/on-loan/', views.UserOnLoan.as_view(), name='user-on-loan'),
    path('mybooks/returned/', views.UserReturned.as_view(), name='user-returned'),
]
