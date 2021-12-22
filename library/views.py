from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models import Q
from django.views.generic.edit import UpdateView
from library.models import Book, BookItem, Order, PickUpSite
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from datetime import datetime, timedelta


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'book-list.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(
                request, f'You must be logged in to access the book list.')
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
        context = {'book_list': books, 'search': search,
                   'query_length': query_length}
        return render(request, self.template_name, context)


class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        b = BookItem.objects.filter(book_item=self.kwargs['pk'])
        context['items'] = b
        s = PickUpSite.objects.all()
        context['sites'] = s
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(
                request, f'You must be logged in to access the book detail.')
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


def order_create(request, **kwargs):
    if not request.user.is_authenticated:
        messages.warning(request, f'You must be logged in to create an order.')
        return redirect('login')
    else:
        if request.method == 'POST':
            book_item = BookItem.objects.get(pk=request.POST.get('pk'))
            if book_item.issued_to == None:
                book_item = BookItem.objects.get(pk=request.POST.get('pk'))
                book_item.issued_to = request.user
                book_item.issue_date = datetime.date(datetime.now())
                book_item.expiry_date = book_item.issue_date + \
                    timedelta(days=10)

                p_site = PickUpSite.objects.get(id=request.POST.get('site'))
                order = Order.objects.create(
                    user=request.user,
                    item=book_item,
                    status=0,
                    pick_up_site=p_site,
                    date_created=datetime.now(),
                )
                book_item.save()
                messages.success(
                    request, f'Your request will be processed soon. Check mailbox')
                return redirect('library:book-list')
            else:
                messages.warning(
                    request, f'This book is not aviable right now.')
                return redirect('library:book-list')

def order_delete(request, **kwargs):
    if not request.user.is_authenticated:
        messages.warning(request, f'You must be logged in to create an order.')
        return redirect('login')
    else:
        print('delete')
        return redirect('library:user-books')


class UserBooks(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'user-books.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        reserved = Order.objects.filter(user=self.request.user, status=0)
        context['reserved'] = reserved

        waiting = Order.objects.filter(user=self.request.user, status=1)
        context['waiting'] = waiting

        on_loan = Order.objects.filter(user=self.request.user, status=2)
        context['on_loan'] = on_loan

        return context
    

