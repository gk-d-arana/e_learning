from django.shortcuts import redirect, render
from extras.models import Rating
from courses.models import Course

def home_view(request):
    ratings = Rating.objects.all()
    courses = Course.objects.all()
    
    return render(request, 'home.html', {"ratings":ratings, "courses":courses})