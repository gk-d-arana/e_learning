from django.db import models
from django.contrib.auth import get_user_model



User = get_user_model()



INSTRUCTOR_BAGDES_CHOICES = (
    ("Best-Selling Instructor", "Best-Selling Instructor"),
)

INSTRUCTOR_WEBSITE_ROLL_CHOICES = (
    ('student', 'student'),
    ('instructor', 'instructor'),
)

    
WEEK_DAYS = (
    ('Sunday', 'Sunday'),
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday')
)


class Instructor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField()
    total_students = models.PositiveIntegerField(default=0)
    total_balance = models.PositiveIntegerField(default=0)
    total_rate= models.FloatField(default=0)
    badges = models.CharField(max_length=255, choices=INSTRUCTOR_BAGDES_CHOICES, default="1")
    profile_image = models.FileField(upload_to="static/images")
    age = models.PositiveIntegerField(default=0, blank=True, null=True)
    education = models.CharField(max_length=1500, blank=True, null=True, default="")
    favourite_category = models.ForeignKey('extras.Category', on_delete=models.SET_NULL ,blank=True, null=True)
    facebook_link = models.CharField(max_length=1000, blank=True, null=True, default="")
    job_role = models.TextField(default="", blank=True, null=True)
    certificates = models.ManyToManyField('Certificate', blank=True)
    courses_count = models.PositiveIntegerField(default=0)
    availaibe_for_meetings = models.ManyToManyField('AvailableForMeeting', blank=True,related_name="instructor_available_times") 
    phone_number = models.CharField(max_length=255,blank=True, null=True)
    website_role = models.CharField(max_length=20, choices=INSTRUCTOR_WEBSITE_ROLL_CHOICES,blank=True, null=True, default="student")
    my_tests_as_students = models.ManyToManyField('courses.MyTest', blank=True, related_name="my_tests_as_students")
    my_tests_as_instructor = models.ManyToManyField('courses.CourseTest', blank=True, related_name="my_tests_as_instructor")
    
    
    def __str__(self):
        return "Instructor {}".format(self.user.username)
    
    
class AvailableForMeeting(models.Model):
    day = models.CharField(max_length=255, choices=WEEK_DAYS,blank=True, null=True)
    availaibe_for_meetings_from_hour = models.TimeField(blank=True, null=True)
    availaibe_for_meetings_to_hour = models.TimeField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    cost = models.PositiveIntegerField(default=0, blank=True, null=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE,blank=True, null=True, related_name="instructor_available_time")


class MyLearningVideo(models.Model):
    video = models.ForeignKey('courses.Video', on_delete=models.SET_NULL, related_name="my_learning_video",blank=True, null=True)
    is_watched = models.BooleanField(default=False)

class MyLearningSection(models.Model):
    section = models.ForeignKey('courses.Section', on_delete=models.SET_NULL, related_name="my_learning_section",blank=True, null=True)
    videos = models.ManyToManyField(MyLearningVideo, blank=True)
    
class MyLearningCourse(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, related_name="my_learning_course",blank=True, null=True)
    sections = models.ManyToManyField(MyLearningSection, blank=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE,blank=True, null=True)
    progress = models.PositiveIntegerField(default=0,blank=True, null=True)
    rating = models.ForeignKey('extras.Rating', on_delete=models.SET_NULL,blank=True, null=True)
    
    def __str__(self):
        return f"MyLearningCourse {self.course.course_name}"    
    

class MyLearning(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    courses = models.ManyToManyField(MyLearningCourse, blank=True)
    
    def __str__(self):
        return f"My Learning For {self.instructor.user.username}"



class Certificate(models.Model):
    certificate_description = models.TextField(blank=True, null=True, default="")
    certificate_date = models.DateTimeField(blank=True, null=True)
    certificate_file = models.FileField(upload_to="static/files/", blank=True, null=True)
    


class WishList(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    courses = models.ManyToManyField('courses.Course', blank=True)



class CodesForPassReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="code_for_user")
    code = models.PositiveIntegerField(default=0000)
    
    
class Subject(models.Model):
    subject_name = models.CharField(max_length=255, default="", blank=True, null=True)
    lessons_count = models.PositiveIntegerField(default=0)
    not_studied_lessons_count = models.PositiveIntegerField(default=0)
    

class OffDay(models.Model):
    day = models.CharField(max_length=255, default="Sunday", choices=WEEK_DAYS)
    duration  = models.PositiveIntegerField(blank=True, null=True)
    note = models.TextField(default="", blank=True, null=True)

    
class Schedule(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, blank=True, null=True)
    subjects = models.ManyToManyField(Subject, blank=True)
    off_days = models.ManyToManyField(OffDay, blank=True)
    notes = models.TextField(default="", blank=True, null=True)
    start_hour = models.TimeField(blank=True, null=True)
    end_hour = models.TimeField(blank=True, null=True)
    number_of_subjects_per_day = models.PositiveIntegerField(blank=True, null=True, default=0)