from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q
from library.models import Book, BookItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'book-list.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, f'You must be logged in to access the book list.')
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        page = request.GET.get('page', 1)
        search = request.GET.get('search', False)

        if search:
            query = Q(title__icontains=search)
            query.add(Q(authors__name__icontains=search), Q.OR)
            query.add(Q(genre__genre_name__icontains=search), Q.OR)
            book_list = Book.objects.filter(query).select_related().distinct()
        else:
            book_list = Book.objects.all()
            search = ''
        query_length = len(book_list)
        paginator = Paginator(book_list, 100)
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)
        context = {'book_list': books, 'search': search, 'query_length': query_length   }
        return render(request, self.template_name, context)


class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        b = BookItem.objects.filter(book_item=self.kwargs['pk'])
        context['items'] = b
        n = BookItem.objects.filter(book_item=self.kwargs['pk'])
        context['number'] = len(n)
        return context
        

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, f'You must be logged in to access the book detail.')
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class OrderView(LoginRequiredMixin, CreateView):
    pass