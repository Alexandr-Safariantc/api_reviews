from django.contrib.auth import get_user_model
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import ALLOWED_METHODS
from .custom_viewset import CreateListDestroyModelViewSet
from .filters import TitleFilter
from .permissions import (
    IsAdminOrSuperuser,
    IsAdminOrSuperuserOrReadOnly,
    IsAuthorOrModeratorOrAdminOrSuperuser,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    TitleGetSerializer,
    UserGettingTokenSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)
from reviews.models import (
    Category,
    Genre,
    Review,
    Title,
)


User = get_user_model()


class CategoryViewSet(CreateListDestroyModelViewSet):
    """A simple ViewSet for categories."""

    lookup_field = 'slug'
    permission_classes = (IsAdminOrSuperuserOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CommentViewSet(ModelViewSet):
    """A simple ViewSet for comment."""

    http_method_names = ALLOWED_METHODS
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorOrAdminOrSuperuser,
    )
    serializer_class = CommentSerializer

    def get_review(self):
        """Return review instance in case of existing one."""
        return get_object_or_404(
            Review, pk=self.kwargs.get('review_id'),
            title__pk=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        """Get comments instances of review."""
        return self.get_review().comments.all()

    def perform_create(self, serializer: Serializer):
        """Save values for author and review fields."""
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )


class GenreViewSet(CreateListDestroyModelViewSet):
    """A simple ViewSet for genres."""

    lookup_field = 'slug'
    permission_classes = (IsAdminOrSuperuserOrReadOnly,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(ModelViewSet):
    """A simple ViewSet for reviews."""

    http_method_names = ALLOWED_METHODS
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorOrAdminOrSuperuser,
    )
    serializer_class = ReviewSerializer

    def get_title(self):
        """Return title instance in case of existing one."""
        return get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        """Get reviews instances of title."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer: Serializer):
        """Save values for author and title fields."""
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class TitleViewSet(ModelViewSet):
    """A simple ViewSet for title."""

    http_method_names = ALLOWED_METHODS
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrSuperuserOrReadOnly,)
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    )
    serializer_class = TitleSerializer

    def get_serializer_class(self):
        """Define serializer for different methods."""
        if self.request.method == 'GET':
            return TitleGetSerializer
        return TitleSerializer


class UserCreateView(APIView):
    """A simple View for creating users."""

    def post(self, request):
        """Send confirmation code to existing user or create new one."""
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)


class UserGetTokenView(APIView):
    """A simple View for JWT generation."""

    def post(self, request):
        """Generate and return JWT to user."""
        serializer = UserGettingTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
            'token': str(
                AccessToken.for_user(
                    user=get_object_or_404(
                        User,
                        username=serializer.validated_data.get('username')
                    )
                )
            )
        })


class UserViewSet(ModelViewSet):
    """A simple ViewSet for user."""
    http_method_names = ALLOWED_METHODS
    filter_backends = (SearchFilter,)
    lookup_field = 'username'
    permission_classes = (IsAdminOrSuperuser,)
    queryset = User.objects.all()
    search_fields = ('username',)
    serializer_class = UserSerializer

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(IsAuthenticated,),
        url_name='me',
        url_path='me',
    )
    def manage_request_user_data(self, request):
        """Process allowed methods for request User instance."""
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                context={'request': request},
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=HTTP_200_OK)
