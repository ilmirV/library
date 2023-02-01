from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path, reverse_lazy
from django.views.generic.base import RedirectView

from rest_framework.routers import DefaultRouter

from books import views

router = DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'authors', views.AuthorViewSet)
router.register(r'genres', views.GenreViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'reviews', views.ReviewViewSet)
router.register(r'book_relation', views.UserBookRelationView)
router.register(r'mybooks', views.LoanedBooksByUserListView, basename='my-borrowed')
router.register(r'allborrowed', views.AllBorrowedBooks, basename='all-borrowed')
router.register(r'bookcopy', views.BookInstanceViewSet, basename='book-copy')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('account/login/', views.LogInView.as_view()),
    path('account/register/', views.SignUpView.as_view()),
    path('accounts/logout/', views.LogoutView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += [
#     path('accounts/', include('django.contrib.auth.urls')),
# ]
