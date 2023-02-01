from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Book, Author, Genre, BookInstance, Review, UserBookRelation


class EmptySerializer(serializers.Serializer):
    pass


class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
        * username
        * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs


UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
        )
        return user

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')


class RelatedBooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'image', 'summary', 'bookinstance_set']


class AuthorSerializer(serializers.ModelSerializer):
    book_set = RelatedBooksSerializer(read_only=True, many=True)

    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'date_of_death', 'image', 'book_set']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']


class BookInstanceSerializer(serializers.ModelSerializer):
    borrower = UserSerializer()

    class Meta:
        model = BookInstance
        fields = ['id', 'due_back', 'status', 'borrower', 'imprint']


class ReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    pub_date = serializers.DateTimeField(format="%d %B %Y, %H:%M", read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'title', 'review_text', 'author', 'pub_date', 'book']


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(read_only=True, many=True)
    genre = GenreSerializer(read_only=True, many=True)
    bookinstance_set = BookInstanceSerializer(read_only=True, many=True)
    review_set = ReviewSerializer(read_only=True, many=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'image', 'summary', 'isbn', 'genre', 'bookinstance_set', 'review_set']


class UserBookRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ['book', 'like', 'in_bookmarks', 'rate']
