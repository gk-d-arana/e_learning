from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *

User = get_user_model()


class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'id']


class SimpleInstructorSerializer(serializers.ModelSerializer):

    user = SimpleUserSerializer(User)
    
    class Meta:
        model = Instructor
        fields = ['user', 'profile_image', 'id', 'website_role']

class ParentCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ParentCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class SimpleCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'category_id', 'category_name', 'category_image',
            'category_description', 'students_count'
        ]

class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = [
            'topic_id', 'topic_name'
        ]


class RatingSerializer(serializers.ModelSerializer):
    instructor = SimpleInstructorSerializer(Instructor)
    class Meta:
        model = Rating
        fields = [
            "rating_id", "instructor", "rating_content", "rating_value", "created_at"
        ]



class SimpleRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = [
            "rating_id", "rating_content", "rating_value", "created_at"
        ]




class PaymentTypeSerializer(serializers.ModelSerializer):
    instructor = SimpleInstructorSerializer(Instructor)

    class Meta:
        model = PaymentType
        fields = "__all__"