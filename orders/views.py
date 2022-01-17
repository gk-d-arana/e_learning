import django
from django.http.response import JsonResponse
from chat.models import ChatRoom, Inbox, Message
from orders.models import Cart, CartItem
from django.core.exceptions import PermissionDenied
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from users.models import Instructor, MyLearning, MyLearningCourse, MyLearningSection, MyLearningVideo, User, WishList
from rest_framework import mixins
from courses.models import Course, Enrollment
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
import json
from django.shortcuts import redirect



class CartItemManager(CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView):

    def create(self, request, *args, **kwargs):
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
            }, status=status.HTTP_400_BAD_REQUEST)
        cart_item, created = CartItem.objects.get_or_create(course=course, cart_item_owner=instructor)
        cart_item.save()
        cart, created = Cart.objects.get_or_create(cart_owner=instructor)
        cart.cart_items.add(cart_item)
        
        cart.save()
        return JsonResponse({
            'message' : 'Created Cart Item Successfully',
        })
        
    def update(self, request, *args, **kwagrs):
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
        try:
            operation = int(request.POST['operation']) # 0 for increase and 1 for descrease
        except:
            return JsonResponse({
                'message' : 'Please Pass Operation'
            })
        if operation == 0:
            cart_item.quantity += 1
        if operation == 1 and cart_item.quantity > 2:
            cart_item.quantity -= 1
        cart_item.save()
        return JsonResponse({
            'message' : 'Updated Cart Item Successfully'
        })

    def destroy(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            data = json.loads(request.body)
            course = Course.objects.get(course_id=data['course_id'])
            cart_item = CartItem.objects.get(course=course, cart_item_owner=instructor)
        except Exception as e:
            print(e)
            return Response({
                'message' : 'Please Pass Valid Data'
            }, status=status.HTTP_400_BAD_REQUEST)
        cart, created = Cart.objects.get_or_create(cart_owner=instructor)
        cart.cart_items.remove(cart_item)
        cart.save()
        cart_item.delete()
        return JsonResponse({
            'message' : 'Deleted Cart Item Successfully'
        })
        
    def get(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        cart, created = Cart.objects.get_or_create(cart_owner=instructor)
        cart.save()
        in_wishlist = False
        wishlist, created =WishList.objects.get_or_create(instructor=Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user))
        wishlist.save()
        data = []
        for cart_item in cart.cart_items.all():
            in_wishlist = False
            if cart_item.course in wishlist.courses.all():
                in_wishlist = True
            data.append({"cart_item" : CartItemSerializer(cart_item).data, "in_wishlist" : in_wishlist})
        return Response(data)




class OrderManager(CreateAPIView, ListAPIView):
    def create(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            data = json.loads(request.body)
            cart, created= Cart.objects.get_or_create(cart_owner=instructor)
            my_learning = MyLearning.objects.get(instructor=instructor)
        except Exception as e:
            print(e)
            return Response({
                'message' : 'Please Pass Valid Data'
            }, status=status.HTTP_400_BAD_REQUEST)
        wallet, created = Wallet.objects.get_or_create(instructor=instructor)
        wallet.save()
        if cart.get_total_price() < wallet.money_amount:
            return Response({'error' : 'not enough money in wallet'}, status=status.HTTP_402_PAYMENT_REQUIRED)    
        order = Order.objects.create(
            ordered_by = instructor,
        )
        for cart_item in cart.cart_items.all():
            order.cart_items.add(cart_item)
            cart_item.course.course_students += 1
            cart_item.course.save()
            my_learning_course, created = MyLearningCourse.objects.get_or_create(course=cart_item.course, instructor=instructor)
            my_learning_course.save()
            for section in cart_item.course.course_sections.all():
                my_learning_section, created = MyLearningSection.objects.get_or_create(section=section)
                my_learning_section.save()
                for video in section.section_videos.all():
                    my_learning_video, created = MyLearningVideo.objects.get_or_create(video=video)
                    my_learning_video.save()
                    my_learning_section.videos.add(my_learning_video)
                my_learning_course.sections.add(my_learning_section)
                my_learning_course.save()
            for pcat in cart_item.course.course_parent_categories.all():
                pcat.students_count += 1
                pcat.save()
            for cat in cart_item.course.course_categories.all():
                cat.students_count += 1
                cat.save()
            cart_item.course.course_instructor.total_students += 1
            cart_item.course.course_instructor.save()
            cart.cart_items.remove(cart_item)
            cart.save()
            enrollment = Enrollment.objects.create(
                course = cart_item.course,
                user_enrolling = instructor
            )
            enrollment.save()
            order.save()
            inbox, created = Inbox.objects.get_or_create(inbox_owner=instructor)
            inbox.save()
            enrollment_message = Message.objects.create(
                message=cart_item.course.course_message,
                message_from=cart_item.course.course_instructor,
                message_to=instructor
            )
            enrollment_message.save()
            inbox.messages.add(enrollment_message)
            inbox.save()
            chat_room = ChatRoom.objects.create()
            chat_room.save()
            chat_room.messages.add(enrollment_message)
            chat_room.chat_room_participants.add(cart_item.course.course_instructor)
            chat_room.chat_room_participants.add(instructor)
            chat_room.save()
            
        return JsonResponse({
            'message' : 'Order Submitted Successfully'
        })

        
    def list(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        orders = OrderSerializer(Order.objects.filter(ordered_by=instructor), many=True).data
        return Response(orders)


class WalletManager(CreateAPIView, UpdateAPIView, RetrieveAPIView):
    def create(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            wallet, created = Wallet.objects.get_or_create(instructor=instructor)
            wallet.save()
            temp_wallet = TempWallet.objects.create(instructor=instructor
                ,money_amount = request.POST['money_amount'],
                check_image = request.data['check_image'],
                transaction_choice = request.POST['transaction_choice'],
                number = request.POST['number'],
                region = request.POST['region'],
                money_before_edit = wallet.money_amount
                                                    )
            temp_wallet.save()
            return Response({'message' : 'success'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message' : 'Please Pass Valid Number'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            data = json.loads(request.body)
            wallet, created = Wallet.objects.get_or_create(instructor=instructor)
            wallet.save()
            temp_wallet = TempWallet.objects.create(instructor=instructor, money_amount=data['money_to_cut'],
                transaction_choice = data['transaction_choice'],
                region = data['region'], number=data['number'],
                money_before_edit=wallet.money_amount)
            temp_wallet.save()
            try:
                payment_company_cut_off = PaymentCompanyCutOff.objects.create(
                    payment_company = PaymentCompany.objects.get(id=data['payment_company_id']),
                    full_name = data['full_name'],
                    region = data['region']
                )
                payment_company_cut_off.save()
                temp_wallet.payment_company_cut_off = payment_company_cut_off
                temp_wallet.branch = Branch.objects.get(id=data['branch_id'])
                temp_wallet.save()
            except Exception as e:
                pass
            return Response({'message' : 'success'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'message' : 'Please Pass Valid Number'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        wallet, created = Wallet.objects.get_or_create(instructor=instructor)
        wallet.save()
        return Response(WalletSerializer(wallet).data)



@api_view(['POST'])
def manage_wallet_money(request):
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
        wallet = Wallet.objects.get(id=data['wallet_id'])
        temp_wallet = TempWallet.objects.get(wallet=wallet)
        if data['condition']:
            wallet.money_amount = temp_wallet.money_amount
            wallet.save()
            temp_wallet.delete()
            return Response({'message' : 'money added successfully'})
        else:
            temp_wallet.delete()
            return Response({'message' : 'money not added to wallet'})
    except Exception as e:
        return Response({'message' : 'Please Pass Valid Number'}, status=status.HTTP_400_BAD_REQUEST)



class TransesManager(ListAPIView, UpdateAPIView, DestroyAPIView):
    queryset = TempWallet.objects.all()
    def list(self, request, *args, **kwargs):
        queryset = TempWallet.objects.all()
        page = self.paginate_queryset(queryset)
        serializer = TempWalletSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

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
            temp_wallet = TempWallet.objects.get(id=data['temp_wallet_id'])
            temp_wallet.delete()
            return Response({'message' : 'success'})
        except Exception as e:
            return Response({'message' : 'Please Pass Valid Data'}, status=status.HTTP_400_BAD_REQUEST)
        


    def update(self, request, *args, **kwargs):
        try:
            user=Token.objects.get(key=request.headers['Authorization']).user
            if user.is_staff:
                pass
            else:
                raise PermissionDenied
        except Exception as e:
            raise PermissionDenied
        try:
            data = json.loads(request.body)
            temp_wallet = TempWallet.objects.get(id=data['temp_wallet_id'])
            instructor = Instructor.objects.get(id=data['instructor_id'])
            wallet, created = Wallet.objects.get_or_create(instructor=instructor)
            wallet.save()
            print(temp_wallet.transaction_choice)
            if temp_wallet.transaction_choice == 'add_money':
                wallet.number = temp_wallet.number
                wallet.region = temp_wallet.region
                wallet.money_amount += temp_wallet.money_amount
                wallet.save()
            else:
                wallet.number = temp_wallet.number
                wallet.region = temp_wallet.region
                wallet.money_amount -= temp_wallet.money_amount
                wallet.save()
            temp_wallet.delete()
            return Response({'message' : 'success'})
        except Exception as e:
            return Response({'message' : 'Please Pass Valid Data'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
@api_view(['GET'])
def all_p_comps(request):
    return Response(PaymentCompanySerializer(PaymentCompany.objects.all(), many=True).data)
        
        

@api_view(['POST'])
def buy_now(request):
    try:
        instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
    except Exception as e:
        raise PermissionDenied
    try:
        data = json.loads(request.body)
        wallet = Wallet.objects.get(instructor=instructor)
        course = Course.objects.get(course_id=data['course_id'])
        if wallet.money_amount >= course.course_price:
            my_learning_course, created = MyLearningCourse.objects.get_or_create(course=course, instructor=instructor)
            my_learning_course.save()
            for section in course.course_sections.all():
                my_learning_section, created = MyLearningSection.objects.get_or_create(section=section)
                my_learning_section.save()
                for video in section.section_videos.all():
                    my_learning_video, created = MyLearningVideo.objects.get_or_create(video=video)
                    my_learning_video.save()
                    my_learning_section.videos.add(my_learning_video)
                my_learning_course.sections.add(my_learning_section)
                my_learning_course.save()
            try:
               cart_item = CartItem.objects.get(course=course, cart_item_owner=instructor)
               cart_item.delete()
            except Exception as e1:
                print(e1)
                pass
            enrollment = Enrollment.objects.create(
                course = course,
                user_enrolling = instructor
            )
            enrollment.save()
            inbox, created = Inbox.objects.get_or_create(inbox_owner=instructor)
            inbox.save()
            enrollment_message = Message.objects.create(
                message=course.course_message,
                message_from=course.course_instructor,
                message_to=instructor
            )
            enrollment_message.save()
            inbox.messages.add(enrollment_message)
            inbox.save()
            chat_room = ChatRoom.objects.create()
            chat_room.save()
            chat_room.messages.add(enrollment_message)
            chat_room.chat_room_participants.add(cart_item.course.course_instructor)
            chat_room.chat_room_participants.add(instructor)
            chat_room.save()
            course.course_students += 1
            course.save()
            course.course_instructor.total_students += 1
            course.course_instructor.save()
            for pcat in course.course_parent_categories.all():
                pcat.students_count += 1
                pcat.save()
            for cat in course.course_categories.all():
                cat.students_count += 1
                cat.save()
            return Response({'message' : 'success'}, status=status.HTTP_201_CREATED)
        else:   
            return Response({'message' : 'No Enough Money'}, status=status.HTTP_402_PAYMENT_REQUIRED)
            
    except Exception as e:
        return Response({'message' : 'Please Pass Valid Data'}, status=status.HTTP_400_BAD_REQUEST)