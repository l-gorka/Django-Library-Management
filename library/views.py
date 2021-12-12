from django.core import paginator
from django.shortcuts import render
from django.views.generic import ListView
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
            query.add(Q(description__icontains=search), Q.OR)
            book_list = Book.objects.filter(query).select_related()
        else:
            book_list = Book.objects.all()
            search = ''
        paginator = Paginator(book_list, 100)
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)
        context = {'book_list': books, 'search': search}
        return render(request, self.template_name, context)

