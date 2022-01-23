from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [
    path('', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('mybooks/', views.UserBooks.as_view(), name='user-books'),

    path('orders/<int:pk>/delete/', views.OrderDelete.as_view(), name='order-delete'),
    path('orders/<int:pk>/update/', views.OrderUpdate.as_view(), name='order-update'),
    path('orders/<int:pk>/staff-update/', views.StaffOrderUpdate.as_view(), name='staff-update'),

    path('manage/orders/', views.ManageOrders.as_view(), name='manage-orders'),
    path('manage/books/', views.ManageBooks.as_view(), name='manage-books'),
    path('books/<int:pk>/delete/', views.DeleteBook.as_view(), name='book-delete'),
    path('books/<int:pk>/update/', views.UpdateBook.as_view(), name='book-update'),
    path('books/<int:pk>/add-item/', views.CreateBookItem.as_view(), name='add-book-item'),
    path('manage/books/add/', views.CreateBook.as_view(), name='add-book'),
        
    path('item/<int:pk>/', views.order_create, name='order-create'),
    path('item/<int:book>/delete/<int:pk>', views.DeleteBookItem.as_view(), name='delete-book-item'),

    path('authors/', views.AuthorsListView.as_view(), name='authors-list'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),

    path('genres/', views.GenresListView.as_view(), name='genres-list'),
    path('genres/<int:pk>', views.GenreDetailView.as_view(), name='genre-detail'),

]
