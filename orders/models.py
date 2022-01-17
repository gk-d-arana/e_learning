from django.db.models.fields import CharField, PositiveIntegerField
from extras.models import PaymentType
from courses.models import Course
from django.db import models
import uuid
from users.models import Instructor


class CartItem(models.Model):
    cart_item_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    cart_item_owner = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name="cart_item_owner")

    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return "Cart Item For Course {} For User {}".format(self.course.course_name, self.cart_item_owner.user.username)
    
    def get_item_total_price(self):
        return self.course.course_price * self.quantity 


class Cart(models.Model):
    cart_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    cart_owner = models.ForeignKey(Instructor, on_delete=models.CASCADE ,related_name="cart_owner")
    cart_items = models.ManyToManyField(CartItem, blank=True)

    def __str__(self):
        return "{} Cart".format(self.cart_owner)

    def get_total_price(self):
        total_price = 0
        for cart_item in self.cart_items.all():
            total_price += cart_item.get_item_total_price()
        return total_price


class Order(models.Model):
    order_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    ordered_by = models.ForeignKey(Instructor, on_delete=models.DO_NOTHING)
    ordered_at = models.DateTimeField(auto_now_add=True)
    cart_items = models.ManyToManyField(CartItem, blank=True)

    def __str__(self):
        return "Order For {}".format(self.ordered_by.user.username)


class Wallet(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, blank=True, null=True)
    number = CharField(max_length=255, default=0, blank=True, null=True)
    money_amount = models.PositiveIntegerField(default=0, blank=True, null=True)    
    is_usable = models.BooleanField(default=False, blank=True, null=True)
    region = models.CharField(max_length=1000,blank=True, null=True, default="Damascus")
    number_sent_to = models.CharField(max_length=1000,blank=True, null=True, default="Damascus")
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        return "Wallet For Instructor {}".format(self.instructor.user.username)


class Branch(models.Model):
    branch_name = models.CharField(max_length=255,blank=True, null=True)
    

class PaymentCompany(models.Model):
    name = models.CharField(max_length=255,blank=True, null=True)
    branches = models.ManyToManyField(Branch, blank=True)


class PaymentCompanyCutOff(models.Model):
    full_name = models.CharField(max_length=255,blank=True, null=True)
    payment_company = models.ForeignKey(PaymentCompany, on_delete=models.SET_NULL,blank=True, null=True)
    region = models.CharField(max_length=1000,blank=True, null=True)



TRANSACTION_CHOICES = (
    ('add_money','add_money'),
    ('cut_off_money','cut_off_money'),
)


class TempWallet(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, blank=True, null=True)
    money_amount = models.PositiveIntegerField(default=0, blank=True, null=True)    
    check_image = models.FileField(upload_to="static/images",blank=True, null=True)     
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    transaction_choice = models.CharField(max_length=255, choices=TRANSACTION_CHOICES, default="add_money",blank=True, null=True)
    payment_company_cut_off = models.ForeignKey(PaymentCompanyCutOff, on_delete=models.SET_NULL,blank=True, null=True)
    number = CharField(max_length=255, default=0, blank=True, null=True)
    region = CharField(max_length=255, default=0, blank=True, null=True)
    money_before_edit = models.PositiveIntegerField(default=0, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL,blank=True, null=True)




