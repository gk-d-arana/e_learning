from rest_framework import serializers
from .models import *
from extras.serializers import *

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'id']

class SimpleUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'id']




class InstructorSerializer(serializers.ModelSerializer):

    user = UserSerializer(User)
    
    class Meta:
        model = Instructor
        fields = "__all__"



class SimpleInstructorSerializer(serializers.ModelSerializer):

    user = SimpleUserSerializer(User)
    
    class Meta:
        model = Instructor
        fields = ["user", "profile_image", "id",
                  "job_role", "bio" ,"total_students", 
                  "total_balance" , "total_rate", "courses_count"]





"""
    Sometimes circular imports using nested serializers to solve it try this (Example) :
        try:
            from images.serializers import SimplifiedImageSerializer
        except ImportError:
            import sys
            SimplifiedImageSerializer = sys.modules[__package__ + '.SimplifiedImageSerializer']
"""


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"
        
class NoVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields =  [
            "video_id", "video_title", "video_duration"
        ]


class SectionSerializer(serializers.ModelSerializer):
    section_videos = VideoSerializer(Video, many=True)
    class Meta:
        model = Section
        fields = "__all__"



class SimpleSectionSerializerForLearning(serializers.ModelSerializer):
    section_videos = NoVideoSerializer(Video, many=True)
    class Meta:
        model = Section
        fields = "__all__"
        

class SectionSerializerForLearning(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = [
            "section_id",
            "section_name",
            "section_article"
        ]



class CourseLearningGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLearningGoal
        fields = "__all__"

class CourseRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRequirement
        fields = "__all__"
        
        
class CourseCouponSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Coupon
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    course_parent_category = ParentCategorySerializer(ParentCategory, many=True)
    course_category = CategorySerializer(Category, many=True)
    #course_topic = TopicSerializer(Topic)
    course_sections = SimpleSectionSerializerForLearning(Section, many=True)
    course_instructor = SimpleInstructorSerializer(Instructor )
    course_learning_goals = CourseLearningGoalSerializer(CourseLearningGoal, many=True)
    course_requirements = CourseRequirementSerializer(CourseRequirement, many=True)
    course_coupons = CourseCouponSerializer(Coupon, many=True)
    class Meta:
        model = Course
        fields = "__all__"


class HistoryCourseSerializer(serializers.ModelSerializer):
    course_parent_category = ParentCategorySerializer(ParentCategory, many=True)
    
    class Meta:
        model = Course
        fields = [
            "course_id" , "course_name", "course_parent_category"
        ]




class CartCourseSerializer(serializers.ModelSerializer):
    course_instructor = SimpleInstructorSerializer(Instructor)
    class Meta:
        model = Course
        fields = [
            'course_id', 'course_name', 'course_instructor', 'course_level', 'course_description',
            'course_rate', 'course_price', 'is_free', 'currency', 'course_videos_count', 'course_duration',
            'badges', 'course_subtitle', 'course_image', 'course_students', 'course_language'
        ]


class EnrollmentSerializer(serializers.ModelSerializer):
    user_enrolling = InstructorSerializer(Instructor)
    course = CartCourseSerializer(Course)
    class Meta:
        model = Enrollment
        fields = "__all__"


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model=Coupon
        fields = ["coupon_code"]
        
        
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"
        

class MultipleChoiceQuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(Answer, many=True)
    class Meta:
        model = MultipleChoiceQuestion
        fields = "__all__"
    
class EditorialQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditorialQuestion
        fields = "__all__"
        
        
class InstruCourseTestSerializer(serializers.ModelSerializer):
    multiple_choice_questions = MultipleChoiceQuestionSerializer(MultipleChoiceQuestion, many=True)
    editorial_questions = EditorialQuestionSerializer(EditorialQuestion, many=True)
    parent_category = ParentCategorySerializer(ParentCategory)
    category = CategorySerializer(Category)
    requirements = CourseRequirementSerializer(CourseRequirement, many=True)
    
    class Meta:
        model = CourseTest
        fields = "__all__"
        
        
class MyMultipleChoiceQuestionSerializer(serializers.ModelSerializer):
    question = MultipleChoiceQuestionSerializer(MultipleChoiceQuestion)
    answer = AnswerSerializer(Answer)
    class Meta:
        model = MyMultipleChoiceQuestion
        fields = "__all__"
        
class MyEditorialQuestionSerializer(serializers.ModelSerializer):
    question = EditorialQuestionSerializer(EditorialQuestion)
    class Meta:
        model = MyEditorialQuestion
        fields = "__all__"

class StudCourseTestSerializer(serializers.ModelSerializer):
    course_test = InstruCourseTestSerializer(CourseTest)
    my_multi_choice_ques_answers = MyMultipleChoiceQuestionSerializer(MyMultipleChoiceQuestion, many=True)
    my_edot_ques_answers = MyEditorialQuestionSerializer(MyEditorialQuestion, many=True)
    class Meta:
        model = MyTest
        fields = "__all__"
        


class MeetingStudentSerializer(serializers.ModelSerializer):
    instructor = InstructorSerializer(Instructor)
    class Meta:
        model = Meeting
        fields = [
            "meeting_id", "instructor", 'topic',
            'description', 'date', 'from_hour', 
            'to_hour', 'is_weekly', 'day'
        ]
        
        
        
class SimpleMeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = [
            "meeting_id", 'topic',
            'description', 'date', 'from_hour', 
            'to_hour', 'is_weekly', 'day'
        ]
        

class MeetingInstructorSerializer(serializers.ModelSerializer):
    students = InstructorSerializer(Instructor, many=True)
    class Meta:
        model = Meeting
        fields = "__all__"
        
        
class MyTestSerializer(serializers.ModelSerializer):
    instructor = SimpleInstructorSerializer(Instructor)
    course_test = InstruCourseTestSerializer(CourseTest)
    my_multi_choice_ques_answers = MyMultipleChoiceQuestionSerializer(MyMultipleChoiceQuestion, many=True)
    my_edot_ques_answers = MyEditorialQuestionSerializer(MyEditorialQuestion, many=True)
    
    class Meta:
        model = MyTest
        fields = "__all__"
        
        
        
class HistorySerializer(serializers.ModelSerializer):
    instructor = SimpleInstructorSerializer(Instructor)
    courses = HistoryCourseSerializer(Course, many=True)
    class Meta:
        model = MyHistory
        fields = "__all__"