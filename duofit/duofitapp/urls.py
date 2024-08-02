<<<<<<< HEAD
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    index,
    login_view,
    signup_view,
    settings_view,
    log_training,
    logout_user,
    editconfig_view,
    statistics_view
)

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name="login"),
    path('signup/', signup_view, name="signup"),
    path('logout/', logout_user, name="logout"),
    path('settings/', settings_view, name="settings"),
    path('editconfig/', editconfig_view, name="editconfig"),
    path('log_training/', log_training, name='log_training'),
    path('statistics/', statistics_view, name='statistics')
]

if settings.DEBUG:
=======
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    index,
    login_view,
    signup_view,
    settings_view,
    log_training,
    logout_user,
    editconfig_view,
    statistics_view
)

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name="login"),
    path('signup/', signup_view, name="signup"),
    path('logout/', logout_user, name="logout"),
    path('settings/', settings_view, name="settings"),
    path('editconfig/', editconfig_view, name="editconfig"),
    path('log_training/', log_training, name='log_training'),
    path('statistics/', statistics_view, name='statistics')
]

if settings.DEBUG:
>>>>>>> d77da84d47139c0f069eb156bd042e60b9e7d816
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)