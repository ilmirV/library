import uuid
from datetime import date

from django.contrib.auth.models import User
from django.db import models
from rest_framework.authtoken.models import Token


from django.urls import reverse


class Genre(models.Model):
    """
    Model representing a book genre.
    """
    name = models.CharField(unique=True, max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name


class Language(models.Model):
    """
    Model representing a book language.
    """
    name = models.CharField(unique=True, max_length=200, help_text='Enter a book language (e.g. English, Russian)')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name


class Author(models.Model):
    """
    Model representing an author.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    image = models.ImageField(upload_to='author_images', default='default-author-image.png')

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """
        Returns the URL to access a particular author instance.
        """
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return f'{self.last_name}, {self.first_name} {self.middle_name}'


class Book(models.Model):
    """
    Model representing a book (but not a specific copy of a book).
    """
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, help_text='Select the author(s) for this book')
    image = models.ImageField(upload_to='book_covers', default='default-book-cover.png')
    summary = models.TextField(max_length=1500, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 Character <a '
                            'href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    bbk = models.CharField('ББК', max_length=50, null=True, blank=True)
    copy_sign = models.CharField('Авторский знак', max_length=20, null=True, blank=True)
    pages = models.PositiveSmallIntegerField(null=True, blank=True)
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    language = models.ForeignKey(Language, help_text='Select a language for this book', on_delete=models.CASCADE)
    readers = models.ManyToManyField(User, through='UserBookRelation')

    class Meta:
        ordering = ['title']

    def get_absolute_url(self):
        """
        Returns the URL to access a detail record for this book.
        """
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """
        Create a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

    def display_author(self):
        """
        Create a string for the Author. This is required to display author in Admin.
        """
        return ', '.join(author.__str__() for author in self.authors.all()[:3])

    display_author.short_description = 'Author'

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title


class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for '
                          'this particular book across whole library')
    inventory = models.CharField('Инвентарный номер', unique=True, max_length=20, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        """
        Determines if the book is overdue based on due date and current date.
        """
        return bool(self.due_back and date.today() > self.due_back)

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return f'{self.id} ({self.book.title})'


class Review(models.Model):
    title = models.CharField(max_length=100)
    review_text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.title


class UserBookRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Ok'),
        (2, 'Fine'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES)

    def __str__(self):
        return f'{self.user} on book {self.book}'
