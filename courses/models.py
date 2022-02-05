from users.models import WEEK_DAYS, Instructor
import uuid
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Video(models.Model):
    video_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    video = models.FileField(upload_to="static/videos")
    video_title = models.CharField(max_length=1000, blank=True, null=True)
    video_duration = models.FloatField(default=0)

    def __str__(self):
        return self.video_title

class Section(models.Model):
    section_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    section_name = models.CharField(max_length=255)
    section_videos = models.ManyToManyField(Video, blank=True ,related_name="section_videos")
    section_article = models.TextField(default="",blank=True, null=True)
    

    def __str__(self):
        return "Section {}".format(self.section_name)

    def get_section_duration(self):
        section_total_duration = 0
        for video in self.section_videos.all():
            section_total_duration += video.video_duration
        return section_total_duration



COURSE_PRICE_CHOICES = (
    ("NONE", "NONE"),
    ("USD", "USD"),
    ("EURO", "EURO"),
)


COURSE_BAGDES_CHOICES = (
    ("Best Selling", "Best Selling"),
)

COURSE_LEVEL_CHOICES = (
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Expert', 'Expert'),

)


class Course(models.Model):
    course_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    course_name = models.CharField(max_length=255)
    course_subtitle = models.CharField(max_length=255 ,blank=True)
    course_description = models.TextField()
    course_instructor = models.ForeignKey(Instructor, on_delete=models.DO_NOTHING)
    course_rate = models.FloatField(default=0)
    course_review_count = models.PositiveIntegerField(default=0)
    course_students = models.PositiveIntegerField(default=0)
    course_sections = models.ManyToManyField(Section, blank=True, related_name="course_sections")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    is_free = models.BooleanField(default=False)
    course_price = models.PositiveIntegerField(default=0)
    currency = models.CharField(max_length=255, default="2", choices=COURSE_PRICE_CHOICES)
    course_topic = models.ForeignKey('extras.Topic', on_delete=models.DO_NOTHING, null=True)
    course_parent_category = models.ManyToManyField('extras.ParentCategory', blank=True)
    course_category = models.ManyToManyField('extras.Category', blank=True)
    badges = models.CharField(max_length=255, choices=COURSE_BAGDES_CHOICES, default="Best Selling")
    course_level = models.CharField(max_length=40, default="Beginner", choices=COURSE_LEVEL_CHOICES)
    course_image = models.FileField(upload_to="static/images", blank=True)
    course_promotional_video = models.FileField(upload_to="static/images", blank=True)
    course_message = models.TextField(blank=True)
    course_learning_goals = models.ManyToManyField('CourseLearningGoal', blank=True)
    course_requirements = models.ManyToManyField('CourseRequirement', blank=True)    
    course_language = models.CharField(max_length=255 ,default="English")
    course_videos_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    course_duration = models.PositiveIntegerField(default=0, blank=True, null=True)
    course_selling_times = models.PositiveIntegerField(default=0, blank=True, null=True)
    course_coupons = models.ManyToManyField('Coupon', blank=True, related_name="course_coupons")
    course_test = models.ForeignKey('CourseTest', on_delete=models.SET_NULL, null=True, blank=True, related_name="course_tests")
    course_tests_price = models.PositiveIntegerField(blank=True, null=True, default=25000)
    
    def __str__(self):
        return "Course {} For Instructor {}".format(self.course_name, self.course_instructor.user.username)
    

    def set_course_duration(self):
        course_total_duration = 0
        for section in self.course_sections.all():
            course_total_duration += section.get_section_duration()
        self.course_duration = course_total_duration
    
    
class CourseLearningGoal(models.Model):
    learning_goal = models.CharField(max_length=255, default="", blank=True, null=True)

    def __str__(self):
        return self.learning_goal


class CourseRequirement(models.Model):
    course_requirement = models.CharField(max_length=255, default="", blank=True, null=True)

    def __str__(self):
        return self.course_requirement


class Meeting(models.Model):
    meeting_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    instructor = models.ForeignKey(Instructor, related_name='meeting_instructor', on_delete=models.CASCADE)
    topic = models.CharField(max_length=255, blank=True, null=True)
    video = models.ForeignKey(Video, on_delete=models.DO_NOTHING, null=True, blank=True)
    description = models.TextField(default="", blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    from_hour = models.TimeField(blank=True, null=True)
    to_hour = models.TimeField(blank=True, null=True)
    is_weekly = models.BooleanField(default=False)
    students = models.ManyToManyField(Instructor, blank=True)
    meeting_cover_image = models.FileField(upload_to="static/images",blank=True, null=True)
    day = models.CharField(choices=WEEK_DAYS, max_length=20,blank=True, null=True)
    price = models.PositiveIntegerField(default=0, blank=True, null=True)

    

    
class Coupon(models.Model):
    coupon_code=models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_coupon",null=True)

    def __str__(self):
        return self.coupon_code
    


class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_enrolled")
    user_enrolling = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name="user_enrolling")
    
    def __str__(self):
        return "Enrollment {} For Instructor {}".format(self.course.course_name, self.user_enrolling.user.username)
    
    
    
class Answer(models.Model):
    value = models.TextField(default="", blank=True, null=True)
    is_correct = models.BooleanField(default=False,blank=True, null=True) 
    
class MultipleChoiceQuestion(models.Model):
    question = models.TextField(default="", blank=True, null=True) 
    answers = models.ManyToManyField(Answer, blank=True)
    
    
    
class EditorialQuestion(models.Model):
    question = models.TextField(default="", blank=True, null=True) 
    answer = models.TextField(default="", blank=True, null=True) 
    answer_as_image = models.FileField(upload_to="static/images", blank=True, null=True)
    

class MyMultipleChoiceQuestion(models.Model):
    question = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE, blank=True, null=True) 
    answer = models.ForeignKey(Answer, on_delete=models.SET_NULL,blank=True, null=True)
    is_correct = models.BooleanField(default=False,blank=True, null=True) 
    
    
class MyEditorialQuestion(models.Model):
    question = models.ForeignKey(EditorialQuestion, on_delete=models.CASCADE, blank=True, null=True) 
    answer = models.TextField(default="", blank=True, null=True)
    answer_as_image = models.FileField(upload_to="static/images", blank=True, null=True) 
    is_correct = models.BooleanField(default=False,blank=True, null=True) 



class CourseTest(models.Model):
    multiple_choice_questions = models.ManyToManyField(MultipleChoiceQuestion, blank=True)
    editorial_questions = models.ManyToManyField(EditorialQuestion, blank=True)
    price = models.PositiveIntegerField(default=0)
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=400, blank=True, null=True)
    description = models.TextField(default="",blank=True, null=True)
    parent_category = models.ForeignKey('extras.ParentCategory', blank=True, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey('extras.Category', blank=True, on_delete=models.SET_NULL, null=True)
    language = models.CharField(max_length=255 ,default="English")
    level = models.CharField(max_length=40, default="Beginner", choices=COURSE_LEVEL_CHOICES)
    test_goal = models.TextField(default="",blank=True, null=True)    
    requirements = models.ManyToManyField(CourseRequirement, blank=True)    
    test_for = models.TextField(default="",blank=True, null=True)
    
    
    
class MyTest(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL,blank=True, null=True)
    course_test = models.ForeignKey(CourseTest, on_delete=models.CASCADE)
    my_multi_choice_ques_answers = models.ManyToManyField(MyMultipleChoiceQuestion)
    my_edot_ques_answers = models.ManyToManyField(MyEditorialQuestion)
    total_correct = models.PositiveIntegerField(default=0, blank=True, null=True)
    
    
class MyHistory(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, blank=True)    
    
    
