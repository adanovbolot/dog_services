from django.contrib import admin
from .models import (UserAccount,
                     Client,
                     Employee,
                     ProfileEmployee,
                     Skills,
                     Schedule,
                     ProfileClient
                     )


class SkillsInlines(admin.TabularInline):
    model = Skills
    extra = 0


class ScheduleInlines(admin.TabularInline):
    model = Schedule
    extra = 0


@admin.register(ProfileClient)
class ClientProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass


@admin.register(ProfileEmployee)
class ProfileEmployee(admin.ModelAdmin):
    inlines = [ScheduleInlines, SkillsInlines]


admin.site.register(UserAccount)
admin.site.register(Client)
