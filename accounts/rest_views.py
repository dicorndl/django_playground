from django.contrib.auth.models import User
from rest_framework import generics

from accounts.serializers import UserSerializer


class AccountList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AccountDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
