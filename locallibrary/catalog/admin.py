from django.contrib import admin
from .models import Author, Genre, Book, BookInstance

# Register your models here.

admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(Author)
# admin.site.register(BookInstance)

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):

    list_display = ('book', 'status','borrower','due_back','id')
    list_filter = ('status','due_back')


    fieldsets = (
        (None, {
            'fields':('book','imprint','id')
        }),
        ('Avilability', {
            'fields':('status','due_back','borrower')
        }),
    )