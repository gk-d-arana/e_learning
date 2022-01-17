from django.urls import path
from .views import *

urlpatterns = [
    path("pcats_and_cats/", PCatsCats.as_view(), name="pcats_and_cats_and_topics"),
    path("top_pcats/", TopPcats.as_view(), name="top_pcats"),
    path("top_cats/", TopCats.as_view(), name="top_cats") ,
    path("payment_manager/", PaymentManager.as_view(), name="payment_manager"), 
    path("ratings_by_value/", TopRatings.as_view(), name="top_ratings"), 
    path("rating_manager/", RatingApiView.as_view(), name="rating_manager"), 
    path("course_ratings/<str:course_id>/", CourseRatingApiView.as_view(), name="course_ratings"), 
    path("category_manager/", CategoryManager.as_view(), name="category_manager"),
    path("parent_category_manager/", ParentCategoryManager.as_view(), name="category_manager")   
]