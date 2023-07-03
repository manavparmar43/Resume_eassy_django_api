from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework.response import Response
from account.authentication import UserTokenAuthentication
from .models import *
from .serializers import ContactSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status
from document.serializers import *
from math import factorial
import statistics
from .serializers import *

# Create your views here.
from django.conf import settings

## create particular user contact
class ContactViewset(viewsets.ModelViewSet):
    authentication_classes = (UserTokenAuthentication,)
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get_queryset(self):
        query = self.queryset.filter(user_key=self.request.user)
        return query

    def create(self, request, *args, **kwargs):
        print("Inside view")
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user_key=request.user)
            return Response("Added Contact", 201)
        return Response("Invalid Credentials", 401)


class DocumentShareViewset(viewsets.ModelViewSet):
    queryset = DocumentShare.objects.all()
    serializer_class = DocumentSerializer

    @action(detail=True, methods=["GET", "POST"], url_path="preview")
    def preview_document(self, request, pk=None, id=None):
        if request.method == "POST":
            try:
                query = self.queryset.filter(pk=pk).update(
                    rating=request.data["rating"]
                )
                query_2 = self.queryset.filter(pk=pk).update(disabled=True)
                return Response("Added Rating", 201)
            except:
                return Response("Bad Request", 404)
        else:
            try:
                new_dict = {}
                document = self.get_object().document
                serializer = self.get_serializer(instance=document, partial=True)
                # disabled = DocumentShare.objects.filter(id=pk).first().disabled
                data = DocumentShare.objects.filter(
                    document=serializer["id"].value
                )
                rating=data.aggregate(rating=Avg("rating"))
                shared_doc = DocumentShare.objects.get(id=pk)
                new_dict['shared_doc_id']=shared_doc.id
                new_dict['is_rated'] = shared_doc.is_rated
                new_dict["created_by"]=document.user.username
                new_dict["document_type"] = document.document_key.name
                new_dict.update(serializer.data)
                new_dict.update(rating)
                # new_dict["disabled"] = disabled
                return Response(new_dict, 200)
            except:
                return Response("No Data Found", 404)
            

class DocumentRatingView(APIView):
    def post(self, request, id=None):
        try:
            try:
                payload = request.data
            except Exception as error:
                return Response({"status":False,"error":str(error)},status=status.HTTP_400_BAD_REQUEST)
            try:
                document = DocumentShare.objects.get(id=id)
            except Exception as e:
                print(e,"eeeeee")
                return Response({"status":False,"error":"Document detail not found"},status=status.HTTP_400_BAD_REQUEST)
            try:
                content = Content.objects.get(id=payload['content_id'])
            except Exception as e:
                return Response({"status":False,"error":"Content detail not found"},status=status.HTTP_400_BAD_REQUEST)
            
            try:
                data = {
                    'document_share':document,
                    'content':content,
                }
                content_rating = ContetRating.objects.create(**data)

                rating_list = []
                for i in payload['sub_contant']:
                    try: 
                        sub_content = SubContent.objects.get(id=i['sub_content_id'])
                    except Exception as e:
                        return Response({"status":False,"error":"Sub-content detail not found"},status=status.HTTP_400_BAD_REQUEST)

                    record = {
                        'sub_content':sub_content,
                        'content_rating': content_rating,
                        'rating': i['rating']
                    }
                    rating_list.append(i['rating'])
                    SubContentRating.objects.create(**record)

                avg_content = statistics.mean(rating_list)
                avg_rating = round(avg_content,1)
                content_rating.rating = avg_rating
                content_rating.save()

                document.is_rated = payload.get('is_rated', document.is_rated )
                document.save()
                
                return Response({"status":True,"content_avg":avg_rating,"data":"Rating added successfully"},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"status":False,"error":"Error while data saving", "msg":str(e)},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status":False,"error":"Somthing went wrong"},status=status.HTTP_400_BAD_REQUEST)
        

    def get(self, request, id=None):
        try:
            data = DocumentShare.objects.get(id=id)
        except Exception as e:
            return Response({"status":False,"error":"Document detail not found"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            doc_rating = ContetRating.objects.filter(document_share=id).aggregate(rating=Avg("rating"))
            data.rating = doc_rating.get('rating')
            data.save()
        except:
            pass
        try:
            if serializer := DocumentRatingSerializer(data):
                return Response({"status":True, "data":serializer.data}, status=status.HTTP_200_OK)
            return Response({"status":False,"error":"Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status":False,"error":"Something went wrong","msg":str(e)}, status=status.HTTP_400_BAD_REQUEST)

