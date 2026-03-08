# Django Project Flow Guide

This file explains how your project works from URL to view to model to template in simple language.

## Big Picture

When a user opens your site, Django handles the request in this order:

1. The browser requests a URL.
2. Django checks which URL pattern matches.
3. Django calls the related view function.
4. The view may read data from models.
5. The view sends that data to a template.
6. The template becomes HTML and is returned to the browser.

In your project, that path starts at [dashboard_project/urls.py](dashboard_project/urls.py), then goes into [core/urls.py](core/urls.py), then into [core/views.py](core/views.py), then sometimes into [core/models.py](core/models.py), and finally into templates inside [core/templates/core](core/templates/core).

## Step 1: Project URL Entry

The first URL file Django reads is [dashboard_project/urls.py](dashboard_project/urls.py).

What it does:

- It says `/admin/` should go to Django admin.
- It says all other URLs should be handled by the `core` app.

So if a user visits `/dashboard/`, Django first comes here, then forwards that request into [core/urls.py](core/urls.py).

## Step 2: App URL Routing

Inside [core/urls.py](core/urls.py), each route is connected to a view.

Examples:

- `/` goes to `landing`
- `/login/` goes to Django’s built-in login view
- `/dashboard/` goes to `dashboard`
- `/dashboard/table/` goes to `dashboard_table`
- `/dashboard/chart-data/` goes to `dashboard_chart_data`
- `/export-pdf/` goes to `export_grades_pdf`

This file is basically the traffic controller.

## Step 3: Views Do The Main Work

The real logic happens in [core/views.py](core/views.py).

Each view function answers one request.

Important views:

- `landing(request)`
- `dashboard(request)`
- `dashboard_table(request)`
- `dashboard_chart_data(request)`
- `export_grades_pdf(request)`

What each one does:

### `landing`

- Shows the public home page.
- It does not need login.
- It renders [core/templates/core/landing.html](core/templates/core/landing.html).

### `dashboard`

- Requires login because of `@login_required`.
- Gets the current user’s enrollments from the database.
- Builds chart data.
- Sends both table data and chart data into [core/templates/core/dashboard.html](core/templates/core/dashboard.html).

### `dashboard_table`

- Also requires login.
- Returns only the table rows, not the full page.
- This is used by HTMX to refresh the course table every 5 seconds.
- It renders [core/templates/core/partials/table_data.html](core/templates/core/partials/table_data.html).

### `dashboard_chart_data`

- Requires login.
- Returns JSON instead of HTML.
- The JavaScript in the dashboard page uses this to refresh the chart without reloading the whole page.

### `export_grades_pdf`

- Requires login.
- Reads the logged-in user’s enrollments.
- Creates a PDF in memory.
- Returns that PDF file directly to the browser.

So views are the bridge between URLs, database, and templates.

## Step 4: Models Hold Database Structure

The database structure is defined in [core/models.py](core/models.py).

You have three main models:

### `Course`

- Stores course name and credits.

### `Enrollment`

- Connects one user to one course.
- Also stores grade and enrollment date.

### `Attendance`

- Connects to one enrollment.
- Stores total classes and attended classes.
- Has a helper function to calculate attendance percentage.

How they relate:

- One user can have many enrollments.
- One course can appear in many enrollments.
- One enrollment has one attendance record.

This is the data layer of the app.

## Step 5: Templates Show Data

Templates turn Python data into HTML.

Main templates:

- [core/templates/core/landing.html](core/templates/core/landing.html)
- [core/templates/core/login.html](core/templates/core/login.html)
- [core/templates/core/dashboard.html](core/templates/core/dashboard.html)
- [core/templates/core/base.html](core/templates/core/base.html)
- [core/templates/core/partials/table_data.html](core/templates/core/partials/table_data.html)

How they work:

### [core/templates/core/base.html](core/templates/core/base.html)

- Shared layout.
- Contains navbar and logout button.
- Other pages extend this template.

### [core/templates/core/login.html](core/templates/core/login.html)

- Shows the login form.
- Uses Django’s built-in auth view.

### [core/templates/core/landing.html](core/templates/core/landing.html)

- Public home page.
- If user is logged in, dashboard buttons go straight to dashboard.
- If user is not logged in, buttons go to login first.

### [core/templates/core/dashboard.html](core/templates/core/dashboard.html)

- Shows enrolled courses and chart.
- Uses data passed from the `dashboard` view.
- Uses HTMX for table refresh.
- Uses JavaScript `fetch()` for chart refresh.

### [core/templates/core/partials/table_data.html](core/templates/core/partials/table_data.html)

- Only renders rows of the table.
- Used for partial live updates.

## Step 6: Settings Control App Behavior

Important settings are in [dashboard_project/settings.py](dashboard_project/settings.py).

The key ones for this flow:

- `INSTALLED_APPS`: turns on Django apps and your `core` app
- `MIDDLEWARE`: includes auth/session support
- `TEMPLATES`: allows Django to find template files
- `DATABASES`: uses SQLite
- `LOGIN_URL`: where Django sends users if a page needs login
- `LOGIN_REDIRECT_URL`: where users go after login
- `LOGOUT_REDIRECT_URL`: where users go after logout

This file controls how Django behaves globally.

## One Real Request Example

Example: user opens `/dashboard/`

1. Browser requests `/dashboard/`
2. Django enters [dashboard_project/urls.py](dashboard_project/urls.py)
3. Request is passed into [core/urls.py](core/urls.py)
4. `/dashboard/` matches `views.dashboard`
5. Django runs `dashboard(request)` in [core/views.py](core/views.py)
6. `@login_required` checks whether user is logged in
7. If not logged in, Django redirects to `/login/?next=/dashboard/`
8. If logged in, the view loads enrollments from [core/models.py](core/models.py)
9. The view prepares context data
10. Django renders [core/templates/core/dashboard.html](core/templates/core/dashboard.html)
11. Browser receives the final HTML page

Then after page load:

- HTMX calls `/dashboard/table/`
- JavaScript calls `/dashboard/chart-data/`
- Both refresh parts of the dashboard live

## Why This Structure Is Good

This separation is the core Django pattern:

- URLs decide where requests go
- Views decide what to do
- Models decide how data is stored
- Templates decide how data looks

That separation makes the app easier to maintain.

## Best Way To Understand It Fast

Open these files in this order:

1. [dashboard_project/urls.py](dashboard_project/urls.py)
2. [core/urls.py](core/urls.py)
3. [core/views.py](core/views.py)
4. [core/models.py](core/models.py)
5. [core/templates/core/dashboard.html](core/templates/core/dashboard.html)

That order matches how a request moves through the app.

## Next Step

If you want, the next useful explanation is the exact dashboard flow from clicking the button to live table and chart refresh.