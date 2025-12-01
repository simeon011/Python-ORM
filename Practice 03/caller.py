import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

# Create queries within functions

from main_app.models import Publisher, Author, Book
from django.db.models import Q, Count, Avg, F, Value, DecimalField, Case, When
from decimal import Decimal


def get_publishers(search_string=None) -> str:
    if search_string is None:
        return "No search criteria."

    publisher = Publisher.objects.filter(
        Q(name__icontains=search_string) |
        Q(country__icontains=search_string)
    ).order_by('-rating', 'name')

    if not publisher.exists():
        return "No publishers found."

    result = []
    for p in publisher:
        country_display = "Unknown" if p.country == "TBC" else p.country
        result.append(
            f"Publisher: {p.name}, country: {country_display}, rating: {p.rating:.1f}"
        )
    return "\n".join(result)


def get_top_publisher() -> str:
    top_publisher = (
        Publisher.objects.annotate(book_count=Count("book"))
        .order_by('-book_count', 'name')
        .first()
    )

    if top_publisher is None:
        return "No publishers found."

    return f"Top Publisher: {top_publisher.name} with {top_publisher.book_count} books."


def get_top_main_author() -> str:
    top_author = (
        Author.objects.annotate(
            book_count=Count("main_books"),
            avg_rating=Avg("main_books__rating")
        )
        .filter(book_count__gt=0)
        .order_by('-book_count', 'name')
        .first()
    )

    if top_author is None or top_author.book_count == 0:
        return "No results."

    own_books = top_author.main_books.all().order_by('title')
    title_string = ", ".join(book.title for book in own_books)

    avg_rating = f"{top_author.avg_rating:.1f}"

    return (
        f"Top Author: {top_author.name}, "
        f"own book titles: {title_string}, "
        f"books average rating: {avg_rating}"
    )


def get_authors_by_books_count() -> str:
    if not Author.objects.exists() or not Book.objects.exists():
        return "No results."

    authors = Author.objects.annotate(
        main_books_count=Count('main_books'),
        coauthored_books_count=Count('coauthored_books')
    ).annotate(
        total_books=F('main_books_count') + F('coauthored_books_count')
    ).filter(
        total_books__gt=0
    ).order_by(
        '-total_books', 'name'
    )[:3]

    if not authors:
        return "No results."

    result = [
        f"{author.name} authored {author.total_books} books."
        for author in authors
    ]
    return "\n".join(result)


def get_bestseller() -> str:
    bestseller = (
        Book.objects.filter(is_bestseller=True)
        .annotate(
            authors_count=Count('co_authors') + Value(1, output_field=IntegerField())
        )
        .annotate(
            composite_index=F('rating') + F('authors_count')
        )
        .select_related('main_author')
        .prefetch_related('co_authors')
        .order_by(
            '-composite_index',
            '-rating',
            '-authors_count',
            'title'
        )
        .first()
    )

    if bestseller is None:
        return "No results."

    main_author_name = bestseller.main_author.name
    coauthors = sorted([a.name for a in bestseller.co_authors.all()])
    coauthors_string = "/".join(coauthors) if coauthors else "N/A"
    composite_index_str = f"{bestseller.composite_index:.1f}"

    return (
        f"Top bestseller: {bestseller.title}, index: {composite_index_str}. "
        f"Main author: {main_author_name}. Co-authors: {coauthors_string}."
    )


def increase_price():
    books_to_update = Book.objects.filter(
        publication_date__year=2025
    ).select_related('publisher').annotate(
        total_rating=F('rating') + F('publisher__rating')
    ).filter(
        total_rating__gte=Decimal('8.0')
    )

    update_count = books_to_update.update(
        price=Case(
            When(price__gt=Decimal('50.00'), then=F('price') * Decimal('1.10')),
            default=F('price') * Decimal('1.20'),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    )

    if update_count == 0:
        return "No changes in price."

    return f"Prices increased for {update_count} book/s."