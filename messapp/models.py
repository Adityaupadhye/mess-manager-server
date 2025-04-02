from time import localtime
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ValidationError

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def user_profile_photo_path(instance, filename):
    # Store images in 'profile_photos/<username>/' directory
    extension = filename.split('.')[-1]
    return f"profile_photos/{instance.username}/profile.{extension}"

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

    profile_photo = models.ImageField(upload_to=user_profile_photo_path, blank=True, null=True)

    def delete(self, *args, **kwargs):
        # Delete the profile photo when the user is deleted
        if self.profile_photo:
            if os.path.isfile(self.profile_photo.path):
                os.remove(self.profile_photo.path)
        super().delete(*args, **kwargs)

class FoodLog(models.Model):
    FOOD_CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('snacks', 'Snacks'),
        ('dinner', 'Dinner'),
        ('milk', 'Milk')
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

    date = models.DateField(null=True, blank=True)  # New column for date
    time = models.TimeField(null=True, blank=True)  # New column for time

    def save(self, *args, **kwargs):
        if self.timestamp:
            local_timestamp = localtime(self.timestamp)
            self.date = local_timestamp.date()
            self.time = local_timestamp.time()
        super().save(*args, **kwargs)

    def __str__(self):
        field_values = []
        for field in self._meta.get_fields():
            field_values.append(str(getattr(self, field.name, '')))
        return ' '.join(field_values)
    
    class Meta:
        unique_together = ('roll_no', 'food_category', 'date')
    

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

