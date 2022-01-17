from courses.models import Course, Section, Video
from rest_framework import serializers
from django.contrib.auth import get_user_model
from extras.models import Category, Rating

from extras.serializers import CategorySerializer, RatingSerializer, SimpleRatingSerializer
from .models import *
from courses.serializers import CartCourseSerializer, CourseSerializer, SectionSerializer, SectionSerializerForLearning, VideoSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'id', 'date_joined']




class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']



class CertificateSeriailzer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = "__all__"

class CustomersListSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(User)
    class Meta:
        model = Instructor
        fields = ['user', 'id']



class AvailableForMeetingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AvailableForMeeting
        fields = [
            "id",
            "day", "availaibe_for_meetings_from_hour",
            "availaibe_for_meetings_to_hour", "note", "cost"
        ]

class InstructorSerializer(serializers.ModelSerializer):

    user = UserSerializer(User)
    favourite_category = CategorySerializer(Category)
    certificates = CertificateSeriailzer(Certificate, many=True)
    availaibe_for_meetings = AvailableForMeetingSerializer(AvailableForMeeting, many=True)
    class Meta:
        model = Instructor
        fields = "__all__"



class MyLearningVideoSerializer(serializers.ModelSerializer):
    video = VideoSerializer(Video)
    class Meta:
        model = MyLearningVideo
        fields = "__all__"    

class MyLearningSectionSerializer(serializers.ModelSerializer):
    section = SectionSerializerForLearning(Section)
    videos = MyLearningVideoSerializer(MyLearningVideo, many=True)
    
    class Meta:
        model = MyLearningSection
        fields = "__all__"    

class MyLearningCourseSerialzer(serializers.ModelSerializer):
    course = CartCourseSerializer(Course)
    sections= MyLearningSectionSerializer(MyLearningSection, many=True)
    rating = RatingSerializer(Rating)
    
    class Meta:
        model = MyLearningCourse
        fields = [
            "course", "sections", "rating", "progress"
        ]   
        
class MyLearningSimpleCourseSerialzer(serializers.ModelSerializer):
    course = CartCourseSerializer(Course)
    rating = SimpleRatingSerializer(Rating)
    class Meta:
        model = MyLearningCourse
        fields = [
            'course', 'rating', 'progress'
        ]  



class MyLearningSerializer(serializers.ModelSerializer):
    
    courses = MyLearningCourseSerialzer(MyLearningCourse, many=True)

    class Meta:
        model = MyLearning
        fields = ["courses"]


class MyLearningSimpleSerializer(serializers.ModelSerializer):
    
    courses = MyLearningSimpleCourseSerialzer(MyLearningCourse, many=True)

    class Meta:
        model = MyLearning
        fields = ["courses"]





class WishListSerializer(serializers.ModelSerializer):
    courses = CartCourseSerializer(Course, many=True)
    
    class Meta:
        model = WishList
        fields = ["courses"]
        
        
            
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"        
        
        
        

class OffDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = OffDay
        fields = "__all__"        
class ScheduleSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(Subject, many=True)
    off_days = OffDaySerializer(OffDay, many=True)


    class Meta:
        model = Schedule
        fields = [
            "subjects", "off_days" , "notes", 
            "start_hour", "end_hour", "number_of_subjects_per_day"
        ]