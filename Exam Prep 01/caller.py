import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_skeleton.settings')
django.setup()

from main_app.models import Profile, Product, Order
from django.db.models import Q, F


def populate_db():
    profile1 = Profile.objects.create(
        full_name="Ivan Petrov",
        email="ivan.petrov@example.com",
        phone_number="+359888123456",
        address="Sofia, Bulgaria"
    )

    profile2 = Profile.objects.create(
        full_name="Maria Georgieva",
        email="maria.georgieva@example.com",
        phone_number="+359888654321",
        address="Plovdiv, Bulgaria"
    )

    product1 = Product.objects.create(
        name="Laptop",
        description="15-inch business laptop",
        price=1299.99,
        in_stock=5
    )

    product2 = Product.objects.create(
        name="Wireless Mouse",
        description="Ergonomic wireless mouse",
        price=29.99,
        in_stock=20
    )

    order1 = Order.objects.create(
        profile=profile1,
        total_price=1329.98,
        is_completed=False
    )
    order1.products.add(product1, product2)

    order2 = Order.objects.create(
        profile=profile2,
        total_price=1299.99,
        is_completed=True
    )
    order2.products.add(product1)

    print("Database populated successfully!")


def get_profiles(search_string=None) -> str:
    if search_string is None:
        return ""

    profile_match = Profile.objects.filter(
        Q(full_name__icontans=search_string) | Q(email__icontains=search_string) | Q(
            phone_number__icontains=search_string)
    ).order_by('full_name')

    return "\n".join(
        f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.order_set.count()}"
        for p in profile_match
    )


def get_loyal_profiles() -> str:
    loyal_profiles = Profile.objects.get_regular_customers()
    return "\n".join(f"Profile: {p.full_name}, orders: {p.count_orders}"
                     for p in loyal_profiles)


def get_last_sold_products() -> str:
    last_order = Order.objects.last()
    if not last_order:
        return ""
    return f"Last sold products: {', '.join(p.name for p in last_order.products.all())}"


def get_top_products() -> str:
    top_products = Products.objects.annotate(
        orders_count=Count('order')
    ).filter(order_count__gt=0
             ).order_by('-orders_count', 'name')[:5]

    return "Top products:\n" + "\n".join(f"{p.name}, sold {p.orders_count} times" for p in top_products)

    if not top_products.exists():
        return ""


def apply_discounts() -> str:
    updated_records = Order.objects.annotate(
        products_count=Count('products')
    ).filter(products_count__gt=2, is_completed=False).update(total_price=F('total_price' * 0.90))

    return f"Discount applied to {updated_records} orders."


def complete_order() -> str:
    order = Order.objects.filter(is_completed=False).order_by('creation_date').first()
    if not order:
        return ""

    order.is_completed = True
    Product.objects.update(order=order).update(in_stock=F('in_stock') - 1, is_available=Case(
        When(in_stock=1, then=Value(False)),
        default=F('is_available')
    ))
    order.save()

    return "Order has been completed!"


if __name__ == "__main__":
    populate_db()
