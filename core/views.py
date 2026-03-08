"""Views control what data is loaded and which template or response is returned."""

# render loads an HTML template and fills it with context data.
from django.shortcuts import redirect, render

# login_required blocks anonymous users from protected pages.
from django.contrib.auth.decorators import login_required

# Enrollment gives us student-course data and Attendance helps us handle missing attendance safely.
from .models import Attendance, Enrollment, Course

# json converts Python data into JavaScript-friendly strings for templates.
import json

# HttpResponse sends raw responses and JsonResponse sends JSON responses.
from django.http import HttpResponse, JsonResponse

# canvas is used to generate PDFs with ReportLab.
from reportlab.pdfgen import canvas

# io lets us create an in-memory file buffer for PDF downloads.
import io


# This helper fetches the logged-in student's enrollments together with related course and attendance data.
def _get_student_enrollments(user):
    # select_related reduces extra database queries for related objects.
    return Enrollment.objects.filter(user=user).select_related('course', 'attendance')


# This helper converts enrollment objects into a simple chart payload.
def _build_dashboard_chart_payload(enrollments):
    # course_names becomes the X-axis labels in the chart.
    course_names = [enrollment.course.name for enrollment in enrollments]
    # course_credits becomes the Y-axis values in the chart.
    course_credits = [enrollment.course.credits for enrollment in enrollments]
    # Return both pieces together as one dictionary.
    return {
        'course_names': course_names,
        'course_credits': course_credits,
    }


# Only logged-in users should be able to open the dashboard.
@login_required
def dashboard(request):
    # Load all enrollments for the current user.
    student_data = list(_get_student_enrollments(request.user))
    # Build data for the credits chart.
    chart_payload = _build_dashboard_chart_payload(student_data)

    # This context is passed into dashboard.html.
    context = {
        'enrollments': student_data,
        'course_names': json.dumps(chart_payload['course_names']),
        'course_credits': json.dumps(chart_payload['course_credits']),
    }

    # Render the main dashboard page.
    return render(request, 'core/dashboard.html', context)


# Only logged-in users should be able to download their PDF report.
@login_required
def export_grades_pdf(request):
    # Create a memory buffer instead of saving a temporary file on disk.
    buffer = io.BytesIO()
    # Attach a PDF canvas to that in-memory buffer.
    p = canvas.Canvas(buffer)

    # Write the heading text near the top of the PDF page.
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, f"Course Report: {request.user.username}")

    # Fetch the current user's enrollments for the report.
    enrollments = _get_student_enrollments(request.user)

    # Start printing course rows slightly lower on the page.
    y = 750
    # Use normal font for the row content.
    p.setFont("Helvetica", 12)

    # Loop through each enrolled course and print one line per course.
    for enrollment in enrollments:
        # Attendance may not exist yet, so handle that case safely.
        try:
            att_pct = f"{enrollment.attendance.attendance_percentage()}%"
        except Attendance.DoesNotExist:
            # Show N/A when attendance has not been entered yet.
            att_pct = "N/A"

        # Build the text for one course row in the PDF.
        text_line = (
            f"Course: {enrollment.course.name} | Credits: {enrollment.course.credits} | "
            f"Grade: {enrollment.grade} | Att: {att_pct}"
        )
        # Draw that text on the PDF at the current vertical position.
        p.drawString(100, y, text_line)
        # Move down before printing the next row.
        y -= 30

    # Finish the current page.
    p.showPage()
    # Finalize the PDF content.
    p.save()

    # Move the buffer pointer back to the beginning so Django can read it.
    buffer.seek(0)
    # Send the generated PDF back to the browser.
    return HttpResponse(buffer, content_type='application/pdf')


# This view returns only the table rows so HTMX can refresh them without reloading the page.
@login_required
def dashboard_table(request):
    # Load the current user's enrollments.
    enrollments = _get_student_enrollments(request.user)

    # Render only the partial template that contains table rows.
    return render(request, 'core/partials/table_data.html', {'enrollments': enrollments})


# This view returns fresh chart data as JSON for the polling JavaScript.
@login_required
def dashboard_chart_data(request):
    # Load the current user's enrollments.
    enrollments = list(_get_student_enrollments(request.user))
    # Convert enrollments into JSON-ready chart data.
    return JsonResponse(_build_dashboard_chart_payload(enrollments))


# The landing page is public, so anyone can open it.
def landing(request):
    # Render the public home page.
    return render(request, 'core/landing.html')

@login_required
def add_course(request):
    if request.method == "POST":
        course_id = request.POST.get('course_id') # Form se course ID lena
        
        # Course object dhoondna database mein
        try:
            course = Course.objects.get(id=course_id)
            
            # Check karna ki student ne pehle se toh enroll nahi kiya
            if not Enrollment.objects.filter(user=request.user, course=course).exists():
                Enrollment.objects.create(user=request.user, course=course)
                
            return redirect('dashboard') # Success ke baad dashboard bhejo
        except Course.DoesNotExist:
            # Agar course nahi mila toh error dikha sakte hain
            pass
            
    # Agar sirf page khola hai (GET), toh saare available courses dikhao
    all_courses = Course.objects.all()
    return render(request, 'core/add_course.html', {'all_courses': all_courses})