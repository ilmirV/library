from django.contrib import admin

from .models import Author, Genre, Book, BookInstance, Review, UserBookRelation, Language


# class BooksInline(admin.TabularInline):
#     model = Book
#     extra = 0


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'date_of_birth', 'date_of_death')

    fields = ['first_name', 'last_name', 'middle_name', 'image', ('date_of_birth', 'date_of_death')]

    # inlines = [BooksInline]


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_author', 'display_genre', 'display_language')

    inlines = [BooksInstanceInline]


@admin.register(UserBookRelation)
class UserBookRelationAdmin(admin.ModelAdmin):
    pass


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )


admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Review)
