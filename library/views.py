from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Q
from library.models import Book
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


class BookListView(ListView):
    model = Book
    template_name = 'book-list.html'

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


class BookDetailView(DetailView):
    model = Book
    template_name = 'detail.html'
