from django.urls import path
from .views import *



urlpatterns = [
    path('courses/', CourseList.as_view()),
    path('tests/', TestsList.as_view()),
    path("course_by_selling_times/", course_filter),
    path("mobile_courses_by_selling_times/", mobile_courses_by_selling_times),
    path("course_by_top_rating/", course_by_top_rating),
    path('course_details/<str:course_id>/', course_details),
    path("create_meeting/", create_meeting, name="create_meeting"),
    path("course_details/", CourseDetailsView.as_view(), name="course_details"),
    #path("filter_courses/", FilterCourses.as_view(), name="filter_courses"),
    path('courses_by_level/', CoursesByLevel.as_view(), name="courses_by_level"),
    path('courses_by_rate/', CoursesByRate.as_view(), name="courses_by_rate"),
    path('search_courses/<str:id>/', SearchCourses.as_view(), name="search_courses"),
    path('course_tests/<str:course_id>/', CourseTests.as_view(), name="course_tests"),
    path('upload_video/', UploadVideo.as_view(), name="upload_video"),
    path('delete_course/', DeleteCourse.as_view(), name="delete_course"),    
    path('home_courses/', home_courses, name="home_courses"),
    path('section_managment/', SectionManagment.as_view(), name="section_managment"),
    path('course_managment/', CourseManagment.as_view(), name="course_managment"),
    path('course_test_managment/', CourseTestManagment.as_view(), name="course_test_managment"),
    path('wishlist_managment/', WishListManagment.as_view()),
    path('enrollment_managment/', EnrollmentManagment.as_view(), name="enrollment_managment"),
    path('enroll_in_live_meeting/', enroll_in_live_meeting, name="enroll_in_live_meeting"),
    path('enroll_in_single_meeting/', enroll_in_single_meeting, name="enroll_in_single_meeting"),
    path('my_meetings/', my_meetings),
    path('last_course/', last_course),
    path('add_live_meeting/', add_live_meeting),
    
]










