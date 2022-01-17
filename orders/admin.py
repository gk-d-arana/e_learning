from django.contrib import admin

from .models import *


admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(TempWallet)
admin.site.register(Wallet)
admin.site.register(Branch)
admin.site.register(PaymentCompany)
admin.site.register(PaymentCompanyCutOff)
