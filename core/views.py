from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import Enrollment
import json
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import io

#@login_required ensure that user can see dashboard wihtout login

@login_required
def dashboard(request):
    student_data = Enrollment.objects.filter(user=request.user) #logged in user data fetch
    #creating datalist for chartjs
    course_names = [e.course.name for e in student_data]
    course_credits = [e.course.credits for e in student_data]

    context = {'enrollments': student_data,
               'course_names': json.dumps(course_names),
               'course_credits': json.dumps(course_credits)}

    return render(request, 'core/dashboard.html',context )

from django.http import HttpResponse
from reportlab.pdfgen import canvas
import io
# Ensure login_required aur models imported hain

@login_required
def export_grades_pdf(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    # PDF ka Title (Grade Report ki jagah Course Report kar diya)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, f"Course Report: {request.user.username}")

    # Logged-in user ka data
    enrollments = Enrollment.objects.filter(user=request.user)
    
    y = 750
    p.setFont("Helvetica", 12)
    
    for e in enrollments:
        # Check kar rahe hain ki kya is course ki attendance available hai
        try:
            att_pct = f"{e.attendance.attendance_percentage()}%"
        except:
            att_pct = "N/A"  # Agar admin ne attendance nahi daali hai
            
        # PDF line mein Grade ki jagah Attendance add kar diya
        text_line = f"Course: {e.course.name} | Credits: {e.course.credits} | Grade: {e.grade} | Att: {att_pct}" 
        p.drawString(100, y, text_line)
        y -= 30  # Har line ke baad gap

    p.showPage()
    p.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

@login_required
def dashboard_table(request):
    # Sirf data fetch kar rahe hain
    enrollments = Enrollment.objects.filter(user=request.user)
    
    # Dhyan do: Hum ek naye chote HTML fragment (partial) par data bhej rahe hain
    return render(request, 'core/partials/table_data.html', {'enrollments': enrollments})