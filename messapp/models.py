from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ValidationError

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


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
    # updated_time = models.DateTimeField(auto_now=True)
    profile_photo = models.ImageField(upload_to='profile_pics/',blank=True,null=True)

class FoodLog(models.Model):
    FOOD_CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('snacks', 'Snacks'),
        ('dinner', 'Dinner'),
        ('milk', 'Milk'),
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

    # new fields
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["roll_no", "food_category", "date"],
                name="unique_roll_food_date" # ensures one person can take only one meal of a category per day
            )
        ]

    def __str__(self):
        field_values = []
        for field in self._meta.get_fields():
            field_values.append(str(getattr(self, field.name, '')))
        return ' '.join(field_values)
    

class FoodMenu(models.Model):

    FOOD_CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('snacks', 'Snacks'),
        ('dinner', 'Dinner'),
        ('milk', 'Milk'),
    ]


    food_category = models.CharField(max_length=50,choices=FOOD_CATEGORY_CHOICES)
    date = models.DateField()
    menu = models.JSONField() #Added JSON field instead of text field for proper formatting.
    food_wastage = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['date', 'food_category'], name='unique_date_category')
        ]


class MessRebates(TimeStampedModel):

    REBATE_STATUS_OPTIONS = [
        ('pending', 'pending'), # student has requested but not yet approved
        ('inactive', 'inactive'), # approved but start date not reached yet
        ('active', 'active'), # today's date is between start and end
        ('expired', 'expired'), # today's date greater than end date
        ('rejected', 'rejected') # manager rejects the request (entry to be deleted)
    ]

    hostel = models.CharField(max_length=30, default='', null=False)
    roll_no = models.CharField(max_length=20, unique=False, null=False)
    status = models.CharField(max_length=20, choices=REBATE_STATUS_OPTIONS, default='pending')
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    duration = models.IntegerField(
        editable=True,
        validators=[
            MinValueValidator(2, message='Minimum Rebate days is 2'),
            MaxValueValidator(15, message='Maximum Rebate days is 15')
        ]
    )

class Feedback(models.Model):
    feedback_text= models.TextField(max_length=500)
    date=models.DateTimeField(auto_now_add=True)

class Rating(models.Model):
    rating= models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    timestamp = models.DateTimeField(auto_now_add=True)


