from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from publications.models import Publication
from users.models import User


# Create your tests here.

class ViewsTestCase(TestCase):
    def test_index_loads_properly(self):
        """The index page loads properly"""
        response = self.client.get('http://127.0.0.1:8000/login/')
        self.assertEqual(response.status_code, 200)


class TestCase(TestCase):
    def test_index_loads_properly(self):
        """The index page loads properly"""
        response = self.client.get('http://127.0.0.1:8000/login/')
        self.assertEqual(response.status_code, 200)


class PublicationTestCase(TestCase):
    def setUp(self) -> None:
        self.url = '/'
        self.user = User.objects.create(
            email='test@user.ru',
            phone='+79171717171',
            password='0000'
        )
        self.user2 = User.objects.create(
            email='test@user2.ru',
            phone='+79170000000',
            password='1111'
        )
        self.publication = Publication.objects.create(
            owner=self.user,
            header='first',
            content='content'
        )


        self.data = {
            'owner': self.user,
            'header': 'second',
            # 'course': self.course,
            'content': 'content2',
            'quantity_of_views': '2'
        }

        self.publication2 = Publication.objects.create(**self.data)
        # self.client.force_authenticate(user=self.user)
        # def test_create_lesson(self):
        #     data = {
        #         'name': 'testT',
        #         'description': 'test',
        #         'course': self.course.pk,
        #         'owner': self.user.pk
        #     }
        #     lesson_create_url = reverse('course_app:lesson-create')
        #     response = self.client.post(lesson_create_url, data)
        #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #     self.assertEqual(Lesson.objects.all().count(), 2)