from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/new",views.add_listing,name="add_listing"),
    path("list/<int:id1>",views.list,name="list"),
    path("comment/new",views.comment,name="comment"),
    path("watchlist/<int:id>/del",views.del_watch,name="del_watch"),
    path("watchlist/<int:id>/add",views.add_watch,name="add_watch"),
    path("bid/add/<int:id>",views.add_bid,name="bid_add"),
    path("close/<int:id>",views.close_bid,name="close_bid"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("categories",views.categories,name="categories"),
    path("category/<str:name>",views.category_page,name="category_page"),
]
