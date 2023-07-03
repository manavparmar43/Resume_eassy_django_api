from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from account.authentication import UserTokenAuthentication
from account.permissions import AdminPermissions
from django.http import JsonResponse
from .serializers import (
    DocumentTypeSerializer,
    DocumentFieldSerializer,
    # DocumentContentSerializer,
    # DocumentContentListSerializer,
    DocumentSerializer,
    DocumentDashboardSerializer,
    DocumentChoiceFieldSerializer,
    DocumentChoiceFieldListSerializer,
    ContentSerializer
)
from .models import *
from .helper import divide_paragraph
import json
from contact.models import DocumentShare
from contact.serializers import DocumentShareSaveSerializer, DocumentShareShowSerializer
from rest_framework.generics import RetrieveAPIView 
import uuid  
from rest_framework.views import APIView
from contact.serializers import DocumentRatingSerializer


class DocumentTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [
        AdminPermissions,
    ]
    authentication_classes = [
        UserTokenAuthentication,
    ]
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save(icon=request.FILES["icon"])
                return Response("Added the Type", 201)
        except:
            return Response("Invalid Credentials", 401)

    ## Field Will be added according to type
    @action(
        detail=True,
        methods=["GET", "POST"],
        url_path="add-field",
        authentication_classes=[
            UserTokenAuthentication,
        ],
        permission_classes=[
            AdminPermissions,
        ],
    )
    def add_document_field(self, request, pk=None):
        if request.method == "POST":
            try:
                for data in request.data:
                    id = data.get("id", None)
                    if id is None:
                        data["type"] = pk
                        serializer = DocumentFieldSerializer(data=data)
                        if serializer.is_valid():
                            data = serializer.save()
                        else:
                            return Response(serializer.errors)
                    else:
                        doc_obj = DocumentField.objects.get(id=id)
                        serializer = DocumentFieldSerializer(
                            instance=doc_obj, data=data, partial=True
                        )
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            return Response(serializer.errors)
                return Response("Added successfully", 201)
            except:
                return Response("Invalid request", 401)

        else:
            try:
                data = DocumentField.objects.filter(type=pk).order_by("-section")
                serializer = DocumentFieldSerializer(instance=data, many=True)
                return Response(serializer.data)
            except:
                return Response("No Field Found", 401)



##use for normal
class DocumentFieldViewSet(viewsets.ModelViewSet):
    permission_classes = [
        AdminPermissions,
    ]
    authentication_classes = [
        UserTokenAuthentication,
    ]
    queryset = DocumentField.objects.all()
    serializer_class = DocumentFieldSerializer
    
    # http_method_names = ['post','get']
    @action(
        detail=True,
        methods=["GET", "POST"],
        url_path="get-field",
        authentication_classes=[
            UserTokenAuthentication,
        ],
        permission_classes=[
            AdminPermissions,
        ],
    )
    def getlist(self,request,pk=None):
        try:
            data = DocumentField.objects.filter(type__id=pk)
            serializer = DocumentFieldSerializer(instance=data, many=True)
            return Response(serializer.data)
        except:
            return Response("No Field Found", 401)
        
    def get_list(self, request, pk=None):
        try:
            data = DocumentField.objects.all()
            serializer = DocumentFieldSerializer(instance=data, many=True)
            return Response(serializer.data)
        except:
            return Response("No Field Found", 401)
        
   
    

class DocumentFieldChoiceViewset(viewsets.ModelViewSet):
    authentication_classes = [
        UserTokenAuthentication,
    ]
    serializer_class = DocumentChoiceFieldSerializer
    def list(self,request):

        queryset=DocumentChoiceFied.objects.filter(selected=True,user__id=request.user.id)
        serializer = DocumentChoiceFieldListSerializer( instance=list(queryset), many=True)
        output = serializer.data  
        title = output[0]['title']
        fields = []
        document_type_list=[]
        for element in output:
            data=DocumentField.objects.get(id=element['document_field_key']['id'])
            document_type_list.append(data.type.id)
            section=data.section
            count=data.count
            usercount=""
            status=""
            document_field_key = element['document_field_key']['id'] 
            selected = element['selected']
            field = {'document_field_key': document_field_key, 'selected': selected,"section":section,"count":count,"usercount":usercount,"status":status}
            fields.append(field)
        document_type = [*set(document_type_list)]
        result = {"document_type":document_type,'title': title, 'fields': fields}
        return Response(result)
    def create(self, request, *args, **kwargs): 
            
        user=User.objects.filter(username=request.user.username)
        
        if user:
            dict=request.data
            for i in dict['fields']:
                
                    document_choice_filed_dict={
                        "user":request.user.id,
                        "document_field_key":i['document_field_key'],
                        "selected":i['selected'],
                        "title":dict['title']
                    }
                    
                    serializer=self.serializer_class(data=document_choice_filed_dict)
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)
            return JsonResponse({"Success":"Document Choice Created"})
            
        else:
            return Response("User Not Found")
        
        
    






# ## use when input the field and submit particular user field; this function will call
# class DocumentContentViewSet(viewsets.ModelViewSet):
#     authentication_classes = [
#         UserTokenAuthentication,
#     ]
#     queryset = DocumentContent.objects.all()
#     serializer_class=DocumentContentSerializer
#     def list(self,request):
#         serializer = DocumentContentListSerializer(instance=list(self.queryset),many=True)
#         return Response(serializer.data)
#     def retrieve(self,request,pk=None):
        
#         if pk:
#             document=DocumentContent.objects.filter(uniquecode=pk)
#             print(document)
#             if document:
#                 serializer = DocumentContentListSerializer(instance=list(document),many=True)
#                 return Response(serializer.data)
#             else:
#                 return Response({"Error":"Data Not Available"})
#         else:
#             return Response({"Error":"Data Not Available"})
       

#     def create(self, request, *args, **kwargs):
#         unicode=uuid.uuid1()
#         hexa=unicode.hex
#         dict=request.data
#         for i in dict['fields']:
#                     print(i)
#                     document_content_filed_dict={
#                         "document_field":i['document_field'],
#                         "count":i['count'],
#                         "content":i['content'],
#                         "uniquecode":hexa
#                     }
                    
#                     serializer=self.serializer_class(data=document_content_filed_dict)
#                     serializer.is_valid(raise_exception=True)
#                     self.perform_create(serializer)
#         return JsonResponse({"Success":"DocumentContent Choice Created"})



## dashboard document View
#comment
class DocumentViewSet(viewsets.ModelViewSet):
    authentication_classes = [
        UserTokenAuthentication,
    ]
    queryset = Document.objects.all()
    serializer_class = DocumentDashboardSerializer

    def get_queryset(self):
        query = self.queryset.filter(user=self.request.user)
        return query

    def retrieve(self, request, *args, **kwargs):
        query = self.get_object()
        serializer = DocumentSerializer(instance=query)
        return Response(serializer.data)

    ##create url for feedback of every unique contact user
    @action(
        detail=True,
        methods=["GET", "POST"],
        url_path="get-feedback",
    )
    def get_feeback(self, request, pk=None):
        if request.method == "POST":
            contacts = request.data.get("contacts", None)

            for contact in contacts:
                data = {"contact": contact, "document": pk}
                serializer = DocumentShareSaveSerializer(data=data)
                data_1 = DocumentShare.objects.filter(
                    contact_user=contact, document=pk
                ).exists()
                if not data_1:
                    if serializer.is_valid():
                        serializer.save()
                else:
                    continue
            return Response("Added Successfully", 201)

        else:
            try:
                data = DocumentShare.objects.filter(document=pk).select_related(
                    "contact_user"
                )
                serializer = DocumentShareShowSerializer(instance=data, many=True)
                return Response(serializer.data, 200)
            except:
                return Response("No Data Found", 200)
            

    ## show preview of document to contact user





class DocumentView(APIView):
    authentication_classes = [UserTokenAuthentication,]
    
    def post(self, request):
        try:
            try:
                payload = request.data
            except Exception as error:
                return Response({"status":False,"error":str(error)},status=status.HTTP_400_BAD_REQUEST)
            try: 
                doc_type=DocumentType.objects.get(id=payload['document_key'])
            except Exception as e:
                return Response({"status":False,"error":"error", "msg":str(e)},status=status.HTTP_400_BAD_REQUEST)
            data = {
                'title':payload['title'],
                'user':request.user,
                'document_key':doc_type,
            }
            doc = Document.objects.create(**data)
            try:
                for i in payload['content']:
                    try: 
                        content_field=DocumentField.objects.get(id=i['content_field'])
                    except Exception as e:
                        return Response({"status":False,"error":"error", "msg":str(e)},status=status.HTTP_400_BAD_REQUEST)
                    record = {
                        'document':doc,
                        'content_field':content_field,
                        'content':i['content'],
                        'content_count':i['content_count']
                    }
                    content = Content.objects.create(**record)
                    result = divide_paragraph(i['content'])
                    for paragraph in enumerate(result):
                        text_count = len(str(paragraph).split())
                        record_1 = {
                            "content" : content,
                            "sub_content" : paragraph[1],
                            "sub_content_count" : text_count
                        }
                        SubContent.objects.create(**record_1)
            except Exception as e:
                return Response({"status":False,"error":"Error while data saving", "msg":str(e)},status=status.HTTP_400_BAD_REQUEST)
            return Response({"status":True,"data":"Document created successfully", "Document_id": doc.id},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":False,"error":"Somthing went wrong", "msg":str(e)},status=status.HTTP_400_BAD_REQUEST)
        


class MyDocumentReview(APIView):
    authentication_classes = [UserTokenAuthentication,]
    
    def  get(self, request, id=None):
        try:
            data = DocumentShare.objects.filter(document__id=id, is_rated=True)
            user_data = data.values_list('id', 'contact_user__name').order_by('-created_at')
        except Exception as e:
            return Response({"status":False,"error":"Document detail not found", "msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        try:
            doc_id = request.GET.get('id', data.first().id)
        except Exception as e:
            return Response({"status":False,"error":"Something went wrong","msg":str(e)}, status=status.HTTP_400_BAD_REQUEST)

        document_data = data.get(id=doc_id)
        try:
            if serializer := DocumentRatingSerializer(document_data):
                return Response({"status":True,"user_data":user_data, "data":serializer.data}, status=status.HTTP_200_OK)
            return Response({"status":False,"error":"Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status":False,"error":"Something went wrong","msg":str(e)}, status=status.HTTP_400_BAD_REQUEST)


        
        





            

