from django.urls import path
from my_school import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'students', views.StudentViewSet, basename="students-viewset")
router.register(r'model_students', views.StudentModelViewSet, basename="model_students")
# urlpatterns = router.urls

urlpatterns = [
    # path("students/fb/create/", views.students_create(),name="students_f_create"),
    path('students/cb/create/', views.StudentsAPIView.as_view(), name="students_c_create"),
    path('students/cb/list/', views.StudentsAPIView.as_view(), name="students_c_list"),
    path('students/cb/get/<int:pk>/', views.StudentsAPIView.as_view(), name="students_c_get"),
    path('students/cb/update/<int:pk>/', views.StudentsAPIView.as_view(), name="students_c_update"),
    path('students/cb/delete/<int:pk>/', views.StudentsAPIView.as_view(), name="students_c_delete"),
    path('students/gcb/create/', views.StudentsCreateAPIView.as_view(), name="students_g_create"),
    path('students/gcb/list/', views.StudentsListAPIView.as_view(), name="students_g_list"),
    # path('students/gcb/get/<int:pk>/', views.StudentsGETAPIView.as_view(), name="students_g_get"),
    path('students/gcb/update/<int:pk>/', views.StudentsUpdateAPIView.as_view(), name="students_g_update"),
    path('students/gcb/delete/<int:pk>/', views.StudentsDeleteAPIView.as_view(), name="students_g_delete"),
    path('students/fb/', views.students_list, name="students_fb_list"),
    path('students/fb/<int:pk>/', views.student_detail, name="student_fb_detail"),
    path('students/cb/', views.StudentList.as_view(), name="students_cb_list"),
    path('students/cb/<int:pk>/', views.StudentDetail.as_view(), name="student_cb_detail"),
    path('students/gcb/', views.GStudentList.as_view(), name="students_gcb_list"),
    path('students/gcb/<int:pk>/', views.GStudentDetail.as_view(), name="student_gcb_detail"),
    path('students/mcb/', views.MixinStudentList.as_view(), name="students_mcb_list"),
    path('students/mcb/<int:pk>/', views.MixinStudentDetail.as_view(), name="student_mcb_detail"),

] + router.urls