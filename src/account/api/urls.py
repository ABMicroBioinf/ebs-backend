from django.urls import path
from . import views

app_name = "account"

'''
    CRUD mapping scheme

        create = register
        read = <int: id>; detail view
        update = update
        delete = delete

    Other requests mapping scheme 

        login = login
        logout = logout
'''
urlpatterns = [
    path('register', views.register_view, name="register"),
    path('<slug>', views.detail_view, name="detail"),
    path('<slug>/update', views.update_view, name="update"),
    path('<slug>/delete', views.delete_view, name="delete"),

    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
]