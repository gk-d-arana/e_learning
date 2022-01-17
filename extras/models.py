from django.db import models
import uuid
from users.models import Instructor


class ParentCategory(models.Model):
    parent_category_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    parent_category_name = models.CharField(max_length=255)
    parent_category_image = models.FileField(upload_to='static/images',blank=True, null=True)
    parent_category_description = models.TextField(blank=True, null=True, default="")
    students_count = models.PositiveIntegerField(default=0)
    def __str__(self):  
         return "Parent Category {}".format(self.parent_category_name)
     
    class Meta:
          verbose_name_plural = "ParentCategories"


class Category(models.Model):
    category_id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False)
    category_name = models.CharField(max_length=255)
    parent_category = models.ForeignKey(ParentCategory, on_delete=models.CASCADE)
    category_image = models.FileField(upload_to='static/images',blank=True, null=True)
    category_description = models.TextField(blank=True, null=True, default="")
    students_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
         return "Category {}".format(self.category_name)
     
    class Meta:
          verbose_name_plural = "Categories"


class Topic(models.Model):
     topic_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
     topic_name = models.CharField(max_length=255)
     category = models.ForeignKey(Category, on_delete=models.CASCADE)

     def __str__(self):
         return "Topic {}".format(self.topic_name)
     

PROVIDER_CHOICES = (
    ("Visa", "Visa"),
    ("Master Card", "Master Card"),
    ("Zein Cash", "Zein Cash"),
)


class PaymentType(models.Model):
    payment_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    payment_provider =  models.CharField(
        max_length = 20,
        choices = PROVIDER_CHOICES,
        default = 'Visa'
        )
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    card_cvc = models.PositiveIntegerField(default=123)
    card_expire_date = models.DateField(default="1999-01-01")

    def __str__(self):
        return "Payment Type {} For Instructor {}".format(self.payment_provider, self.instructor.user.username)





class Rating(models.Model):
    rating_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    instructor = models.ForeignKey(Instructor , on_delete=models.CASCADE,blank=True, null=True)
    rating_content = models.TextField()
    rating_value = models.FloatField(default=0)
    course_rated = models.ForeignKey('courses.Course', on_delete=models.CASCADE,blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return "Rating For Instructor {} For Course {}".format(self.instructor.user.username, self.course_rated.course_name)
