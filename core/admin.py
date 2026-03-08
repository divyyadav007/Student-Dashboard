# admin gives us Django's admin customization tools.
from django.contrib import admin

# Import the models we want to manage from the admin panel.
from .models import Course, Enrollment, Attendance

# Register Course so admins can create and edit courses from /admin/.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # Show these columns in the course list page.
    list_display = ('name', 'credits')
    # Add a search box that searches by course name.
    search_fields = ('name',)
    # Add a filter sidebar based on credits.
    list_filter = ('credits',)

# Register Enrollment so admins can manage which user is in which course.
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    # Show these columns in the enrollment list.
    list_display = ('user', 'course', 'enrollment_date')
    # Search by username or course name.
    search_fields = ('user__username', 'course__name')
    # Filter enrollment list by date.
    list_filter = ('enrollment_date',)
    # Use raw ID input for user to keep large dropdowns manageable.
    raw_id_fields = ('user',)
    # Show date navigation links at the top of the admin list page.
    date_hierarchy = 'enrollment_date'
    # Newer enrollments appear first.
    ordering = ('-enrollment_date',)
    # Use autocomplete widget for the user relation.
    autocomplete_fields = ('user',)
    # Show enrollment_date but do not allow editing it manually.
    readonly_fields = ('enrollment_date',)
    # Hide enrollment_date from the editable form because it is auto-created.
    exclude = ('enrollment_date',)
    # Only show user and course fields in the form.
    fields = ('user', 'course')

# Register Attendance so admins can manage class counts.
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    # Show the enrollment and attendance numbers in the admin list.
    list_display = ('enrollment', 'total_classes', 'classes_attended', 'attendance_percentage')