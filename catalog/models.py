from django.db import models
from django.urls import reverse 
import uuid


# Create your models here.
class MyModelName(models.Model):
    #Fields
    my_field_name = models.CharField(max_length = 20, help_text="Enter whatever you want", verbose_name="I am the name")
    #more fields...

    #Metadata
    class Meta:
        ordering = ['-my_field_name']

    #Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName"""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
            """String for representing the MyModelName object (in Admin site etc.)."""
            return self.my_field_name

class Genre(models.Model):
    """Model representing a book genre"""
    name = models.CharField(max_length=200, help_text="Enter a book genre(e.g Science Fiction")

    def __str__(self):
        """String for representing the model object"""
        return self.name

class Book(models.Model):
    """Model representing a book"""
    title = models.CharField(max_length=200,help_text="Title of the book")

    #Foreign key used because book can only have one author but authors can have
    #many books. Is a String as author hasnt been created yet.
    author = models.ForeignKey('Author',on_delete=models.RESTRICT,null=True)

    summary = models.TextField(max_length=1000,help_text="Brief description of the book")
    isbn = models.CharField('ISBN', max_length=13,unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    #Manytomany field as book can content many genres and genre can contain many books
    #As genre has been defined we can use the object.
    genre = models.ManyToManyField(Genre,help_text='Select a genre for this book')
    language = models.ForeignKey('Language',on_delete=models.RESTRICT,null=True)

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

    def __str__(self):
        """String representing the Model object"""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book"""
        return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
    """Class representing an instance of a book (i.e a book that can be borrowed)"""
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, help_text="Unique ID for this particular book across the library")
    book = models.ForeignKey(Book,on_delete=models.RESTRICT)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True,blank=True)

    LOAN_STATUS = (
        ('m','Maintenance'),
        ('o','On loan'),
        ('a','Available'),
        ('r','Reserved')
    )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availavility',
    )
    class Meta:
        ordering = ['due_back']
    
    def __str__(self):
        """String representing the Model object"""
        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    """Model representing an author"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True,blank=True)
    date_of_death = models.DateField(null=True,blank=True)

    class Meta:
        ordering = ['last_name','first_name']
    
    def get_absolute_url(self):
        """Return the url to access an specific record author instance"""
        return reverse('author-detail', args=[str(self.id)])
    def __str__(self):
        """String representing the Model object"""
        return f'{self.last_name}, {self.first_name}'
    class Meta:
        ordering = ['last_name']

class Language(models.Model):
    """Model representing the language in which a boook is written"""
    lang = models.CharField(max_length=50,help_text="Add another language", verbose_name="New language")

    def __str__(self):
        """String representing the Model object"""
        return self.lang
