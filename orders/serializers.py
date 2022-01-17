from extras.serializers import PaymentTypeSerializer, SimpleInstructorSerializer
from rest_framework import serializers
from .models import *
from courses.serializers import CartCourseSerializer


class CartItemSerializer(serializers.ModelSerializer):
    course = CartCourseSerializer(Course)
    
    class Meta:
        model = CartItem
        fields = [
            'cart_item_id', 'quantity', 'course'
        ]


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(CartItem, many=True)
    
    class Meta:
        model = Cart
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    ordered_by = SimpleInstructorSerializer(Instructor)
    cart_items = CartItemSerializer(CartItem)
    payment_type = PaymentTypeSerializer(PaymentType)
    class Meta:
        model = Order
        fields  = "__all__"
        
        
class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = [
            "number", "money_amount", 'created_at'
        ]
        
        
class BranchSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Branch
        fields = "__all__"
        

class PaymentCompanySerializer(serializers.ModelSerializer):
    branches = BranchSerializer(Branch, many=True)
    class Meta:
        model = PaymentCompany
        fields = "__all__"
        
class PaymentCompanyCutOffSerializer(serializers.ModelSerializer):
    payment_company = PaymentCompanySerializer(PaymentCompany)
    class Meta:
        model = PaymentCompanyCutOff
        fields = "__all__"
        
        
class TempWalletSerializer(serializers.ModelSerializer):
    instructor = SimpleInstructorSerializer(Instructor)
    payment_company_cut_off = PaymentCompanyCutOffSerializer(PaymentCompanyCutOff)
    class Meta:
        model = TempWallet
        fields = "__all__"