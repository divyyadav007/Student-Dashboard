from django.contrib import admin

# Register your models here.
from .models import Course, Enrollment, Attendance

#registering course model
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'credits')
    search_fields = ('name',)
    list_filter = ('credits',)

#registering enrolllment model
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrollment_date')
    search_fields = ('user__username', 'course__name')
    list_filter = ('enrollment_date',)
    raw_id_fields = ('user',)
    date_hierarchy = 'enrollment_date'
    ordering = ('-enrollment_date',)
    autocomplete_fields = ('user',)
    readonly_fields = ('enrollment_date',)
    exclude = ('enrollment_date',)
    fields = ('user', 'course')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'total_classes', 'classes_attended', 'attendance_percentage')