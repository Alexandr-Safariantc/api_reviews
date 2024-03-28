from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

from api_yamdb.settings import (
    CHAR_FIELD_MAX_LENGTH,
    SLUG_FIELD_MAX_LENGTH,
)
from reviews.validators import check_rate, check_year

User = get_user_model()


class CategoryGenreBaseModel(models.Model):
    """Describes category and genre base model."""

    name = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=SLUG_FIELD_MAX_LENGTH,
        verbose_name='Слаг категории',
        unique=True,
    )

    def __str__(self):
        """Returns text representation of the class."""
        return self.name

    def save(self, *args, **kwargs):
        """Saves the slug value if it is not entered."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(CategoryGenreBaseModel):
    """Describes category model."""

    class Meta:
        default_related_name = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreBaseModel):
    """Describes genre model."""

    class Meta:
        default_related_name = 'genres'
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Describes title model."""

    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория'
    )
    description = models.TextField(
        blank=True,
        default='',
        verbose_name='Описание',
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр',
    )
    name = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH,
        verbose_name='Название произведения',
    )
    year = models.SmallIntegerField(
        help_text='Допускается только текущий год или предшествующие.',
        validators=[
            check_year,
        ],
        verbose_name='Год создания',
    )

    class Meta:
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        """Returns text representation of the class."""
        return f'{self.name} {self.year} year'


class GenreTitle(models.Model):
    """Describes cross table for genre and title models."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )

    class Meta:
        verbose_name = 'Связь жанр-название'
        verbose_name_plural = 'Связи жанры-названия'

    def __str__(self):
        """Returns text representation of the class."""
        return f'{self.title}-{self.genre}'


class ReviewCommentBaseModel(models.Model):
    """Describes review and comment base model."""

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    text = models.TextField()

    def __str__(self):
        """Returns text representation of the class."""
        return self.text


class Review(ReviewCommentBaseModel):
    """Describes review model."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    score = models.IntegerField(
        validators=[
            check_rate,
        ],
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    class Meta:
        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
        )


class Comment(ReviewCommentBaseModel):
    """Describes comment model."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta:
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
