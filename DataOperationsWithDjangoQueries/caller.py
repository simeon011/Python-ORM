import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character


def create_pet(name: str, species: str) -> str:
    pet = Pet(name=name, species=species)
    pet.save()

    return f"{pet.name} is a very cute {pet.species}!"


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool) -> str:
    artifact = Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )
    artifact.save()

    return f"The artifact {artifact.name} is {artifact.age} years old!"


def rename_artifact(artifact: Artifact, new_name: str) -> None:
    if artifact.age > 250 and artifact.is_magical:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts() -> None:
    Artifact.objects.all().delete()


def show_all_locations() -> str:
    locations = Location.objects.all().order_by('-id')
    return '\n'.join(f"{loc.name} has a population of {loc.population}!" for loc in locations)


def new_capital() -> None:
    location = Location.objects.first()
    location.is_capital = True
    location.save()


def get_capitals():
    return Location.objects.filter(is_capital=True)


def delete_first_location() -> None:
    Location.objects.first().delete()


def apply_discount():
    for car in Car.objects.all():
        per_off = Decimal(str(sum(int(d) for d in str(car.year)) / 100))
        discount = car.price * per_off
        car.price_with_discount = car.price - discount
        car.save()


def get_recent_cars():
    Car.objects.filter(year__gt=2020).values('model', ' price_with_discount')


def delete_last_car():
    Car.objects.last().delete()


def show_unfinished_tasks() -> str:
    tasks = Task.objects.filter(completed=False)
    return '\n'.join(f"Task - {t.title} needs to be done until {t.due_date}" for t in tasks)


def complete_odd_tasks():
    tasks = Task.objects.all()
    for t in tasks:
        if t.id % 2 != 0 and t.completed == False:
            t.completed = True
            t.save()


    # Task.objects.filter(id__mod(2, 1), completed=False).update(cpmplated=True)


def encode_and_replace(text: str, task_title: str):
    encoded_text = ''.join(chr(ord(l) - 3) for l in text)
    Task.objects.filter(title=task_title).update(description=encoded_text)


def get_deluxe_rooms() -> str:
    deluxe_rooms = HotelRoom.objects.filter(room_type='Deluxe').order_by('id')

    deluxe_rooms = [r for r in deluxe_rooms if r.id % 2 == 0]

    return '\n'.join(
        f"Deluxe room with number {r.room_number} costs {r.price_per_night}$ per night!"
        for r in deluxe_rooms
    )


def increase_room_capacity() -> None:
    rooms = HotelRoom.objects.all().order_by('id')

    previous_capacity = 0

    for index, room in enumerate(rooms):
        if room.is_reserved:
            if index == 0:

                room.capacity += room.id
            else:

                room.capacity += rooms[index - 1].capacity

            room.save()


def reserve_first_room() -> None:
    first_room = HotelRoom.objects.first()
    if first_room and not first_room.is_reserved:
        first_room.is_reserved = True
        first_room.save()


def delete_last_room() -> None:
    last_room = HotelRoom.objects.last()
    if last_room and not last_room.is_reserved:
        last_room.delete()


def update_characters():
    characters = Character.objects.all()
    for c in characters:
        if c.class_name == 'Mage':
            c.level += 3
            c.intelligence -= 7
        elif c.class_name == 'Warrior':
            c.hit_points = c.hit_points / 2
            c.dexterity += 4
        elif c.class_name in ['Assassin', 'Scout']:
            c.inventory = 'The inventory is empty'
        c.save()


def fuse_characters(first_character: Character, second_character: Character):
    new_name = f"{first_character.name} {second_character.name}"
    new_class = "Fusion"
    new_level = (first_character.level + second_character.level) // 2
    new_strength = int((first_character.strength + second_character.strength) * 1.2)
    new_dexterity = int((first_character.dexterity + second_character.dexterity) * 1.4)
    new_intelligence = int((first_character.intelligence + second_character.intelligence) * 1.5)
    new_hit_points = first_character.hit_points + second_character.hit_points

    if first_character.class_name in ["Mage", "Scout"]:
        new_inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    else:  # Warrior or Assassin
        new_inventory = "Dragon Scale Armor, Excalibur"

    fusion_character = Character.objects.create(
        name=new_name,
        class_name=new_class,
        level=new_level,
        strength=new_strength,
        dexterity=new_dexterity,
        intelligence=new_intelligence,
        hit_points=new_hit_points,
        inventory=new_inventory,
    )

    first_character.delete()
    second_character.delete()

    return fusion_character


def grand_dexterity():
    Dexterity.objects.update(dexterity=30)


def grand_intelligence():
    Intelligance.objects.update(intelligence=40)


def grand_strength():
    Strength.objects.update(strength=50)


def delete_characters():
    Character.objects.filter(inventory='The inventory is empty').delete()
