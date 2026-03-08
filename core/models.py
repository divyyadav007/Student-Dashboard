# models contains Django field classes like CharField and ForeignKey.
from django.db import models

# User is Django's built-in user model used for login accounts.
from django.contrib.auth.models import User


# Course stores one subject that a student can enroll in.
class Course(models.Model):
    # name stores the course title, for example "Data Structures".
    name = models.CharField(max_length=100)
    # credits stores how many credits this course is worth.
    credits = models.IntegerField()
    
    def __str__(self):
        # Django uses this readable text in admin dropdowns and lists.
        return self.name


# Enrollment links one user to one course.
class Enrollment(models.Model):
    # user points to the student who enrolled.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # course points to the selected course.
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # enrollment_date is filled automatically when the record is created.
    enrollment_date = models.DateTimeField(auto_now_add=True)
    # grade stores the student's grade and can stay empty until assigned.
    grade = models.CharField(max_length=2, null=True, blank=True)
    
    def __str__(self):
        # This readable label helps identify an enrollment quickly.
        return f"{self.user.username} - {self.course.name}"
    

# Attendance stores attendance details for one enrollment.
class Attendance(models.Model):
    # OneToOneField means each enrollment has at most one attendance record.
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE)
    # total_classes is the total number of classes conducted.
    total_classes = models.IntegerField(default=0)
    # classes_attended is how many of those classes the student attended.
    classes_attended = models.IntegerField(default=0)

    # This helper calculates attendance percentage for display in templates and admin.
    def attendance_percentage(self):
        # Avoid division by zero when no classes have been entered yet.
        if self.total_classes > 0:
            # Convert attended classes into a percentage value.
            return (self.classes_attended / self.total_classes) * 100
        else:
            # If no classes exist yet, attendance is treated as 0%.
            return 0.0
    
    def __str__(self):
        # This readable text appears in admin and debug output.
        return f"Attendance for {self.enrollment}"
