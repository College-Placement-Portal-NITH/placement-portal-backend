from django.shortcuts import redirect
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import status
# from rest_framework_simplejwt.views import jwt_views
# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            user = serializer.save()
            # print("Valid Data")
            return Response({
                "message": "User Created Successfully.  Now perform Login to get your token",
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
        return Response({
            "errors":serializer.errors,
            "message": "Error Creating User",
        },status=status.HTTP_409_CONFLICT)



# class LoginAPI(KnoxLoginView):
    # permission_classes = (permissions.AllowAny,)

    # def post(self, request, format=None):
    #     serializer = AuthTokenSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.validated_data['user']
    #     login(request, user)
    #     return super(LoginAPI, self).post(request, format=None)