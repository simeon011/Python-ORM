# Python-ORM
Here you can see my first steps in Python ORM – working with databases through Django models and connecting them to a real PostgreSQL database.🤗

## Table of Contents:
<details>
  <summary>1. Models Basic – Django ORM</summary>
  
---
  
  This project is a **database modeling and ORM practice app** built with **Python and Django**.

It demonstrates how Django’s **Object-Relational Mapper (ORM)** connects Python classes to real SQL tables and performs database operations **without writing raw SQL queries**.

Perfect for **educational purposes**, **learning ORM fundamentals**, or as a **foundation for more complex Django applications**.

---

## 🎯 **Features**
- Define and manage models such as `Employee` and `Project`
- Create and apply migrations automatically
- Connect Django to a **PostgreSQL** database
- Explore relationships between models
- Auto-generate tables and manage them via Django Admin
- Learn the difference between field types (`CharField`, `BooleanField`, `DateField`, `DecimalField`, etc.)

---

## 🛠️ **Technologies Used**
- **Python (3.10+)** – core language  
- **Django (4.x)** – web framework and ORM  
- **PostgreSQL** – database engine  
- **PyCharm / VS Code** – development environment  
- **Docker (optional)** – PostgreSQL container  

---

## 💻 **Example Model**

```python
class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_date = models.DateField(blank=True, null=True)
```
</details>

<details>
  <summary>2. Migrations and Django Admin</summary>
  
  ---
  
  This project is a **Django ORM and database modeling application** built with **Python and Django**, designed for practicing database structures, relationships, and data migrations.

  It demonstrates how Django’s Object-Relational Mapper (ORM) connects Python models to real SQL tables and allows developers to perform database operations without writing raw   SQL.
  This app serves as a practical exercise in defining models, creating migrations, and working with PostgreSQL through the Django framework.

  Perfect for educational purposes, learning ORM fundamentals, and exploring database management in Django.
  
  ---

  ## 🎯 Features

 - Define and manage multiple Django models:

    - Course – structured model with price, lecturer, and automatic start date

    - Student – academic record keeping

    - Supplier – company and contact information

    - Person – includes logic for age group classification (Child, Teen, Adult)

    - EventRegistration – event participation management

    - Movie – example of content catalog modeling

- Create and apply migrations for structural and data changes

- Connect and manage data through PostgreSQL

- Use **RunPython** migrations to prefill or transform data automatically

- Explore the **Django Admin** Panel with custom:

    - list_display, list_filter, and search_fields

    - readonly_fields and fieldsets for structured editing

- Understand how CharField, DateField, EmailField, DecimalField, and other types behave in a real database

---
## 🛠️ Technologies Used

- Python 3.10+ – core programming language

- Django 4.x – web framework and ORM

- PostgreSQL – relational database engine

- Docker (optional) – PostgreSQL container setup

- PyCharm / VS Code – development environment

  
</details>
