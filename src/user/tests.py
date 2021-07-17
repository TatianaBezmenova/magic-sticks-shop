from django.test import TestCase
from django.urls import reverse
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, HttpResponseNotFound, \
    HttpResponseNotAllowed
from django.conf import settings

from .models import User


class UserViewsTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.user_bob = User.objects.create_user('bob', password='qwerty-123')
        self.user_eve = User.objects.create_user('eve', password='qwerty-123')
        self.superuser = User.objects.create_superuser('ann', password='qwerty-123')

    def tearDown(self):
        User.objects.all().delete()
        super().tearDown()

    def test_user_can_see_edit_page(self):
        # Bob
        bob_edit_url = reverse('user:edit', args=[self.user_bob.username])
        self.client.force_login(self.user_bob)
        response = self.client.get(bob_edit_url)
        self.assertEqual(response.status_code, HttpResponse.status_code,
                         'Проверка что пользователь может видить свою страницу редактирования')

        # Eve
        self.client.force_login(self.user_eve)
        response = self.client.get(bob_edit_url)
        self.assertEqual(response.status_code, HttpResponseForbidden.status_code,
                         'Проверка что Ева не может смотреть страницу Боба')

        # Anonymous
        self.client.logout()
        response = self.client.get(bob_edit_url)
        self.assertEqual(response.status_code, HttpResponseRedirect.status_code,
                         'Проверка, что анонимный пользователь направляется на страницу входа при попытке перейти '
                         'на страницу редактирования профиля')
        url_path, *_ = response.headers['location'].split('?')
        self.assertEqual(url_path, settings.LOGIN_URL,
                         'Проверка, что анонимный пользователь направляется на страницу входа при попытке перейти '
                         'на страницу редактирования профиля')

        # Superuser
        self.client.force_login(self.superuser)
        response = self.client.get(bob_edit_url)
        self.assertEqual(response.status_code, HttpResponse.status_code,
                         'Проверка что страница редактирования доступна суперпользователю')

    def test_user_can_edit_via_edit_page(self):
        bob_edit_url = reverse('user:edit', args=[self.user_bob.username])
        bob_detail_url = reverse('user:detail', args=[self.user_bob.username])

        correct_content = {
            'email': 'bob@localhost',
            'first_name': 'Bob',
            'last_name': 'Black'
        }

        # Bob
        self.client.force_login(self.user_bob)
        response = self.client.post(bob_edit_url, data=correct_content)
        self.assertEqual(response.status_code, HttpResponseRedirect.status_code,
                         'Проверка что пользователь может редактировать свою страницу')
        self.assertEqual(response.headers['location'], bob_detail_url,
                         'Проверка что после редактирования пользователь был перенаправлен')
        self.assertTrue(User.objects.filter(username='bob', email='bob@localhost').exists(),
                        'Проверка что данные пользователя изменились')

        # Eve
        self.client.force_login(self.user_eve)
        response = self.client.post(bob_edit_url, data=correct_content)
        self.assertEqual(response.status_code, HttpResponseForbidden.status_code,
                         'Проверка что Ева не может редактировать страницу Боба')

        # Anonymous
        self.client.logout()
        response = self.client.post(bob_edit_url, data=correct_content)
        self.assertEqual(response.status_code, HttpResponseRedirect.status_code,
                         'Проверка, что анонимный пользователь направляется на страницу входа при попытке перейти '
                         'на страницу редактирования профиля')
        url_path, *_ = response.headers['location'].split('?')
        self.assertEqual(url_path, settings.LOGIN_URL,
                         'Проверка, что анонимный пользователь направляется на страницу входа при попытке перейти '
                         'на страницу редактирования профиля')

        # Superuser
        self.client.force_login(self.superuser)
        response = self.client.post(bob_edit_url, data=correct_content)
        self.assertEqual(response.status_code, HttpResponseRedirect.status_code,
                         'Проверка что страница редактирования доступна суперпользователю')
        self.assertEqual(response.headers['location'], bob_detail_url)

    def test_user_can_see_login_page(self):
        login_url = reverse('user:login')
        self.client.logout()
        response = self.client.get(login_url)
        self.assertEqual(response.status_code, HttpResponse.status_code,
                         'Провекра что страница для входа доступна анон.пользователю')

        self.client.force_login(self.user_bob)
        response = self.client.get(login_url)
        self.assertEqual(response.status_code, HttpResponse.status_code,
                         'Провекра что страница для входа доступна Бобу')

    def test_update_form(self):
        bob_edit_url = reverse('user:edit', args=[self.user_bob.username])

        correct_content = {
            'email': 'bob@localhost',
            'first_name': 'Bob',
            'last_name': 'Black'
        }

        self.client.force_login(self.user_bob)
        response = self.client.post(bob_edit_url, data=correct_content)
        self.assertEqual(response.status_code, HttpResponseRedirect.status_code)

        correct_content['email'] = '12345'
        response = self.client.post(bob_edit_url, data=correct_content)
        self.assertEqual(response.status_code, HttpResponse.status_code)
        self.assertIn('Введите правильный адрес электронной почты', response.content.decode())


    def test_login(self):
        login_url = reverse('user:login')

        self.client.logout()
        response = self.client.post(login_url, data={'username': 'bob', 'password': 'qwerty-123'})
        self.assertEqual(response.status_code, HttpResponseRedirect.status_code,
                         'Проверка входа')

        self.assertEqual(response.headers['location'], settings.LOGIN_REDIRECT_URL,
                         'Проверка что редикект на верную страницу')

        self.client.logout()
        response = self.client.post(login_url, data={'username': 'bob', 'password': 'qwerty-1234'})
        self.assertEqual(response.status_code, HttpResponse.status_code, 'Проверка если ввели неверный логин/пароль')
        self.assertIn('Пожалуйста, введите правильные имя пользователя и пароль', response.content.decode())

    def test_logout(self):
        logout_url = reverse('user:logout')
        self.client.force_login(self.user_bob)
        self.assertIn('_auth_user_id', self.client.session, 'Проверка что пользователь залогинен')

        response = self.client.get(logout_url)
        self.assertEqual(response.status_code, HttpResponseNotAllowed.status_code)

        response = self.client.post(logout_url)
        self.assertEqual(response.status_code, HttpResponseRedirect.status_code)
        self.assertEqual(response.headers['location'], '/')
        self.assertNotIn('_auth_user_id', self.client.session, 'Проверка что пользователь разлогинен')
