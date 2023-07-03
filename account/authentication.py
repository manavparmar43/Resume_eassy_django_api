from .models import NonBuiltInUserToken
from rest_framework.authentication import BaseAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework import exceptions
from .models import User
import datetime
from django.utils import timezone
from datetime import timedelta

class UserTokenAuthentication(TokenAuthentication):
    

    def authenticate(self, request):
        try:
            token = request.headers.get('Authorization')
            access_token = token.split(' ')[1]

        except:
                
            raise exceptions.AuthenticationFailed("Authentication Token require")
            


        if not token:
            return None
        
        try:
            access_token = token.split(' ')[1]
            user = NonBuiltInUserToken.objects.get(key=access_token)

      

        except IndexError:
            raise exceptions.AuthenticationFailed("Token Perfix missing")
        
        except NonBuiltInUserToken.DoesNotExist:
            raise exceptions.AuthenticationFailed("Token is Invalid")
        

        return(user.user,None)
        
       
    
        #     if main > user.created:
        #         token = NonBuiltInUserToken.objects.create(user=user)
        #         return Response
        # except:
        #     return Jso    

        # try:
        #     token = request.headers.get('Authorization').split(' ')[1]
        #     try:
        #         user = NonBuiltInUserToken.objects.get(key=token)
        #         main = timezone.now() - timedelta(minutes=10)

        #         if main > user.created:

        #             raise exceptions.AuthenticationFailed("Token Expired")
        #         else:
        #             return (user.user, None)
        #     except:
        #         raise exceptions.AuthenticationFailed("You are not authorized to access")   
        
        # except token as exception:
        #     raise exceptions.AuthenticationFailed("Token Not Provided")    

