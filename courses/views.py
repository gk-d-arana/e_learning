import json
from extras.serializers import ParentCategorySerializer, RatingSerializer
from extras.models import Category, ParentCategory, Rating, Topic
from rest_framework.response import Response
from courses.serializers import CartCourseSerializer, CourseSerializer, EnrollmentSerializer, InstruCourseTestSerializer, MeetingInstructorSerializer, MeetingStudentSerializer
from django.http.response import JsonResponse
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from courses.models import *
from django.core.exceptions import PermissionDenied
from users.models import AvailableForMeeting, Instructor, MyLearning, MyLearningCourse, WishList
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.db.models.expressions import RawSQL
from orders.models import Cart, CartItem, Wallet
from users.serializers import WishListSerializer
#from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework import status


@api_view(['POST'])
def create_meeting(request):
    try:
        instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
    except Exception as e:
        raise PermissionDenied
    meeting = Meeting.objects.create(instructor=instructor)
    meeting.save()
    resp = {
        'message' : 'success',
        'meeting_id' : meeting.meeting_id
    }
    return JsonResponse(resp)



class SearchCourses(ListAPIView):
    def get(self, request, *args, **kwargs):
        courses = []
        try:
            parent_category = ParentCategory.objects.get(parent_category_id=kwargs['id'])
            courses = Course.objects.filter(course_parent_category=parent_category)
        except Exception as e:
            try:
                category = Category.objects.get(category_id=kwargs['id'])
                courses = Course.objects.filter(course_category=category)
            except Exception as e:
                try:
                    courses = Course.objects.filter(course_name__contains=kwargs['id'])          
                except Exception as e:
                    pass
        return Response(CourseSerializer(courses, many=True).data)
        #try:
        #    courses = Course.objects.filter(course_topic__id=kwargs['id'])
        #except Exception as e:
        #    pass
        




    
@api_view(['GET'])
def course_details(request, course_id):
    course = Course.objects.get(course_id=course_id)
    in_wishlist = False
    in_cart = False
    in_my_learning = False
    try:
        my_learning_course = MyLearningCourse.objects.get(course=course)
        my_learning, created =MyLearning.objects.get_or_create(instructor=Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user))
        my_learning.save()
        if my_learning_course in my_learning.courses.all():
            in_my_learning = True
    except Exception as e:
        pass
    try:
        wishlist, created =WishList.objects.get_or_create(instructor=Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user))
        wishlist.save()
        cart, created =Cart.objects.get_or_create(cart_owner=Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user))
        cart.save()
        if course in wishlist.courses.all():
                in_wishlist = True
        try:
            cart_item = CartItem.objects.get(course=course)
            print(cart.cart_items.all(), cart_item)
            if cart_item in cart.cart_items.all():
                in_cart = True
        except Exception as e:
            print(e)
            pass
    except Exception as e:
        print(e)
        pass
    res = {
        "in_wishlist" : in_wishlist,
        "in_cart" : in_cart,
        "in_my_learning": in_my_learning,
        "course" : CourseSerializer(course).data
    }        
    return Response(res)

@api_view(['GET'])
def home_courses(request):
    queryset = ParentCategory.objects.all().order_by('?')[:5]
    context = []
    for pcat in queryset:
        context.append({
            "parent_category" : ParentCategorySerializer(pcat).data,
            "courses" :  CourseSerializer(Course.objects.filter(course_parent_category=pcat)[:12], many=True).data
        })
    return Response(context)




class CourseList(ListAPIView):
    queryset = Course.objects.all()
    def list(self, request, *args, **kwargs):
        queryset = Course.objects.all()
        page = self.paginate_queryset(queryset)
        serializer = CourseSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

class TestsList(ListAPIView):
    queryset = CourseTest.objects.all()
    def list(self, request, *args, **kwargs):
        queryset = CourseTest.objects.all()
        page = self.paginate_queryset(queryset)
        serializer = InstruCourseTestSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)




class CourseDetailsView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        try:
            _course = Course.objects.get(course_id=request.POST['course_id'])
            course = CourseSerializer(_course).data
        except Exception as e:
            return JsonResponse({
                'message' : 'Please Pass Valid Course Id'
            })
        ratings = RatingSerializer(Rating.objects.filter(course_rated=_course), many=True).data
        return JsonResponse({
            'course' : course,
            'ratings' : ratings
        })


class FilterCourses(ListAPIView):
    def list(self, request, *args, **kwargs):
        """         try:
            filter_query = request.POST['filter_query']
        except Exception as e:
            return JsonResponse({
                'message' : 'Pleas Pass The Query'
            })
        
        queryset = Course.objects.raw("{}".format(filter_query))
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data) """
        try:
            return Response(
                CartCourseSerializer(Course.objects.filter(course_topic=Topic.objects.get(topic_id=request.POST['topic_id'])),
                many=True
                ).data
            )
        except Exception as e:
              pass
        try:
            return Response(
                CartCourseSerializer(Course.objects.filter(course_parent_category=ParentCategory.objects.get(parent_category_id=request.POST['parent_category_id'])),
                many=True
                ).data
            )
        except Exception as e:
            pass
        try:
            return Response(
                CartCourseSerializer(Course.objects.filter(course_category=Category.objects.get(category_id=request.POST['category_id'])),
                many=True
                ).data
            )
        except Exception as e:
            pass
        
        return Response({
            'message' : 'please Pass Valid Data'
        }, status=status.HTTP_400_BAD_REQUEST)            



class CoursesByLevel(ListAPIView):
    def list(self, request, *args, **kwargs):
        try:
            course_level = request.POST['course_level']
            return Response(CourseSerializer(Course.objects.filter(course_level=course_level), many=True).data)
        except Exception as e:
            return JsonResponse({
                'message' : 'Please Pass Valid Course Level'
            })

class CoursesByRate(ListAPIView):
    def list(self, request, *args, **kwargs):
        try:
            course_rate = float(request.POST['course_rate'])
            return Response(CourseSerializer(Course.objects.filter(course_rate=course_rate), many=True).data)
        except Exception as e:
            return JsonResponse({
                'message' : 'Please Pass Valid Course Rate'
            })

@api_view(['GET'])
def course_by_top_rating(request):
    return Response(CartCourseSerializer(Course.objects.all().order_by('-course_rate')[:12], many=True).data)


@api_view(['GET'])
def mobile_courses_by_selling_times(request):
    return Response(CartCourseSerializer(Course.objects.all().order_by('-course_price')[:12], many=True).data)



@api_view(['GET'])
def course_filter(request, *args, **kwargs):        
    courses = Course.objects.all().order_by('-course_selling_times')[:5]
    data = []
    for course in courses:
        try:
            in_wishlist = False
            in_my_learning = False
            wishlist, created =WishList.objects.get_or_create(instructor=Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user))
            wishlist.save()
            my_learning, created =MyLearning.objects.get_or_create(instructor=Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user))
            my_learning.save()
            try:
                if course in my_learning.courses.all():
                    in_my_learning = True
                if course in wishlist.courses.all():
                    in_wishlist = True
            except Exception as e:
                pass
        except Exception as e:
            pass
        data.append({
            "in_wishlist" : in_wishlist,
            "in_my_learning" : in_my_learning,
            "course" : CourseSerializer(course).data
        })
    return Response(data)


class DeleteCourse(DestroyAPIView):
    def destroy(self, request, *args, **kwargs):
        try:
            user=Token.objects.get(key=request.headers['Authorization']).user
            if user.is_staff:
                instructor = Instructor.objects.get(user=user)
            else:
                raise PermissionDenied
        except Exception as e:
            raise PermissionDenied
        try:
            data = json.loads(request.body)
            course = Course.objects.get(course_id=data['course_id'])
            course.delete()
            return Response({'message' : 'success'})
        except Exception as e:
            print(e)
            return Response({'message' : 'Please Pass Valid Data'}, status=status.HTTP_400_BAD_REQUEST)


class UploadVideo(CreateAPIView):

    def create(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            video = request.FILES['video']
            video_duration = float(request.POST['video_duration'])
            new_video, created = Video.objects.get_or_create(video=video, video_duration=video_duration)
            new_video.save()
            return JsonResponse({
                'video_id' : new_video.video_id
            })
        except Exception as e:
            return JsonResponse({
                'message' : 'Please Pass Valid Data'
            })


class SectionManagment(CreateAPIView, DestroyAPIView, UpdateAPIView):

    def create(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            section_name = request.POST['section_name']
            section = Section.objects.create(section_name=section_name)
            section.save()
            return JsonResponse({
                'section_id' : section.section_id
            })
        except Exception as e:
            return JsonResponse({
                'message' : 'Please Pass Valid Data'
            })
            
    def update(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            section_id = request.POST['section_id']
            section = Section.objects.get(section_id=section_id)
            videos = request.POST.getlist('videos')
            for video_id in videos:
                section.section_videos.add(Video.objects.get(video_id=video_id))
            section.save()
            return JsonResponse({
                'message' : 'Videos Added Successfully'
            })
        except Exception as e:
            return JsonResponse({
                'message' : 'Please Pass Valid Data'
            })



class CourseManagment(CreateAPIView, DestroyAPIView, UpdateAPIView):

    def create(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        is_free=False
        try:
            course_price = int(request.POST['course_price'])
            currency = request.POST['currency']
        except Exception as e:
            is_free=True
            course_price=0
            currency="1"

        try:
            courses_name = request.POST['courses_name']
            course_description = request.POST['course_description']
            course_topic = request.POST['course_topic']
            course_parent_category = request.POST['course_parent_category']
            course_category = request.POST['course_category']
            course_level = request.POST['course_level']
            course_image = request.FILES['course_image']
            course_promotional_video = request.FILES['course_promotional_video']
            course_requirements = request.POST['course_requirements']
            course_message = request.POST['course_message']
            course_language = request.POST['course_language']
            course_subtitle = request.POST['course_subtitle']
            course = Course.objects.create(
                courses_name=courses_name, course_description=course_description,
                is_free=is_free ,course_topic=Topic.objects.get(topic_id=course_topic),
                course_parent_category=ParentCategory.objects.get(parent_category_id=course_parent_category),
                course_category=Category.objects.get(category_id=course_category), course_level=course_level,
                course_instructor=instructor, course_price=course_price, currency=currency,
                course_image=course_image, course_promotional_video=course_promotional_video,
                course_message=course_message, course_requirements=course_requirements,
                course_language=course_language, course_subtitle=course_subtitle
            )
            course.save()
            try:
                coupon_code = request.POST['coupon_code']
                coupon = Coupon.objects.create(course=course, coupon_code=coupon_code)
                coupon.save()
            except Exception as e:
                pass
            course.set_course_duration()
            course.save()
            return JsonResponse({
                'course_id' : course.course_id
            })
        except Exception as e:
            return JsonResponse({
                'message' : 'Please Pass Valid Data'
            })
            
    def update(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            course_id = request.POST['course_id']
            course = Course.objects.get(course_id = course_id)
            sections = request.POST.getfiles('sections')
            for section_id in sections:
                course.course_sections.add(Section.objects.get(section_id=section_id))
            course.save()
            return JsonResponse({
                'message' : 'Sections Added Successfully'
            })
        except Exception as e:
            return JsonResponse({
                'message' : 'Please Pass Valid Data'
            })

    def destroy(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            course = Course.objects.get(course_id=request.POST['course_id'])
            course.delete()
            return JsonResponse({
                'message' : 'Course Deleted Successfully'
            })
        except Exception as e:
            return JsonResponse({
                'message' : 'Please Pass Valid Data'
            })

class CourseTestManagment(CreateAPIView):
    def create(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied  
        try:
            pass
        except Exception as e:
            print(e)
            return Response({
                'message' : 'please Pass Valid Data'
            }, status=status.HTTP_400_BAD_REQUEST) 







class WishListManagment(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    def get(self, request, *args, **kwargs):
        try:
            wishlist, created = WishList.objects.get_or_create(instructor=Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user))
            wishlist = WishListSerializer(wishlist).data
            return Response(wishlist)
        except Exception as e:
            raise PermissionDenied

    def update(self, request, *args, **kwargs):
        try:
            token = request.headers['Authorization']
            instructor= Instructor.objects.get(user=Token.objects.get(key=token).user)
        except KeyError:
            raise PermissionDenied
        try:
            course = Course.objects.get(course_id=request.POST['course_id'])
        except Exception as e:
            return JsonResponse({'message' : 'Please Pass Valid o Id'})
        wishlist ,created = WishList.objects.get_or_create(instructor=instructor)
        if course in wishlist.courses.all():
            return JsonResponse({'message' : 'Already In Wishlist'})
        else:
            wishlist.courses.add(course)
            wishlist.save()
        return JsonResponse({'message' : 'Added To Wishlist'})

    def destroy(self, request, *args, **kwargs):
        try:
            token = request.headers['Authorization']
            instructor= Instructor.objects.get(user=Token.objects.get(key=token).user)
        except KeyError:
            raise PermissionDenied
        try:
            course = Course.objects.get(course_id=request.POST['course_id'])
        except Exception as e:
            return JsonResponse({'message' : 'Please Pass Valid Course Id'})
        wishlist ,created = WishList.objects.get_or_create(instructor=instructor)
        if course in wishlist.courses.all():
            wishlist.courses.remove(course)
            wishlist.save()
            return JsonResponse({'message' : 'Removed From Wishlist'})
        else:
            return JsonResponse({'message' : 'Not In Wishlist'})



class EnrollmentManagment(CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView):

    def create(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            course = Course.objects.get(course_id=request.POST['course_id'])
        except Exception as e:
            return JsonResponse({
                'message' : 'Please Pass Valid Data'
            })
        enrollment, created = Enrollment.objects.get_or_create(course=course, user_enrolling=instructor)
        enrollment.save()
        return JsonResponse({
            'message' : 'Enrolled Successfully',
        })
        
    """     def destroy(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            course = Course.objects.get(course_id=request.POST['course_id'])
            cart_item = CartItem.objects.get(course=course, cart_item_owner=instructor)
        except Exception as e:
            return JsonResponse({
                'message' : 'Please Pass Valid Data'
            })
        cart, created = Cart.objects.get_or_create(cart_owner=instructor)
        cart.cart_items.remove(cart_item)
        cart.save()
        cart_item.delete()
        return JsonResponse({
            'message' : 'Deleted Cart Item Successfully'
        })
     """
    
    def get(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        enrollments = EnrollmentSerializer(Enrollment.objects.filter(course__course_instructor=instructor), many=True).data
        return Response(enrollments)




class CourseTests(ListAPIView):
    queryset = CourseTest.objects.all()
    
    def list(self,request, course_id, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            course = Course.objects.get(course_id=course_id)
            return Response(InstruCourseTestSerializer(course.course_test).data)
        except Exception as e:           
            return Response({
                'message' : 'please Pass Valid Data'
            }, status=status.HTTP_400_BAD_REQUEST)            

        
        
                
@api_view(['POST'])        
def enroll_in_live_meeting(request, *args, **kwargs):
    try:
        instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
    except Exception as e:
        raise PermissionDenied
    try:
        data = json.loads(request.body)
        meeting = Meeting.objects.get(meeting_id=data['meeting_id'])
        wallet = Wallet.objects.get(instructor=instructor)
        if instructor not in meeting.students.all():
            if wallet.money_amount >= meeting.price :
                wallet.money_amount -= meeting.price
                meeting.students.add(instructor)
                meeting.save()
                wallet.save()
                return Response({'message' : 'success'} ,status=status.HTTP_201_CREATED)
            else: 
                return Response({'message' : 'No Enough Money'}, status=status.HTTP_402_PAYMENT_REQUIRED)
        return Response({"message" : "success"})
    except Exception as e:           
        return Response({
            'message' : 'please Pass Valid Data'
        }, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['POST'])        
def enroll_in_single_meeting(request):
    try:
        instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
    except Exception as e:
        raise PermissionDenied
    try:
        data = json.loads(request.body)
        av = AvailableForMeeting.objects.get(id=data['available_for_meeting_id'])
        wallet = Wallet.objects.get(instructor=av.instructor)
        wallet_of_stud = Wallet.objects.get(instructor=instructor)
        if wallet_of_stud.money_amount >= av.cost:
            meeting = Meeting.objects.create(
                instructor = av.instructor,
                topic = data['topic'], description = data['description'],
                from_hour = av.availaibe_for_meetings_from_hour,
                to_hour = av.availaibe_for_meetings_to_hour,
                day = av.day,
                date = data['date'],
                is_weekly = True, 
                price = av.cost
            )
            meeting.save()
            meeting.students.add(instructor)
            meeting.save()
            wallet_of_stud.money_amount -= av.cost
            wallet.money_amount += av.cost
            wallet_of_stud.save()
            wallet.save()
            av.delete()
            return Response({'message' : 'success', 'meeting_id' : f"{meeting.meeting_id}"} ,status=status.HTTP_201_CREATED)
        else: 
            return Response({'message' : 'No Enough Money'}, status=status.HTTP_402_PAYMENT_REQUIRED)
            
    except Exception as e:           
        print(e)
        return Response({
            'message' : 'please Pass Valid Data'
        }, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
def my_meetings(request):
    try:
        instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
    except Exception as e:
        raise PermissionDenied
    return Response({
        'meetings_as_instructor' : MeetingInstructorSerializer(Meeting.objects.filter(instructor=instructor), many=True).data,
        'meetings_as_student' : MeetingStudentSerializer(Meeting.objects.filter(students=instructor), many=True).data
    })    
    
    
        
''' class SingleMeetingManagement(CreateAPIView):
    def create(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            data = json.loads(request.body)
            wallet = Wallet.objects.get(instructor=Instructor.objects.get(id=data['instrcutor_id']))
            available_for_meeting = AvailableForMeeting.objects.get(id=data['available_for_meeting_id'])
            if wallet.money_amount >= available_for_meeting.cost:
                meeting = Meeting.objects.create(
                    instructor = available_for_meeting.instructor,
                    topic = data['topic'],
                    description = data['desription'],
                    day = available_for_meeting.day, 
                    from_hour = available_for_meeting.availaibe_for_meetings_from_hour,
                    to_hour = available_for_meeting.availaibe_for_meetings_to_hour,
                    is_weekly= True,
                    price = available_for_meeting.cost
                )
        except Exception as e:           
            return Response({
                'message' : 'please Pass Valid Data'
            }, status=status.HTTP_400_BAD_REQUEST)


 '''




@api_view(['POST'])
def add_live_meeting(request):
    try:
        instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
    except Exception as e:
        raise PermissionDenied
    try:
        meeting = Meeting.objects.create(
            instructor=instructor,
            topic=request.POST['topic'],
            description=request.POST['description'],
            date = request.POST['date'],
            from_hour = request.POST['from_hour'],
            to_hour = request.POST['to_hour'],
            is_weekly = request.POST['is_weekly'],
            day = request.POST['day'],
            meeting_cover_image = request.data['meeting_cover_image'],
            price = int(request.POST['price']),
            
        )
        meeting.save()
        return Response({'message' : 'success'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)               
        return Response({
            'message' : 'please Pass Valid Data'
        }, status=status.HTTP_400_BAD_REQUEST)
        
        
        
@api_view(['GET'])
def last_course(request):
    return Response(CartCourseSerializer(Course.objects.all().order_by('-course_rate').last()).data)