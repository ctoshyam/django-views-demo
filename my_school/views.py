from my_school.serializers import StudentSerializer
from rest_framework.decorators import api_view
from my_school.models import Student

from rest_framework.views import APIView
from rest_framework import status, permissions, generics, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import mixins

from django.views.decorators.csrf import csrf_exempt


# Create your views here.
######################################
# Function based api views -
######################################


@csrf_exempt
@api_view(['POST'])
def students_create(request):
    permission_classes = [permissions.AllowAny]

    stu_serializer = StudentSerializer(data=request.data)
    stu_serializer.is_valid(raise_exception=True)
    stu_serializer.save()

    return Response(stu_serializer.data, status=status.HTTP_201_CREATED)


######################################
# Function based api views - https://www.django-rest-framework.org/tutorial/2-requests-and-responses/
######################################


@api_view(['GET', 'POST'])
def students_list(request):
    """
    List all code students, or create a new student.
    """
    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def student_detail(request, pk):
    """
    Retrieve, update or delete a code student.
    """
    try:
        snippet = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudentSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = StudentSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


######################################
# Class based api views - https://www.django-rest-framework.org/tutorial/3-class-based-views/
######################################


class StudentList(APIView):
    """
    List all students, or create a new student.
    """

    def get(self, request, format=None):
        snippets = Student.objects.all()
        serializer = StudentSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetail(APIView):
    """
    Retrieve, update or delete a student instance.
    """

    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = StudentSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = StudentSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

######################################
# Class based mixin api views - https://www.django-rest-framework.org/tutorial/3-class-based-views/#using-mixins
######################################

class MixinStudentList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class MixinStudentDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# ##################################### Class based generic api views -
# https://www.django-rest-framework.org/tutorial/3-class-based-views/#using-generic-class-based-views
# #####################################


class GStudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class GStudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

# NEXT
# https://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/

######################################
# Class based api views - https://medium.com/djangotube/django-rest-api-curd-example-61c3a29b22ed
######################################


class StudentsAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        stu_serializers = StudentSerializer(data=request.data)
        stu_serializers.is_valid(raise_exception=True)
        stu_serializers.save()
        return Response(stu_serializers.data, status=status.HTTP_201_CREATED)

    def get(self, request, pk=None, format=None):
        if pk:
            student = get_object_or_404(Student, id=pk)
            stu_serializer = StudentSerializer(student)
            return Response(stu_serializer.data, status=status.HTTP_200_OK)
        else:
            students_qs = Student.objects.all()
            stu_serializer = StudentSerializer(students_qs, many=True)
            return Response(stu_serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None, format=None):
        student = get_object_or_404(Student, id=pk)
        stu_serializer = StudentSerializer(instance=student, data=request.data)
        stu_serializer.is_valid(raise_exception=True)
        stu_serializer.save()
        return Response(stu_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None, format=None):
        student = get_object_or_404(Student, id=pk)
        student.delete()
        return Response({'msg': 'done'}, status=status.HTTP_204_NO_CONTENT)


######################################
# Generic Class based api views
######################################


class StudentsListAPIView(generics.ListAPIView):
    """This endpoint lists all of the available todos from the database"""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentsCreateAPIView(generics.CreateAPIView):
    """This endpoint allows for creation of a student"""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentsUpdateAPIView(generics.UpdateAPIView):
    """This endpoint allows for updating a specific student by passing in the id of student to update"""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentsDeleteAPIView(generics.DestroyAPIView):
    """This endpoint allows for deletion of a specific student from the database"""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

######################################
# Viewset Class based api views
######################################


class StudentViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        students_qs = Student.objects.all()
        stu_serializer = StudentSerializer(students_qs, many=True)
        return Response(stu_serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        stu_serializer = StudentSerializer(data=request.data)
        stu_serializer.is_valid(raise_exception=True)
        stu_serializer.save()
        return Response(stu_serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        student = get_object_or_404(Student, id=pk)
        stu_serializer = StudentSerializer(student)
        return Response(stu_serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, ):
        student = get_object_or_404(Student, id=pk)
        stu_serializer = StudentSerializer(instance=student, data=request.data)
        stu_serializer.is_valid(raise_exception=True)
        stu_serializer.save()
        return Response(stu_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None, ):
        student = get_object_or_404(Student, id=pk)
        student.delete()
        return Response({'msg': 'done'}, status=status.HTTP_204_NO_CONTENT)

######################################
# ModelViewSet Class based api views
######################################


class StudentModelViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.AllowAny]
