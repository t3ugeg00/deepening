from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class TestUserRegistrationView(TestCase):
    def test_url_exists_at_desired_location(self):
        res = self.client.get('/user/register/')

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'registration/register.html')
        self.assertContains(res, '</form>')

    def test_register_creates_and_redirects(self):
        url = reverse('register')
        res = self.client.post(url, {
            'username': 'testuser',
            'password1': 'Password67',
            'password2': 'Password67'
        })

        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertRedirects(res, reverse('login'))

    def test_register_fails_with_invalid_data(self):
        url = reverse('register')
        res = self.client.post(url, {
            'username': 'testuser',
            'password1': 'Password67',
            'password2': 'Password68'
        })

        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'registration/register.html')
        self.assertContains(res, 'error', status_code=200)

    def test_register_fails_with_duplicated_user(self):
        url = reverse('register')
        User.objects.create_user(username='testuser', password='Password67')

        res = self.client.post(url, {
            'username': 'testuser',
            'password1': 'Password67',
            'password2': 'Password67'
        })

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'registration/register.html')
        self.assertContains(res, 'error', status_code=200)
