from re import T
from django.core.checks import messages
from django.core.exceptions import PermissionDenied
from courses.models import CourseTest, Meeting
from rest_framework import mixins
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, get_object_or_404
from rest_framework.response import Response
from extras.models import Rating
from extras.serializers import RatingSerializer
from orders.models import CartItem, Cart
from users.models import Instructor
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .serializers import *
from courses.serializers import InstruCourseTestSerializer, SimpleMeetingSerializer
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
import json
User = get_user_model()

@api_view(['POST'])
def register_instructor(request):
    try:
        data = json.loads(request.body)
        first_name = data['first_name']
        last_name = data['last_name']
        phone_number = data['phone_number']
        username = data['username']
        password = data['password']
        email = data['email']
        #profile_image = request.FILES['profile_image']
        #print(request.FILES['profile_image'])
        #bio = request.POST['bio']            
    except Exception as e:  
        print(e)
        return Response({
            'message' : 'Pleas Pass Valid Data'
        }, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username=username)
        Token.objects.get(user=user)
        return Response({
            'message' : 'Username Already Used'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        user = User.objects.create(
            username=username, first_name=first_name, last_name=last_name, email=email,
        )
        user.save()
        user.set_password(password)
        user.save()
        token = Token.objects.create(user=user)
        token.save()
        instructor = Instructor.objects.create(user=user, phone_number=phone_number)
        instructor.save()
        return Response({
            'message' : 'Instructor Created Successfully',
            "token" : "{}".format(token)
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_instructor(request):
    try:
        data = json.loads(request.body)
        username = data['username']
        password = data['password']       
    except Exception as e:
        return Response({
            'message' : 'Pleas Pass Valid Data'
        }, status=status.HTTP_400_BAD_REQUEST)
    try:
        user=User.objects.get(username=username)
        if user.check_password(password):
            instructor = Instructor.objects.get(user=user) 
            token = Token.objects.get(user=user)
            return JsonResponse({
                'message' : 'success',
                'token' : "{}".format(token),
                'instructor' : InstructorSerializer(instructor).data
            })
        return Response({
            'message' : 'Pleas Pass Valid Credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        return Response({
            'message' : 'Pleas Pass Valid Credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)


class ManageWishListView(CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView):

    def create(self, request, *args, **kwargs):    
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            data = json.loads(request.body)
            course = Course.objects.get(course_id=data['course_id'])
        except Exception as e:
            return JsonResponse({
                'message' : 'Please Pass Valid Data'
            })
        wishlist, created = WishList.objects.get_or_create(instructor=instructor)
        wishlist.save()
        wishlist.courses.add(course)
        wishlist.save() 
        return JsonResponse({
            'message' : 'Course Added To WishList Successfully'
        })

    def retrieve(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        wishlist, created = WishList.objects.get_or_create(instructor=instructor)
        context = []
        for course in wishlist.courses.all():
            in_cart = False
            try:
                if CartItem.objects.get(course=course) in Cart.objects.get(instructor=instructor).cart_items.all() :
                    in_cart = True
            except Exception as e:
                pass
            context.append({
                'course' : CartCourseSerializer(course).data,
                'in_cart' : in_cart
            })
        return Response(context)

    def destroy(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            data = json.loads(request.body)
            course = Course.objects.get(course_id=data['course_id'])
        except Exception as e:
            return Response({
                'message' : 'Please Pass Valid Data'
            },status=status.HTTP_400_BAD_REQUEST)
        wishlist, created = WishList.objects.get_or_create(instructor=instructor)
        wishlist.save()
        wishlist.courses.remove(course)
        wishlist.save() 
        return JsonResponse({
            'message' : 'Course Removed From WishList Successfully'
        })



class ManageStudyProgram(CreateAPIView, RetrieveAPIView, UpdateAPIView):
    def create(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            data = json.loads(request.body)
            schedule = Schedule.objects.get_or_create(
                instructor = instructor)
            schedule.notes = data['notes'] 
            schedule.start_hour = data['start_hour']
            schedule.end_hour = data['end_hour']
            schedule.number_of_subjects_per_day = data["number_of_subjects_per_day"]
            schedule.save()
            for subject_data in data['subjects']:
                subject = Subject.objects.create(
                    subject_name = subject_data['subject_name'],
                    lessons_count = subject_data['lessons_count'],
                    not_studied_lessons_count = subject_data['not_studied_lessons_count']
                ) 
                subject.save()
                schedule.subjects.add(subject)
                schedule.save()
            for off_day_data in data['off_days']:
                off_day = OffDay.objects.create(
                    day = off_day_data['day'],
                    duration = off_day_data['duration'],
                    note = off_day_data['note']
                )
                off_day.save()
                schedule.off_days.add(off_day)
                schedule.save()
            
            return Response({'message' : 'success'}, status=status.HTTP_201_CREATED)       
        except Exception as e:
            print(e)
            return Response({'message' : 'Please Pass Valid Data'}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied  
        try:
            data = json.loads(request.body)
            schedule = Schedule.objects.get(instructor = instructor)
            schedule.notes = data['notes']
            schedule.start_hour = data['start_hour']
            schedule.end_hour = data['end_hour']
            schedule.number_of_subjects_per_day = data["number_of_subjects_per_day"]
            schedule.save()
            try: 
                for subject_data in data['subjects']:
                    subject = Subject.objects.get(id=subject_data['id'])
                    subject.subject_name = subject_data['subject_name']
                    subject.lessons_count = subject_data['lessons_count']
                    subject.not_studied_lessons_count = subject_data['not_studied_lessons_count']
                    subject.save()
            except Exception as e:
                print(e)
                pass
            try:
                for off_day_data in data['off_days']:
                    off_day = OffDay.objects.get(id=off_day_data['id'])
                    off_day.day = off_day_data['day']
                    off_day.duration = off_day_data['duration']
                    off_day.note = off_day_data['note']
                    off_day.save()
            except Exception as e:
                print(e)
                pass
            return Response({'message' : 'success'})       
        except Exception as e:
            print(e)
            return Response({'message' : 'Please Pass Valid Data'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    def get(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
            return Response(ScheduleSerializer(Schedule.objects.get(instructor=instructor)).data)
        except Exception as e:
            
            print(e)
            raise PermissionDenied





class MyLearningView(RetrieveAPIView):

    def retrieve(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        my_learning, created = MyLearning.objects.get_or_create(instructor=instructor)
        my_learning.save()
        my_learning = MyLearningSerializer(my_learning).data
        return Response(my_learning)

   

class InstructorView(RetrieveAPIView, UpdateAPIView):
    def retrieve(self, request, *args, **kwargs):
        try:
            return Response(InstructorSerializer(Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)).data)
        except:
            raise PermissionDenied



class InstructorDetailsView(RetrieveAPIView):
    def retrieve(self, request,instructor_id, *args, **kwargs):
        try:
            return Response({
                'instructor' : InstructorSerializer(Instructor.objects.get(id=instructor_id)).data,
                'courses' : CartCourseSerializer(Course.objects.filter(course_instructor=Instructor.objects.get(id=instructor_id))[:10], many=True).data,
                "ratings" : RatingSerializer(Rating.objects.filter(course_rated__course_instructor__id=instructor_id).order_by('-rating_value')[:10], many=True).data,
                'meetings' : SimpleMeetingSerializer(Meeting.objects.filter(instructor=Instructor.objects.get(id=instructor_id)), many=True).data,
            })
        except Exception as e:
            print(e)
            return Response({'message' : 'please pass valid instructor id'}, status=status.HTTP_404_NOT_FOUND)


class ControlPanelInstructorDetailsView(RetrieveAPIView):
    def retrieve(self, request,instructor_id, *args, **kwargs):
        try:
            return Response({   
                'instructor' : InstructorSerializer(Instructor.objects.get(id=instructor_id)).data,
                'courses' : CartCourseSerializer(Course.objects.filter(course_instructor=Instructor.objects.get(id=instructor_id))[:10], many=True).data,
                "tests" : InstruCourseTestSerializer(CourseTest.objects.filter(instructor__id=instructor_id)[:10], many=True).data
    
            })
        except Exception as e:
            print(e)
            return Response({'message' : 'please pass valid instructor id'}, status=status.HTTP_404_NOT_FOUND)

class ControlPanelStudentDetailsView(RetrieveAPIView):
    def retrieve(self, request,instructor_id, *args, **kwargs):
        try:
            my_learning, created = MyLearning.objects.get_or_create(instructor=Instructor.objects.get(id=instructor_id))
            my_learning.save()
            return Response({
                'instructor' : InstructorSerializer(Instructor.objects.get(id=instructor_id)).data,
                #'courses' : CartCourseSerializer(Course.objects.filter(course_instructor=Instructor.objects.get(id=instructor_id))[:10], many=True).data,
                #"tests" : InstruCourseTestSerializer(CourseTest.objects.filter(instructor__id=instructor_id)[:10], many=True).data,
                "my_learning" : MyLearningSimpleSerializer(my_learning).data
            })
        except Exception as e:
            print(e)
            return Response({'message' : 'please pass valid instructor id'}, status=status.HTTP_400_BAD_REQUEST)




class AccountView(UpdateAPIView):
    def update(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user) 
        except:
            raise PermissionDenied
        try:
            data = json.loads(request.body)
        except Exception as e:
            return Response({
                'message' : 'Please Pass Valid Data'
                }, status=status.HTTP_400_BAD_REQUEST)
            
        #update email
        try:
            email = data['email']
            instructor.user.email = email
        except Exception as e:
            pass
        
        #upate password
        try:
            password = data['password']
            new_password = data['new_password']
            if password:
                if instructor.user.check_password(password):
                    instructor.user.set_password(new_password)
                else:
                    return Response({
                        'message' : 'Wrong Password'
                    }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            pass
        
        #update name
        try:
            first_name = data['first_name']
            last_name = data['last_name']
            instructor.user.first_name = first_name
            instructor.user.last_name = last_name
        except Exception as e:
            pass
        
        #update age
        try:
            age = data['age']
            instructor.age = age            
        except Exception as e:
            pass
        
        #update education
        try:
            education = data['education']
            instructor.education = education            
        except Exception as e:
            pass
        
        #update favourite category
        try:
            favourite_category = Category.objects.get(category_id=data['favourite_category_id'])
            instructor.favourite_category = favourite_category            
        except Exception as e:
            pass
        
        #update job role
        try:
            job_role = data['job_role']
            instructor.job_role = job_role            
        except Exception as e:
            pass
        
        
        instructor.save()
        instructor.user.save()
        return JsonResponse({
            'message' : 'Profile Edited Successfully'
        })




@api_view(['PUT'])
def update_profile_image(request):
    try:
        instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user) 
    except:
        raise PermissionDenied
    try:
        profile_image = request.data['profile_image']
        instructor.profile_image = profile_image
        instructor.save()
        return Response({'message' : 'Updated Profile Image'})
    except Exception as e:
        return Response({
            'message' : 'Please Pass Valid Data'
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def check_course(request, course_id):
    try:
        instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user) 
    except:
        raise PermissionDenied
    try:
        my_learning_course = MyLearningCourse.objects.get(course = Course.objects.get(course_id=course_id))
        in_my_learning = False
        my_learning, created = MyLearning.objects.get_or_create(instructor=instructor)
        my_learning.save()        
        if my_learning_course in my_learning.courses.all():
            in_my_learning = True
        
        ratings = Rating.objects.filter(course_rated=Course.objects.get(course_id=course_id))
        return Response({
            "course" : MyLearningCourseSerialzer(my_learning_course).data,
            "ratings" :   RatingSerializer(ratings, many=True).data,
            "in_my_learning" : in_my_learning
        })
    except Exception as e:
        return Response({'message' : 'Please Pass Valid Course Id'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def check_test(request, course_id):
    try:
        instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user) 
    except:
        raise PermissionDenied
    try:
        my_learning_course = MyLearningCourse.objects.get(course = Course.objects.get(course_id=course_id))
        in_my_learning = False
        my_learning, created = MyLearning.objects.get_or_create(instructor=instructor)
        my_learning.save()        
        if my_learning_course in my_learning.courses.all():
            in_my_learning = True
        
        ratings = Rating.objects.filter(course_rated=Course.objects.get(course_id=course_id))
        return Response({
            "course" : MyLearningCourseSerialzer(my_learning_course).data,
            "in_my_learning" : in_my_learning
        })
    except Exception as e:
        return Response({'message' : 'Please Pass Valid Course Id'}, status=status.HTTP_404_NOT_FOUND)


class InstructorsByRating(ListAPIView):
    def list(self, request, *args, **kwargs):
        instructors = Instructor.objects.filter(courses_count__gte=1).order_by('-total_rate')
        return Response(InstructorSerializer(instructors, many=True).data)



class StudentsView(ListAPIView):
    def list(self, request, *args, **kwargs):
        queryset = Instructor.objects.filter(courses_count=0).order_by('-total_rate')
        page = self.paginate_queryset(queryset)
        serializer = InstructorSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class CloseAccount(DestroyAPIView):
    def destroy(self, request, *args, **kwargs):
        try:
            user = Token.objects.get(key=request.headers['Authorization']).user
            user.delete()
            return JsonResponse({
                'message' : 'User Deleted Successfully'
            })
        except Exception as e:
            raise PermissionDenied



@api_view(['POST', 'PUT'])
def reset_password(request):
    data = json.loads(request.body)
    if request.method == "PUT":
        try:
            user=Token.objects.get(key=request.headers['Authorization']).user
        except Exception as e:
            raise PermissionDenied
        try:
            new_password = data['new_password']
            user.set_password(new_password)
            user.save()
            return JsonResponse({
                "message" : "Updated Successfully"
            })
        except Exception as e:
            return Response({"message":"Please Pass New Password"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        email = data['email']
    except Exception as e:
            return Response({"message":"Please Pass Valid Data"}, status=status.HTTP_400_BAD_REQUEST)
    try:    
        user = User.objects.filter(email=email).first()
    except Exception as e:
            return Response({"message":"This Email Did Not Match Our Records"}, status=status.HTTP_400_BAD_REQUEST)
    import random
    string_ints = [str(int) for int in random.sample(range(0, 9), 4)]
    code  = ''.join(string_ints)
    new_code = CodesForPassReset.objects.create(user=user, code=code)
    new_code.save()
    subject = 'Your Request To Reset Your Password'
    message = f'Hi Your Confirmation Code Is {code}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return JsonResponse({
        'message' : 'Sent Email Successfully',
        'id' : new_code.id
    })




@api_view(['POST'])
def check_code(request):
    try:
        data = json.loads(request.body)
        code = CodesForPassReset.objects.filter(id=data['code_id']).last()
        sent_code = int(data['sent_code'])
        if code.code == sent_code:
            return JsonResponse({
            'message' : 'success',
            'token' : "{}".format(Token.objects.get(user=code.user).key)
        })
        else:
            return Response({
                'message' : 'fail',
            }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
            return Response({"message":"Please Pass Valid Data"}, status=status.HTTP_400_BAD_REQUEST)



def check_is_admin(request):
    try:
        user=Token.objects.get(key=request.headers['Authorization']).user
        if user.is_staff:
            return JsonResponse({'isAdmin' : True})        
        else:
            raise PermissionDenied
    except Exception as e:
            raise PermissionDenied



class ManageMeetingAvailibilty(CreateAPIView, RetrieveAPIView):
    def create(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            data = json.loads(request.body)
            av = AvailableForMeeting.objects.create(
                instructor = instructor,
                day = data['day'],
                availaibe_for_meetings_from_hour = data['availaibe_for_meetings_from_hour'],
                availaibe_for_meetings_to_hour = data['availaibe_for_meetings_to_hour'],
                note = data['note'], cost = data['cost']
            )
            av.save()
            instructor.availaibe_for_meetings.add(av)
            instructor.save()
            return Response({'message' : 'success'})
        except Exception as e:
            print(e)
            return Response({"message":"Please Pass Valid Data"}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self ,request,  *args, **kwargs):
        try:
            instructor = get_object_or_404(Instructor,id=request.GET['instructor_id'])
        except Exception as e:
            print(e)
            return Response({'message' : 'Please Pass Valid Id'}, status=status.HTTP_404_NOT_FOUND)
        context = [
            {"Sunday":[]},
            {"Monday":[]},
            {"Tuesday":[]},
            {"Wednesday":[]}, 
            {"Thursday":[]}, 
            {"Friday":[]}, 
            {"Saturday":[]}, 
        ]
        for meeting in instructor.availaibe_for_meetings.all():
            if meeting.day == "Sunday":
                context[0]['Sunday'].append(AvailableForMeetingSerializer(meeting).data)
            elif meeting.day == "Monday":
                context[1]['Monday'].append(AvailableForMeetingSerializer(meeting).data)
            elif meeting.day == "Tuesday":
                context[2]['Tuesday'].append(AvailableForMeetingSerializer(meeting).data)
            elif meeting.day == "Wednesday":
                context[3]['Wednesday'].append(AvailableForMeetingSerializer(meeting).data)
            elif meeting.day == "Thursday":
                context[4]['Thursday'].append(AvailableForMeetingSerializer(meeting).data)
            elif meeting.day == "Friday":
                context[5]['Friday'].append(AvailableForMeetingSerializer(meeting).data)
            elif meeting.day == "Saturday":
                context[6]['Saturday'].append(AvailableForMeetingSerializer(meeting).data)                
        return Response(context)
        
        
        
        
        
        
        