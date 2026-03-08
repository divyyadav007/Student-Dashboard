# path creates one URL pattern.
from django.urls import path

# views imports the functions we wrote in views.py.
from . import views

# auth_views gives us Django's built-in login and logout pages.
from django.contrib.auth import views as auth_views


# urlpatterns connects each URL path to a view.
urlpatterns = [
    # /dashboard/ shows the main student dashboard.
    path('dashboard/', views.dashboard, name='dashboard'),
    # /export-pdf/ downloads the current user's PDF report.
    path('export-pdf/', views.export_grades_pdf, name='export_pdf'),
    # /dashboard/table/ returns only the dashboard table rows for HTMX refreshes.
    path('dashboard/table/', views.dashboard_table, name='dashboard_table'),
    # /dashboard/chart-data/ returns JSON used to refresh the chart.
    path('dashboard/chart-data/', views.dashboard_chart_data, name='dashboard_chart_data'),
    # /login/ uses Django's built-in login view with our custom template.
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    # /logout/ uses Django's built-in logout view.
    path('logout/', auth_views.LogoutView.as_view(template_name='core/logout.html'), name='logout'),
    # The empty path is the landing page shown at the site root.
    path('', views.landing, name='landing'),
    path('add-course/', views.add_course, name='add_course'),
]