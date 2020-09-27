from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers
from .serializers import UserSerializer, BondSerializer
from .models import Bond
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
import requests
import json

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

class BondsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        name = request.GET.get("legal_name", "")
        queryset = Bond.objects.all().filter(userid=request.user.id)
        if name != "":
            queryset = queryset.filter(legal_name=name)

        wantedFields =  ('isin', 'size', 'currency', 'maturity', 'lei', 'legal_name',)    
        data = serializers.serialize('json', list(queryset), fields=wantedFields)
        d = json.loads(data)
        if len(d) == 0:
            return Response("No bonds for this user that match the parameter.", status=status.HTTP_204_NO_CONTENT)

        bonds = [bond["fields"] for bond in d]
        return Response(bonds)

    def post(self, request):
        if "lei" not in request.data:
            return Response("There is no lei in your bond.", status=status.HTTP_400_BAD_REQUEST)
            
        lei = request.data["lei"]
        legal_names = requests.get("https://leilookup.gleif.org/api/v2/leirecords?lei=%s" % lei).json()

        err = len(legal_names) != 1

        try:
            legal_name = legal_names[0]["Entity"]["LegalName"]["$"]
        except:
            err = True

        if err:
            return Response("The lei you have entered does not correspond to any legal name. Bond discarded.", status=status.HTTP_204_NO_CONTENT)    

        legal_name = legal_names[0]["Entity"]["LegalName"]["$"]
        legal_name = legal_name.replace(" ", "")

        request.data["userid"] = request.user.id
        request.data["legal_name"] = legal_name

        serializer = BondSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response("Sorry mate.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
