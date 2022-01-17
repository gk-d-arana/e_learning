from django.urls import path
from .views import *


urlpatterns = [
    path("cart_manager/", CartItemManager.as_view(), name="cart_item_manager"),    
    path("order_manager/", OrderManager.as_view(), name="order_manager"),
    path("wallet_manager/", WalletManager.as_view(), name="wallet_manager"),
    path("manage_wallet_money/", manage_wallet_money, name="manage_wallet_money"),
    path("transes/", TransesManager.as_view(), name=""),
    path("buy_now/", buy_now, name="buy_now"),    
    path("all_p_comps/", all_p_comps, name="all_p_comps")
]