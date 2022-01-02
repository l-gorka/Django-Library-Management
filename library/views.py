from django.contrib.messages.views import SuccessMessageMixin
from django.http import request
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models import Q
from django.views.generic.edit import DeleteView, UpdateView
from library.models import Author, Book, BookItem, Order, PickUpSite, StatusChoices
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from datetime import datetime, timedelta
from .functions import has_group
from .forms import BookForm
from django.urls import reverse_lazy


class BookListView(ListView):
    model = Book
    template_name = 'book-list.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = dict()
        search = self.request.GET.get('search')
        if search:
            query = Q(title__icontains=search)
            query.add(Q(authors__name__icontains=search), Q.OR)
            query.add(Q(genre__genre_name__icontains=search), Q.OR)
            book_list = Book.objects.filter(
                query).select_related().distinct().order_by('title')
        else:
            book_list = Book.objects.all().distinct().order_by('title')
            search = ''
        context['book_list'] = book_list
        context['search'] = search
        return context


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


class OrderDelete(LoginRequiredMixin, DeleteView):
    model = Order
    template_name = 'order-delete.html'
    success_url = reverse_lazy('library:user-books')

    def dispatch(self, request, *args, **kwargs):
        object = super().get_object(queryset=None)
        if object.user == request.user or has_group(request.user, 'moderators'):
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.warning(
                request, f'You are not allowed to delete this order.')
            return redirect('library:book-list')


class OrderUpdate(LoginRequiredMixin, UpdateView):
    model = Order
    template_name = 'order-update.html'
    success_url = reverse_lazy('library:user-books')
    fields = ['pick_up_site', ]

    def dispatch(self, request, *args, **kwargs):
        object = super().get_object(queryset=None)
        if object.user == request.user or has_group(request.user, 'moderators'):
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.warning(
                request, f'You are not allowed to modify this order.')
            return redirect('library:book-list')


class StaffRequiredMixIn(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_staff


class ManageOrders(StaffRequiredMixIn, ListView):
    template_name = 'manage-orders.html'
    paginate_by = 20

    def get_context_data(self):
        context = super().get_context_data()
        context['choices'] = StatusChoices
        context['search'] = self.request.GET.get('search')
        context['status'] = self.request.GET.get('status')
        return context

    def get_queryset(self):
        search = self.request.GET.get('search')
        status_choice = self.request.GET.get('status')
        query = Q()
        if search:
            query = Q(user__username__contains=search)
        if status_choice:
            query.add(Q(status=status_choice), Q.AND)
        qs = Order.objects.filter(query).order_by('date_created')
        return qs


class StaffOrderUpdate(StaffRequiredMixIn, UpdateView):
    template_name = 'order-update.html'
    model = Order
    success_url = reverse_lazy('library:manage-orders')
    fields = ['status']

    def form_valid(self, form):
        if form.is_valid():
            if form.cleaned_data['status'] == 3:
                obj = form.save(commit=False)
                obj.date_returned = datetime.now()
                obj.save()
                messages.success(self.request, 'Order updated.')
                return redirect('library:manage-orders')
            return super().form_valid(form)


class ManageBooks(StaffRequiredMixIn, ListView):
    template_name = 'manage-books.html'
    model = Book
    paginate_by = 20


class DeleteBook(StaffRequiredMixIn, SuccessMessageMixin, DeleteView):
    model = Book
    template_name = 'book-delete.html'
    success_url = reverse_lazy('library:manage-books')
    success_message = f"Deleted {Book.title}"


class UpdateBook(StaffRequiredMixIn, SuccessMessageMixin, UpdateView):
    model = Book
    template_name = 'book-update.html'
    form_class = BookForm
    success_url = reverse_lazy('library:manage-books')
    success_message = 'Book updated'


class CreateBook(StaffRequiredMixIn, SuccessMessageMixin, CreateView):
    model = Book
    template_name = 'book-update.html'
    form_class = BookForm
    success_url = reverse_lazy('library:manage-books')
    success_message = 'Book created'


class CreateBookItem(StaffRequiredMixIn, CreateView):
    model = BookItem
    template_name = 'add-book-item.html'
    fields = []

    def get_success_url(self) -> str:
        return reverse_lazy('library:book-detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book"] = Book.objects.get(id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        book_obj = Book.objects.get(id=self.kwargs['pk'])
        self.obj = form.save(commit=False)
        self.obj.book_item = book_obj
        self.obj.save()
        messages.success(self.request, f'Added copy of the book')
        return redirect(self.get_success_url())


class DeleteBookItem(StaffRequiredMixIn, SuccessMessageMixin, DeleteView):
    model = BookItem
    template_name = 'book-item-delete.html'
    success_message = 'Book item deleted'

    def get_success_url(self) -> str:
        return reverse_lazy('library:book-detail', kwargs={'pk': self.kwargs['book']})
