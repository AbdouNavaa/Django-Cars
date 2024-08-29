from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('trendings', views.trendings, name="trendings"),
    path('auctions', views.auctions, name="auctions"),
    path('reviews', views.reviews, name="reviews"),
    path('add_car', views.add_car, name="add_car"),
    path('seller_cars', views.seller_cars, name="seller_cars"),
    path('C<int:id>',views.car_details , name='car_details'),
    path('like<int:id>',views.add_like , name='add_like'),
    path('CI<int:id>',views.add_carImage , name='add_carImage'),
    # autres routes
    path('ajax/load-models/', views.load_models, name='ajax_load_models'),
    path('ajax/load-trims/', views.load_trims, name='ajax_load_trims'),
    
    path('<int:id>/<int:c_id>',views.to_Update , name='to_Update'),
    path('update_comment/<int:car_id>/<int:c_id>', views.update_comment, name='update_comment'),
    path('delete_comment/<int:car_id>/<int:c_id>', views.delete_comment, name='delete_comment'),
    path('add_comment/<int:id>/', views.add_comment, name='add_comment'),
]