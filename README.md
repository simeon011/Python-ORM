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
</details>
