from django.shortcuts import render
from .serializers import RegisterSerializer, NoteDetailSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import NoteDetails
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from .paginations import CustomPagination
from django.shortcuts import render, get_object_or_404
# Create your views here.

class RegisterView(APIView):

    permission_classes = [AllowAny]
    def post(self, request):
        register_serializer = RegisterSerializer(data=request.data)
        if register_serializer.is_valid():
            register_serializer.save()
            return Response(register_serializer.data, status=status.HTTP_201_CREATED)
        return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class NoteDetailsView(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self, request):
        note_serializer = NoteDetailSerializer(data=request.data)
        if note_serializer.is_valid():
            note_serializer.save()
            return Response(note_serializer.data, status=status.HTTP_201_CREATED)
        return Response(note_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class NoteDetailsViewGet(APIView):
    
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         note_all = NoteDetails.objects.all()
#         print(request.query_params.get)
#         page_number = request.query_params.get('page_number ', 1)
#         page_size = request.query_params.get('page_size ', 2)

#         paginator = Paginator(note_all , page_size)
#         note_serializer = NoteDetailSerializer(paginator.page(page_number), many=True, context={'request':request})  
#         return Response(note_serializer.data, status=status.HTTP_200_OK)
    
class MyModelPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 10

class NoteDetailsViewGet(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = MyModelPagination

    def get(self, request):
        queryset = NoteDetails.objects.all()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = NoteDetailSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class NoteDetailsViewGetNote(APIView):
    
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            note_obj = NoteDetails.objects.get(noteId = id)
        except Exception:
            note_obj = None

        note_serializer = NoteDetailSerializer(note_obj)  
        print(note_serializer)
        return Response(note_serializer.data, status=status.HTTP_200_OK)
    

class NoteDetailsViewUpdateNote(APIView):
    
    permission_classes = [IsAuthenticated]
    page_size = 2
    max_page_size = 1000

    def put(self, request, id):
        content = dict(request.data)
        if not "title" in content and not "content" in content:
            return Response({"error":"field not there."}, status=status.HTTP_404_NOT_FOUND) 
        note_obj = NoteDetails.objects.filter(noteId = id)
        if note_obj:
            note_pk = NoteDetails.objects.get(noteId = id)
            note_serializer = NoteDetailSerializer(instance=note_pk, data = request.data, partial=True)
            if note_serializer.is_valid():
                note_serializer.save()
                return Response(note_serializer.data, status=status.HTTP_200_OK)
            return Response(note_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"data":"Data Not Found.."}, status=status.HTTP_404_NOT_FOUND)
    

class NoteDetailsViewDelete(APIView):
    
    permission_classes = [IsAuthenticated]
    def delete(self, request, id):
        
        note_obj = NoteDetails.objects.filter(noteId = id)
        if note_obj:
            note_obj.delete()
            return Response({"data":"Data Delete Sucessfully..."}, status=status.HTTP_200_OK)
        return Response({"data":"Data Not Found.."}, status=status.HTTP_404_NOT_FOUND)