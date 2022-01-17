from rest_framework.response import Response
from courses.models import Course
from django.core.exceptions import PermissionDenied
from rest_framework.authtoken.models import Token
from users.models import Instructor
from rest_framework import mixins
from extras.serializers import CategorySerializer, PaymentTypeSerializer, RatingSerializer, SimpleCategorySerializer, ParentCategorySerializer, TopicSerializer
from django.http.response import JsonResponse
from extras.models import Category, ParentCategory, PaymentType, Rating, Topic
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework import status
import json


class PCatsCats(ListAPIView):
    def get(self, request, *args, **kwargs):
        context_list = []
        for pcat in ParentCategory.objects.all():
            pcat_item = {
                'parent_category' : ParentCategorySerializer(pcat).data,
                'categories' : SimpleCategorySerializer(Category.objects.filter(parent_category=pcat), many=True).data
            }
            context_list.append(pcat_item)
        return JsonResponse({
            'data' : context_list
        })


class TopPcats(ListAPIView):
    queryset = ParentCategory.objects
    def list(self, request, *args, **kwargs):
        return Response(ParentCategorySerializer(self.queryset.all(), many=True).data)


class TopCats(ListAPIView):
    queryset = Category.objects
    def list(self, request, *args, **kwargs):
        return Response(CategorySerializer(self.queryset.all(), many=True).data)


class PaymentManager(CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView):
    def create(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            payment_provider = request.POST['payment_provider']
            card_number = request.POST['card_number']
            card_cvc = int(request.POST['card_cvc'])
            card_expire_date = request.POST['card_expire_date']
        except Exception as e:
            return JsonResponse({
                'message' : 'Please Pass Valid Data'
            })
        payment = PaymentType.objects.create(
            instructor=instructor, card_number=card_number,
            card_expire_date = card_expire_date, card_cvc=card_cvc
            )
        payment.save()
        if payment_provider == "1":
            payment.payment_provider = "1"
        elif payment_provider == "2":
            payment.payment_provider = "2"
        elif payment_provider == "3":
            payment.payment_provider = "3"
        payment.save()
        return JsonResponse({
            'message' : 'Payment Created Successfully'
        })
    
    def update(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            payment = PaymentType.objects.get(payment_id=request.POST['payment_id'])
            payment_provider = request.POST['payment_provider']
            card_number = request.POST['card_number']
            card_cvc = int(request.POST['card_cvc'])
            card_expire_date = request.POST['card_expire_date']
        except Exception as e:
            return JsonResponse({
                'message' : 'Please Pass Valid Data'
            })
        payment.card_number = card_number
        payment.card_expire_date = card_expire_date
        payment.card_cvc = card_cvc
        if payment_provider == "Visa":
            payment.payment_provider = "Visa"
        elif payment_provider == "Master Card":
            payment.payment_provider = "Master Card"
        elif payment_provider == "Zein Cash":
            payment.payment_provider = "Zein Cash"
        payment.save()
        return JsonResponse({
            'message' : 'Payment Updated Successfully'
        })
    
    def destroy(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            payment = PaymentType.objects.get(payment_id=request.POST['payment_id'])
            payment.delete()
            return JsonResponse({
                'message' : 'Payment Deleted Successfully'
            })
        except Exception as e:
            return JsonResponse({
                'message' : 'Please Pass Valid Data'
            })

    def list(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        return Response(
            PaymentTypeSerializer(
                PaymentType.objects.filter(instructor=instructor),
                many=True
            ).data
        )
        

class CourseRatingApiView(ListAPIView):
    def list(self, request, course_id, *args, **kwargs):
        return Response(RatingSerializer(Rating.objects.filter(course_rated__course_id=course_id), many=True).data)
    
    

class RatingApiView(CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView):
    def create(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            data = json.loads(request.body)
            rating_content = data['rating_content']
            rating_value = float(data['rating_value'])
            course_rated = Course.objects.get(course_id=data['course_id'])
        except:
            return Response({
                'message' : 'Please Pass Valid Data'
            }, status=status.HTTP_400_BAD_REQUEST)

        rating = Rating.objects.create(
            rating_content=rating_content, rating_value=rating_value, instructor=instructor,
            course_rated=course_rated
        )
        rating.save()
        return JsonResponse({
            'message' : 'Rating Created Successfully',
            "rating" : RatingSerializer(rating).data
        })
    def update(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            rating = Rating.objects.get(rating_id=request.POST['rating_id'])
            rating_content = request.POST['rating_content']
            rating_value = float(request.POST['rating_value'])
            course_rated = Course.objects.get(course_id=request.POST['course_id'])
        except:
            return JsonResponse({
                'message' : 'Please Pass Valid Data'
            })
        rating.rating_value = rating_value
        rating.rating_content = rating_content
        rating.save()
        return JsonResponse({
            'message' : 'Rating Edited Successfully'
        })
    def destroy(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            rating = Rating.objects.get(rating_id=request.POST['rating_id'])
        except:
            return JsonResponse({
                'message' : 'Please Pass Valid Data'
            })
        rating.delete()
        return JsonResponse({
            'message' : 'Rating Deleted Successfully'
        })
    def list(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        return Response(RatingSerializer(Rating.objects.filter(course_rated__course_instructor=instructor), many=True).data)
    

class TopRatings(ListAPIView):
    queryset = Rating.objects.all()
    def list(self, request, *args, **kwargs):
        return Response(RatingSerializer(self.queryset.order_by('-rating_value'), many=True).data)
    
    
class ParentCategoryManager(CreateAPIView, UpdateAPIView, DestroyAPIView):
    def create(self, request, *args, **kwargs):
        try:
            user=Token.objects.get(key=request.headers['Authorization']).user
            if not user.is_staff:
                raise PermissionDenied                
        except Exception as e:
            raise PermissionDenied        
        
        try:
            parent_category_name = request.POST['parent_category_name']
            parent_category_image = request.data['parent_category_image']
            parent_category_description = request.POST['parent_category_description']
        except Exception as e:
            return Response({'message':'Please Pass Valid Data'}, status=status.HTTP_400_BAD_REQUEST)
        parent_category = ParentCategory.objects.create(parent_category_name=parent_category_name, parent_category_description=parent_category_description,
            parent_category_image= parent_category_image                       
                                           )
        parent_category.save()
        return Response({'message':'success'}, status.HTTP_201_CREATED)
                
    
class CategoryManager(CreateAPIView, UpdateAPIView, DestroyAPIView):
    def create(self, request, *args, **kwargs):
        try:
            user=Token.objects.get(key=request.headers['Authorization']).user
            if not user.is_staff:
                raise PermissionDenied                
        except Exception as e:
            raise PermissionDenied        
        
        try:
            parent_category = ParentCategory.objects.get(parent_category_id=request.POST['parent_category_id'])
            category_name = request.POST['category_name']
            category_image = request.data['category_image']
            category_description = request.POST['category_description']
        except Exception as e:
            return Response({'message':'Please Pass Valid Data'}, status=status.HTTP_400_BAD_REQUEST)
        category = Category.objects.create(category_name=category_name, category_description=category_description,
                     parent_category=parent_category,category_image= category_image                       
                                           )
        category.save()
        return Response({'message':'success'}, status.HTTP_201_CREATED)
            