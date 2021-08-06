from django.urls import path


from rest_framework_simplejwt.views import (
    #TokenObtainPairView,
    TokenRefreshView,
) 

from .api import (
    register_view,
    detail_view,
    update_view,
    delete_view,
    login_view,
    logout_view,
    MyTokenObtainPairView,

)

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
    path('login', login_view, name="login"),
    path('logout', logout_view, name="logout"),
    path('register', register_view, name="register"),
    path('detail', detail_view, name="detail"),
    path('update', update_view, name="update"),
    path('delete', delete_view, name="delete"),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]