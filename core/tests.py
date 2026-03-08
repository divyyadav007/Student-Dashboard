# get_user_model returns the active user model used by Django.
from django.contrib.auth import get_user_model

# TestCase gives us a temporary test database and a test client.
from django.test import TestCase

# reverse converts route names into real URLs.
from django.urls import reverse

# These models are used to prepare test data.
from .models import Course, Enrollment


# This test class verifies login redirects and dashboard behavior.
class AuthRoutingTests(TestCase):
	def test_dashboard_redirects_anonymous_users_to_login(self):
		# Request the dashboard without logging in first.
		response = self.client.get(reverse('dashboard'))

		# Anonymous users should be redirected to login with a next parameter.
		self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")

	def test_landing_shows_login_cta_for_anonymous_users(self):
		# Open the public landing page.
		response = self.client.get(reverse('landing'))
		# This is the login URL that should be used by both landing-page buttons.
		login_target = f'{reverse("login")}?next={reverse("dashboard")}'

		# The anonymous landing page should encourage login before dashboard access.
		self.assertContains(response, 'Login to View Dashboard')
		# The navbar call-to-action should still appear.
		self.assertContains(response, 'Get Started')
		# Both dashboard-related links should point to the same login target.
		self.assertContains(response, login_target, count=2)

	def test_dashboard_shows_logout_for_authenticated_users(self):
		# Create a user for the test.
		user = get_user_model().objects.create_user(username='student1', password='testpass123')
		# Log the user in without going through the form.
		self.client.force_login(user)

		# Open the dashboard as an authenticated user.
		response = self.client.get(reverse('dashboard'))

		# Logged-in users should see a logout button.
		self.assertContains(response, 'Logout')
		# The logout form should submit to the logout route.
		self.assertContains(response, f'action="{reverse("logout")}"')

	def test_chart_data_endpoint_returns_logged_in_user_courses(self):
		# Create a user and one course.
		user = get_user_model().objects.create_user(username='student2', password='testpass123')
		course = Course.objects.create(name='Data Structures', credits=4)
		# Enroll the user in the course.
		Enrollment.objects.create(user=user, course=course, grade='A')
		# Log the user in so the protected JSON endpoint can be accessed.
		self.client.force_login(user)

		# Request the chart data endpoint.
		response = self.client.get(reverse('dashboard_chart_data'))

		# The request should succeed.
		self.assertEqual(response.status_code, 200)
		# The JSON payload should match the enrolled course.
		self.assertJSONEqual(
			response.content,
			{'course_names': ['Data Structures'], 'course_credits': [4]},
		)

	def test_chart_data_endpoint_redirects_anonymous_users(self):
		# Request the chart endpoint without logging in.
		response = self.client.get(reverse('dashboard_chart_data'))

		# Anonymous users should be sent to login first.
		self.assertRedirects(
			response,
			f"{reverse('login')}?next={reverse('dashboard_chart_data')}",
		)
