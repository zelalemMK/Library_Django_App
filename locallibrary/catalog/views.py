from django.shortcuts import render, get_list_or_404
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from catalog.models import Author

import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from catalog.forms import RenewBookForm




# Create your views here.
def index(request):


    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    #available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
 
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author

def AuthorDetailView(request, pk):
    author = Author.objects.get(pk=pk)
    books_of_author = Book.objects.filter(author=author)

    context = {
        'author':author,
        'books_of_author': books_of_author
    }
    
    return render(request, 'catalog/author_detail.html', context=context)

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):

    model = BookInstance
    template_name = 'catalog/bookintance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    '''view for renewing a spicific bookinstance'''

    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':

        FORM = RenewBookForm(request.POST)

        if form.is_valid():

            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed'))
        
        else:
            proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)

        context = {
            'form': form,
            'book_instance': book_instance,
        }

        render(request, 'catilog/book_renew_librarian.html', context)

class AuthorCreate(CreateView):
            model = Author
            fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
            initial = {'date_of_death': '05/01/2018'}

class AuthorUpdate(UpdateView):
            model = Author
            fields = '__all__'

class AuthorDelete(DeleteView):
            model = Author
            success_url = reverse_lazy('authors')
            