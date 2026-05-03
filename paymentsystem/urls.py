from django.urls import path


from paymentsystem.shop import views

urlpatterns = [
    path("", views.index, name="index"),
    path("item/<int:id>", views.item, name="item"),
    path("buy/<int:id>", views.buy, name="buy"),
    path("buy_order/<int:id>", views.buy_order, name="buy_order"),
    path("success", views.success, name="success"),
    path('cancel', views.cancel, name="cancel")
]

