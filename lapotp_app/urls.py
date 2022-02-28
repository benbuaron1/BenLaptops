from django.urls import path

from . import views

# Creating URLConf
#api/v1/restaurants GET | POST
#api/v1/restaurants/1 GET | PUT | PATCH | DELETE

#api/v1/restaurants/1/reviews GET | POST
#api/v1/restaurants/1/reviews/11 GET | PUT | PATCH | DELETE

#api/v1/userprofile/current

#api/v1/reviews GET | POST


urlpatterns = [
    path('review/',views.review),
    path('review/<int:pk>',views.review_by_id),
    path("laptops/", views.laptops_list),
    path("laptops/<int:pk>", views.laptop_details),
    path("orders/",views.orders_list),
    path("customers/",views.customers),
    path('stats/best_laptops',views.best_laptops),
    path('stats/manu_reviews',views.reviews_manufactorer),
    path('stats/cheapest_rated',views.cheap_rate)
]