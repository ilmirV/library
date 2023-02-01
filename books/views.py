from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin

from rest_framework import viewsets, views, permissions, status, generics, authentication
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response

from .models import Book, Author, User, BookInstance, Genre, Review, UserBookRelation
from .permissions import IsAuthorOrReadOnly
from .serializers import BookSerializer, AuthorSerializer, LoginSerializer, UserSerializer, EmptySerializer, \
    BookInstanceSerializer, GenreSerializer, ReviewSerializer, UserBookRelationSerializer


class SignUpView(generics.CreateAPIView):
    model = get_user_model()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer


class LogInView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({
            'username': user.username,
            'email:': user.email,
            'is_librarian': user.has_perm('books.can_mark_returned')
        },
            status=status.HTTP_202_ACCEPTED
        )


class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return


class LogoutView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = EmptySerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request, format=None):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    search_fields = ['first_name', 'last_name']


class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_fields = ['title']
    search_fields = ['title', 'authors__first_name', 'authors__last_name']


class LoanedBooksByUserListView(viewsets.ModelViewSet):
    """
    Generic class-based view listing books on loan to current user.
    """
    serializer_class = BookInstanceSerializer

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class AllBorrowedBooks(PermissionRequiredMixin, viewsets.ModelViewSet):
    serializer_class = BookInstanceSerializer
    permission_required = 'books.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


class BookInstanceViewSet(viewsets.ModelViewSet):
    serializer_class = BookInstanceSerializer
    queryset = BookInstance.objects.all()


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        serializer.save()


class UserBookRelationView(UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    lookup_field = 'book'
