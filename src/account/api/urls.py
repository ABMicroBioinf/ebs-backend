from django.urls import path
from . import views

app_name = "account"

'''
    CRUD URI mapping scheme

        create = register
        read = <int: id>; detail view
        update = update
        delete = delete

    Additional requests mapping scheme 

        login = login
        logout = logout
'''
urlpatterns = [
    path('register', views.register_view, name="register"),
    path('<email>', views.detail_view, name="detail"),
    path('<email>/update', views.update_view, name="update"),
    path('<email>/delete', views.delete_view, name="delete"),

    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
]