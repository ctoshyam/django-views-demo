from django.test import TestCase, RequestFactory
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from my_school.models import Student
from django.urls import reverse
from my_school.serializers import StudentSerializer
from rest_framework import status

from my_school import views

# Create your tests here.

class StudentsApiTest(TestCase):  # Test the students api
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'shyam@gmail',
            'shyamsunder'
        )
        self.client.force_authenticate(self.user)
        #self.factory = APIRequestFactory()
        self.factory = RequestFactory()

    def test_retrieve_students_fb__list(self):  # Test retrieving a list of students

        Student.objects.create(first_name='Shyam', last_name='Sunder', age=31, gender='m ', date_created='2020-11-19')
        Student.objects.create(first_name='Girish', last_name='Marwah', age=31, gender='m', date_created='2020-11-19')

        res = self.client.get(reverse('students_fb_list'))

        students = Student.objects.all().order_by('-first_name')
        serializer = StudentSerializer(students, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # def test_retrieve_students_viewset(self):  # Test retrieving a list of students
    #
    #     Student.objects.create(first_name='Shyam', last_name='Sunder', age=31, gender='m ', date_created='2020-11-19')
    #     Student.objects.create(first_name='Girish', last_name='Marwah', age=31, gender='m', date_created='2020-11-19')
    #     retrieve_view = views.StudentViewSet.as_view(actions={'get': 'retrieve'})
    #     #Approach 2
    #     #request = self.factory.get('/api/v1/my_school/students')
    #     #res = retrieve_view(request)
    #
    #     # Aproach 1
    #     #res = self.client.get(reverse('students-viewset'))
    #
    #     #Approach 3
    #     factory = APIRequestFactory()
    #     view = views.StudentViewSet.as_view(actions={'get': 'retrieve'})  # <-- Changed line
    #     #cat = Cat(name="bob")
    #     #cat.save()
    #
    #     request = factory.get(reverse('students-viewset'))
    #     response = view(request)
    #
    #     students = Student.objects.all().order_by('-first_name')
    #     serializer = StudentSerializer(students, many=True)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, serializer.data)

    ### Test for GET ###
    def test_student_viewset(self):
        request = self.factory.get('/api/v1/my_school/students', {})
        #force_authenticate(request, user=self.user)
        response = views.StudentViewSet.as_view({'get': 'list'})(request)
        # Check if the first dog's name is Balto, like it is in the fixtures:
        #self.assertEqual(response.data['results'][0]['name'], 'Balto')
        # Check if you get a 200 back:
        #self.assertEqual(response.status_code, HTTPStatus.OK._value_)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ModelTestCase(TestCase):
    """This class defines the test suite for the student model."""

    def setUp(self):
        """Define the test client and other test variables."""

    def test_model_can_create_a_student(self):
        """Test the Student model can create a student."""
        old_count = Student.objects.count()
        # Student.objects.save()
        Student.objects.create(first_name='Shyam', last_name='Sunder', age=31, gender='m ', date_created='2020-11-19')
        new_count = Student.objects.count()
        self.assertNotEqual(old_count, new_count)
