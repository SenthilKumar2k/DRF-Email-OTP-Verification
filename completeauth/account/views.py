from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, VerifyAccountSerializer
from .emails import *

class RegisterAPI(APIView):
    def post(self, request):
        try:
            data=request.data
            serializer=UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                print("fine")
                send_otp_via_email(serializer.data['email'])
                return Response({"status":200,"message":"user registered successfully check email","data":serializer.data})
            return Response({"status":400,"message":"something went wrong", "data":serializer.errors})
        except Exception as e:
            print(f"An error occurred during user registration: {e}")
            return Response({
                "status": 500,
                "message": "Internal server error. Please try again later.",
                "data": None
            })
        
class VerifyOTP(APIView):
    def post(self,request):
        try:
            data=request.data
            serializer=VerifyAccountSerializer(data=data)
            if serializer.is_valid():
                email=serializer.data['email']
                otp=serializer.data['otp']
                user=User.objects.filter(email=email)
                if not user.exists():
                    return Response({'status':400,'message':'something went wrong','data':'email invalid'})
                if user[0].otp !=otp:
                    return Response({'status':400,'message':'something went wrong','data':'otp invalid'})
                user[0].is_verified=True
                user[0].save()
                return Response({'status':200,'message':'account verified successfully'})
            return Response({'status':400,'message':'something went wrong','data':serializer.errors})
        except Exception as e:
            print(f"An Error occurred during user verification: {e}")
            return Response({
                "status": 500,
                "message": "Internal server error. Please try again later.",
                "data": None
            })