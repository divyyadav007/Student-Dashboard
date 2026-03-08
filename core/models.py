from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=100)
    credits = models.IntegerField()
    
    def __str__(self):
        return self.name

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(max_length=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.course.name}"
    
class Attendance(models.Model):
    enrollment = models.OneToOneField(Enrollment,on_delete=models.CASCADE)
    total_classes = models.IntegerField(default=0)
    classes_attended = models.IntegerField(default=0)

    #helper function to calculate percentage
    def attendance_percentage(self):
        if self.total_classes > 0:
            return (self.classes_attended / self.total_classes) * 100
        else:
            return 0.0
    
    def __str__(self):
        return f"Attendance for {self.enrollment}"
