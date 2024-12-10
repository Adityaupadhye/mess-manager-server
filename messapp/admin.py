from django.contrib import admin
from .models import FoodMenu, MessRebates, User,FoodLog

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'hostel', 'roll_no', 'role')

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(FoodLog)
admin.site.register(FoodMenu)
admin.site.register(MessRebates)