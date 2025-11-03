import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

# Create queries within functions
from main_app.models import Author, Book, Song, Artist, Product, Review, Driver, DrivingLicense, Owner, Car, Registration
from datetime import date, timedelta, datetime


def show_all_authors_with_their_books():
    authors = Author.objects.all().order_by('id')
    authors_with_books = []
    for a in authors:
        book = authors.book_set.all()
        if book:
            continue

        titles = ', '.join(b.title for b in books)
        authors_with_books.append(
            f"{author.name} has written - {titles}!"
        )

    return '\n'.join(authors_with_books)


def delete_all_authors_without_books():
    Author.objects.filter(book__isnull=True).delete()


def add_song_to_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.add(song)


def get_songs_by_artist(artist_name: str):
    artist = Artist.objects.get(name=artist_name)
    songs = artist.songs.order_by('-id')
    return songs


def remove_song_from_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.remove(song)


def calculate_average_rating_for_product_by_name(product_name: str):
    product = Product.objects.get(name=product_name)
    reviews = product.reviews.all()
    avg_score = sum(r.rating for r in reviews) / len(reviews)
    return avg_score


def get_reviews_with_high_ratings(threshold: int):
    review = Review.objects.filter(rating__gt=threshold)
    return review


def get_products_with_no_reviews():
    return Product.objects.filter(reviews__isnull=True).order_by('-name')


def delete_products_without_reviews():
    Product.objects.filter(reviews__isnull=True).delete()


def calculate_licenses_expiration_dates():
    licenses = DrivingLicense.objects.all().order_by('-license_number')
    result = []

    for l in licenses:
        expiration_date = l.issue_date + timedelta(days=365)
        result.append(
            f"License with number: {l.license_number} expires on {expiration_date}!"
        )

    return "\n".join(result)


def get_drivers_with_expired_licenses(due_date: date):
    expired = []

    for l in DrivingLicense.objects.all():
        expiration_date = l.issue_date + timedelta(days=365)
        if expiration_date <= due_date:
            expired.append(l.driver)
    return expired


def register_car_by_owner(owner: Owner) -> str:
    car = Car.objects.filter(registration__isnull=True).first()
    registration = Registration.objects.filter(car__isnull=True).first()

    car.owner = owner
    car.registration = registration

    car.save()

    registration.registration_date = datetime.today()
    registration.car = car

    registration.save()

    return f"Successfully registered {car.model} to {owner.name} with registration number {registration.registration_number}."