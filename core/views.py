from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Attendance, Enrollment, Course
import json
from django.http import HttpResponse, JsonResponse
from reportlab.pdfgen import canvas
import io
from django.db.models import Avg, Sum # Yeh naya import hai

# Helper: Student ke enrollments fetch karna
def _get_student_enrollments(user):
    return Enrollment.objects.filter(user=user).select_related('course', 'attendance')

# Helper: Chart ke liye data taiyar karna
def _build_dashboard_chart_payload(enrollments):
    course_names = [enrollment.course.name for enrollment in enrollments]
    course_credits = [enrollment.course.credits for enrollment in enrollments]
    return {
        'course_names': course_names,
        'course_credits': course_credits,
    }

@login_required
def dashboard(request):
    # 1. Base data fetch karna
    enrollments = _get_student_enrollments(request.user)
    student_data = list(enrollments)
    
    # 2. Analytics calculate karna (Meaningful box ke liye)
    # Sabhi courses ki attendance ka average nikalna
    # Note: Hum wahi attendance lenge jo None nahi hai
    total_attendance = 0
    valid_records = 0
    for e in student_data:
        if e.attendance:
            total_attendance += e.attendance.attendance_percentage()
            valid_records += 1
    
    avg_attendance = round(total_attendance / valid_records, 1) if valid_records > 0 else 0
    total_credits = enrollments.aggregate(Sum('course__credits'))['course__credits__sum'] or 0
    
    # 3. Chart aur Low Attendance logic
    chart_payload = _build_dashboard_chart_payload(student_data)
    low_attendance_courses = [
        e for e in student_data 
        if e.attendance and e.attendance.attendance_percentage() < 75
    ]

    # 4. Updated Context
    context = {
        'enrollments': student_data,
        'low_attendance_courses': low_attendance_courses,
        'avg_attendance': avg_attendance, # Naya variable
        'total_credits': total_credits,     # Naya variable
        'course_names': json.dumps(chart_payload['course_names']),
        'course_credits': json.dumps(chart_payload['course_credits']),
    }

    return render(request, 'core/dashboard.html', context)

@login_required
def export_grades_pdf(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, f"Course Report: {request.user.username}")

    enrollments = _get_student_enrollments(request.user)
    y = 750
    p.setFont("Helvetica", 12)

    for enrollment in enrollments:
        # Attendance percentage yahan bhi () ke sath call hoga
        try:
            if enrollment.attendance:
                att_pct = f"{enrollment.attendance.attendance_percentage()}%"
            else:
                att_pct = "N/A"
        except Exception:
            att_pct = "N/A"

        text_line = (
            f"Course: {enrollment.course.name} | Credits: {enrollment.course.credits} | "
            f"Grade: {enrollment.grade} | Att: {att_pct}"
        )
        p.drawString(100, y, text_line)
        y -= 30

    p.showPage()
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

@login_required
def dashboard_table(request):
    enrollments = _get_student_enrollments(request.user)
    return render(request, 'core/partials/table_data.html', {'enrollments': enrollments})

@login_required
def dashboard_chart_data(request):
    enrollments = list(_get_student_enrollments(request.user))
    return JsonResponse(_build_dashboard_chart_payload(enrollments))

def landing(request):
    return render(request, 'core/landing.html')

@login_required
def add_course(request):
    if request.method == "POST":
        course_id = request.POST.get('course_id')
        try:
            course = Course.objects.get(id=course_id)
            # Duplicate enrollment check
            if not Enrollment.objects.filter(user=request.user, course=course).exists():
                Enrollment.objects.create(user=request.user, course=course)
            return redirect('dashboard')
        except Course.DoesNotExist:
            pass
            
    all_courses = Course.objects.all()
    return render(request, 'core/add_course.html', {'all_courses': all_courses})