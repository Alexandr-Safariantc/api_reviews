import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title,
)

User = get_user_model()


class Command(BaseCommand):

    csv_path = 'static/data/'

    tables = {
        'category': Category,
        'genre': Genre,
        'users': User,
        'titles': Title,
        'genre_title': GenreTitle,
        'review': Review,
        'comments': Comment,
    }

    def handle(self, *args, **options):

        for table in self.tables:

            file_path = f'{self.csv_path}/{table}.csv'

            try:
                with open(file_path, mode="r", encoding="utf-8") as csvfile:
                    csv_reader = csv.DictReader(csvfile)
                    csv_data = [row for row in csv_reader]
            except FileNotFoundError:
                raise FileExistsError(
                    f'Ошибка {file_path} не найден'
                )
            else:
                class_instance = self.tables[table]

                self.create_object(
                    cls=class_instance,
                    csv_data=csv_data,
                    table=table,
                )

    def create_object(self, cls, csv_data, table):
        for obj in csv_data:
            if any(
                    True for x in ('category', 'genre', 'users') if x == table
            ):
                cls.objects.create(**obj)
                self.print_info(table)
            elif table == 'review':

                author = User.objects.get(pk=obj['author'])
                title = Title.objects.get(pk=obj['title_id'])

                Review.objects.create(
                    author=author,
                    pub_date=obj['pub_date'],
                    score=obj['score'],
                    title=title,
                    text=obj['text'],
                ).save()
                self.print_info(table)
            elif table == 'genre_title':

                genre = Genre.objects.get(pk=obj['genre_id'])
                title = Title.objects.get(pk=obj['title_id'])

                GenreTitle.objects.create(
                    genre=genre,
                    title=title,
                ).save()
                self.print_info(table)
            elif table == 'titles':

                category = Category.objects.get(pk=obj['category'])

                Title.objects.create(
                    category=category,
                    name=obj['name'],
                    year=obj['year'],
                ).save()
                self.print_info(table)
            elif table == 'comments':

                author = User.objects.get(pk=obj['author'])
                review = Review.objects.get(pk=obj['review_id'])

                Comment.objects.create(
                    author=author,
                    pub_date=obj['pub_date'],
                    review=review,
                    text=obj['text'],
                ).save()
                self.print_info(table)

    def print_info(self, name):
        self.stdout.write(
            self.style.SUCCESS(
                f'{name}.cvs has been successfully import into revievs_{name}.'
            )
        )
