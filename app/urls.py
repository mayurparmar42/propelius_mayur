from django.contrib import admin
from django.urls import path
from .views import RegisterView, NoteDetailsView, NoteDetailsViewGet, NoteDetailsViewGetNote, NoteDetailsViewUpdateNote, NoteDetailsViewDelete
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('registration/', RegisterView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('createNote/', NoteDetailsView.as_view(), name='createNote'),
    path('listNotes/', NoteDetailsViewGet.as_view(), name='listNotes'),
    path('getNote/<int:id>/', NoteDetailsViewGetNote.as_view(), name='getNote'),
    path('updateNote/<int:id>/',NoteDetailsViewUpdateNote.as_view(), name='updateNote' ),
    path('deleteNote/<int:id>/', NoteDetailsViewDelete.as_view(), name='deleteNote')
]