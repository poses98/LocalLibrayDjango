from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

# Register your models here.
admin.site.register(Genre)
admin.site.register(Language)


#making inline books for author
class BooksInline(admin.TabularInline):
    model = Book
    extra = 0

#Creating advanced listing
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name','date_of_birth','date_of_death')
    fields = ['first_name','last_name',('date_of_birth','date_of_death')]
    inlines = [BooksInline]
#Register the admin class with associated model
admin.site.register(Author,AuthorAdmin)


#This will make bookinstance appear with the book information givin
#it no inlines inside the class BookAdmin
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

#Register admin class but with decorator, 
#this does the exact thing as admin.site.register(..)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('status','due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )



