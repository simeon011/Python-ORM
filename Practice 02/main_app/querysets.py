from django.db import models
from django.db.models import QuerySet, Count


class CustomQuerySet(models.QuerySet):
    def get_directors_by_movies_count(self) -> QuerySet:
        return self.annotate(movies_count=Count('movie')).order_by('-movies_count', 'full_name')