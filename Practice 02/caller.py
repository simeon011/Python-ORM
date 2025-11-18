import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app import querysets
from main_app.models import Director, Actor, Movie
from django.db.models import Count, Avg

# Import your models here

# Create queries within functions

from django.db.models import Q


def get_directors(search_name=None, search_nationality=None) -> str:
    if search_name is None and search_nationality is None:
        return ""

    if search_name is not None and search_nationality is not None:
        directors = Director.objects.filter(
            full_name__icontains=search_name,
            nationality__icontains=search_nationality
        ).order_by('full_name')

    elif search_name is not None:
        directors = Director.objects.filter(
            full_name__icontains=search_name
        ).order_by('full_name')

    else:
        directors = Director.objects.filter(
            nationality__icontains=search_nationality
        ).order_by('full_name')

    if not directors.exists():
        return ""

    return "\n".join(
        f"Director: {d.full_name}, nationality: {d.nationality}, experience: {d.years_of_experience}"
        for d in directors
    )


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def get_top_director() -> str:
    director = Director.objects.get_directors_by_movies_count().first()
    if not director:
        return ""
    return f"Top Director: {director.full_name}, movies: {director.movies_count}."


def get_top_actor() -> str:
    actor = (
        Actor.objects.annotate(
            movies_count=Count('movie'),
            avg_rating=Avg('movie__rating')
        )
        .filter(movie__isnull=False)
        .order_by('-movies_count', 'full_name')
        .first()
    )
    if not actor:
        return ""
    movies = Movie.objects.filter(starring_actor=actor)
    movie_titles = ", ".join(m.title for m in movies)
    avg_rating = movies.aggregate(avg=Avg('rating'))['avg'] or 0
    avg_rating = f"{avg_rating:.1f}"
    return (
        f"Top Actor: {actor.full_name}, "
        f"starring in movies: {movie_titles}, "
        f"movies average rating: {avg_rating}"
    )


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def get_actors_by_movies_count() -> str:
    actors = (
        Actor.objects
        .annotate(movies_count=Count('actor_movie'))
        .order_by('-movies_count', 'full_name')[:3]
    )
    if not actors or actors[0].movies_count == 0:
        return ""
    return "\n".join(
        f"{a.full_name}, participated in {a.movies_count} movies"
        for a in actors
    )



def get_top_rated_awarded_movie() -> str:
    top_movie = (
        Movie.objects
        .filter(is_awarded=True)
        .select_related('starring_actor')
        .prefetch_related('actors')
        .order_by('-rating', 'title')
        .first()
    )
    if not top_movie:
        return ""
    rating = f"{top_movie.rating:.1f}"
    starring_actor = (
        top_movie.starring_actor.full_name
        if top_movie.starring_actor
        else "N/A"
    )
    participation_actors = (
        top_movie.actors
        .order_by('full_name')
        .values_list('full_name', flat=True)
    )
    cast = ", ".join(participation_actors)
    return (
        f"Top rated awarded movie: {top_movie.title}, rating: {rating}. "
        f"Starring actor: {starring_actor}. Cast: {cast}."
    )



def increase_rating() -> str:
    movies_upd = Movie.objects.filter(is_classic=True, rating__lt=10)
    if not movies_upd:
        return "No ratings increased"
    update_movie_count = movies_upd.count()
    movies_upd.update(rating=F('rating') + 0.1)

    return f"Rating increased for {update_movie_count} movies."

 
