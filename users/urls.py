from django.urls import path
from .views import *

urlpatterns = [
    path('register_instructor/', register_instructor, name="register_instructor"),
    path('login_instructor/', login_instructor, name="login_instructor"),
    path('manage_wishlist/', ManageWishListView.as_view(), name="manage_wishlist"),
    path('my_learnings/', MyLearningView.as_view(), name="my_learnings"),
    path('profile/', InstructorView.as_view(), name="profile"),
    path('instructor_profile/<str:instructor_id>/', InstructorDetailsView.as_view(), name="instructor_profile"),
    path('cp_instructor_profile/<str:instructor_id>/', ControlPanelInstructorDetailsView.as_view(), name="instructor_profile"),
    path('cp_student_profile/<str:instructor_id>/', ControlPanelStudentDetailsView.as_view(), name="instructor_profile"),
    path('update_account/', AccountView.as_view(), name="user_account"),
    path('update_profile_image/', update_profile_image, name="user_account"),
    path('check_course/<str:course_id>/', check_course, name="check_course"),
    path('check_test/<str:course_id>/', check_test, name="check_test"),
    path('instructors_by_rating/', InstructorsByRating.as_view(), name="instructors_by_rating"),
    path('api_all_students/', StudentsView.as_view(), name="api_all_students"), 
    path('close_account/', CloseAccount.as_view(), name="close_account"),
    #path('reset_password/', reset_password, name="reset_password"),
    path('reset_password/', reset_password),
    path('check_code/', check_code),
    path("check_is_admin/", check_is_admin, name="check_is_admin"),
    path('manage_study_program/', ManageStudyProgram.as_view()),
    path('manage_meeting_availibilty/', ManageMeetingAvailibilty.as_view()),
]
