from scm_app.views import *
from django.urls import path

urlpatterns = [
    path('upload-db-data/', ListUsers.as_view(), name='upload-db-data'),
]