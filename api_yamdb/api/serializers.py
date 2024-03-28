from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from rest_framework.serializers import (
    CharField,
    EmailField,
    IntegerField,
    ModelSerializer,
    Serializer,
    SlugRelatedField,
    ValidationError
)

from api_yamdb.settings import (
    CHAR_FIELD_MAX_LENGTH,
    EMAIL_FIELD_MAX_LENGTH,
    NO_REPLY,
    USERNAME_FIELD_MAX_LENGTH,
)
from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title
)
from users.validators import check_username_for_me_value

User = get_user_model()


class CategorySerializer(ModelSerializer):
    """Category model serializer."""

    class Meta:
        exclude = ('id',)
        lookup_field = 'slug'
        model = Category


class CommentSerializer(ModelSerializer):
    """Comment model serializer."""

    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            'author',
            'id',
            'pub_date',
            'text',
        )


class GenreSerializer(ModelSerializer):
    """Genre model serializer."""

    class Meta:
        exclude = ('id',)
        lookup_field = 'slug'
        model = Genre


class ReviewSerializer(ModelSerializer):
    """Review model serializer."""

    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = (
            'author',
            'id',
            'pub_date',
            'score',
            'text',
        )
        model = Review

    def validate(self, data):
        request = self.context.get('request')
        if (
            request.method == 'POST'
            and Review.objects.filter(
                title=get_object_or_404(
                    Title,
                    pk=self.context.get('view').kwargs.get('title_id')
                ),
                author=request.user
            ).exists()
        ):
            raise ValidationError(
                'Вы уже оставляли отзыв на это произведение!'
            )
        return data


class TitleGetSerializer(ModelSerializer):
    """Title model serializer for safety methods."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = IntegerField(default=None)

    class Meta:
        fields = (
            'category',
            'description',
            'genre',
            'id',
            'name',
            'rating',
            'year',
        )
        model = Title


class TitleSerializer(ModelSerializer):
    """Title model serializer for non-safe methods."""

    category = SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = SlugRelatedField(
        allow_empty=False,
        allow_null=False,
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug',
    )

    class Meta:
        model = Title
        exclude = ('id',)

    def to_representation(self, title):
        """Define serializer for output."""
        return TitleGetSerializer(title).data


class UserRegistrationSerializer(Serializer):
    """User registration serializer."""

    email = EmailField(
        max_length=EMAIL_FIELD_MAX_LENGTH
    )
    username = CharField(
        max_length=USERNAME_FIELD_MAX_LENGTH,
        validators=[
            check_username_for_me_value,
            UnicodeUsernameValidator(),
        ])

    @staticmethod
    def send_code_to_email(email: str, code: str):
        send_mail(
            fail_silently=True,
            from_email=NO_REPLY,
            message=(
                f'Ваш код подтверждения для портала YaMDB:\n{code}\n'
                'Направьте POST-запрос с кодом и вашим логином'
                'по адресу auth/token/ для получения веб токена.'
            ),
            recipient_list=[email],
            subject='Код подтверждения для портала YaMDb',
        )

    def create(self, validated_data):
        """Return new User instance."""
        user, _ = User.objects.get_or_create(**validated_data)
        self.send_code_to_email(
            email=user.email,
            code=default_token_generator.make_token(user)
        )
        return user

    def validate(self, attrs):
        """Check fields request values."""
        email = attrs.get('email')
        error_message: dict = {}
        username = attrs.get('username')

        if User.objects.filter(**attrs).exists():
            return attrs

        same_email_user = User.objects.filter(email=email).first()
        same_username_user = User.objects.filter(username=username).first()

        if same_email_user != same_username_user:
            if same_email_user is not None:
                error_message.update({
                    'email': 'Пользователь с таким адресом почты существует'
                })
            if same_username_user is not None:
                error_message.update({
                    'username': 'Пользователь с таким именем существует'
                })
            raise ValidationError(error_message)
        return attrs


class UserGettingTokenSerializer(Serializer):
    """Create and return token to user."""

    confirmation_code = CharField(
        max_length=CHAR_FIELD_MAX_LENGTH
    )
    username = CharField(
        max_length=USERNAME_FIELD_MAX_LENGTH,
        validators=[
            check_username_for_me_value,
            UnicodeUsernameValidator(),
        ])

    def validate(self, attrs):
        """Check fields request values."""
        if default_token_generator.check_token(
                get_object_or_404(User, username=attrs.get('username')),
                attrs.get('confirmation_code')
        ):
            return attrs
        raise ValidationError(
            'Неверное имя пользователя или код подтверждения'
        )


class UserSerializer(ModelSerializer):
    """User model serializer."""

    class Meta:
        model = User
        fields = (
            'bio',
            'email',
            'first_name',
            'last_name',
            'role',
            'username',
        )
