from django.db import models

class User(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
        ('staff', 'Staff'),
    ]

    username = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    hostel = models.CharField(max_length=50, blank=True, null=True)
    roll_no = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

class FoodLog(models.Model):
    FOOD_CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('snacks', 'Snacks'),
        ('dinner', 'Dinner'),
    ]

    PERSON_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
        ('staff', 'Staff'),
    ]

    roll_no = models.CharField(max_length=20)
    type = models.CharField(max_length=10, choices=PERSON_CHOICES, default='student')
    food_category = models.CharField(max_length=50,choices=FOOD_CATEGORY_CHOICES)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f'{self.roll_no} - {self.food_category} - {self.timestamp}'
    

class FoodMenu(models.Model):

    FOOD_CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('snacks', 'Snacks'),
        ('dinner', 'Dinner'),
    ]


    food_category = models.CharField(max_length=50,choices=FOOD_CATEGORY_CHOICES)
    date = models.DateField()
    menu = models.CharField(max_length=150)
    food_wastage = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


