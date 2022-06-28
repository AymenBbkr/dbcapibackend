from django.shortcuts import render
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
import simplejson
from .models import Client, Link, Card, Setting, Connection, ClientLink
from .serializers import ClientSerializer, LinkSerializer, CardSerializer, SettingSerializer, ConnectionSerializer, ClientLinkSerializer
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView
from django.http import Http404

from rest_framework import mixins
from rest_framework import generics


'''
class ClientDelete(generics.DestroyAPIView):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
    name = 'connection'

    filter_fields = (
        'client1',
        'client2'
    )
'''

class ClientLinkList(generics.ListCreateAPIView):
    queryset = ClientLink.objects.all()
    serializer_class = ClientLinkSerializer



class ClientLinkDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClientLink.objects.all()
    serializer_class = ClientLinkSerializer



class ConnectionList(generics.ListCreateAPIView):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer

class ConnectionDetails(generics.RetrieveUpdateDestroyAPIView):

    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer

class SettingList(generics.ListCreateAPIView):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer

class SettingDetails(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'client'
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer



class CardList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CardDetails(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    lookup_field = 'client'

    def get(self, request, client, *args, **kwargs):
        return self.retrieve(request, client=client)

    def put(self, request, client, *args, **kwargs):
        return self.update(request, client=client)

    def delete(self, request, client):
        return self.delete(request, client=client)



class LinkList(APIView):
    def get(self, request):
        links = Link.objects.all()
        serializer = LinkSerializer(links, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LinkDetails(APIView):
    def get_object(self, client):
        try:
            return Link.objects.get(client=client)
        except Link.DoesNotExist:
            raise Http404

    def get(self, request, client):
        link = self.get_object(client)
        serializer = LinkSerializer(link)
        return Response(serializer.data)

    def put(self, request, client):
        link = self.get_object(client)
        serializer = LinkSerializer(link, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, client):
        link = self.get_object(client)
        link.delete()
        return Response(status.HTTP_204_NO_CONTENT)







@api_view(['GET', 'POST'])
def client_Count(request):
        if request.method == "GET":
            clients = Client.objects.all().count()


            return Response(clients)


        elif request.method == "POST":
            serializer = ClientSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'POST'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def client_links_list(request, *args, **kwargs):
    try:
        client = Client.objects.get(user_id=request.user.id)
        clientLinks = ClientLink.objects.filter(client=client.id)
        serializerLink= ClientLinkSerializer(clientLinks,many=True)
        return Response(serializerLink.data)
    except Client.DoesNotExist:
        return JsonResponse({'message': 'No Item Found'}, status=status.HTTP_404_NOT_FOUND)
@api_view(['GET', 'POST'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def client_info(request, *args, **kwargs):
    try:
        clients = Client.objects.all()
        client = Client.objects.get(user_id=request.user.id)

        list=[]
        serializer = ClientSerializer(clients, many=True)
        for c in serializer.data:
            if c["id"]==client.id:
                continue
            followed = getIsFollwed(client.id,c["id"])
            list.append({'name':c["name"],'descrption':c["description"],'id':c["id"],'phone':c["phone"],'mail':c["mail"],'isFollowed':followed,})
        return Response(list)
    except Client.DoesNotExist:
        return JsonResponse({'message': 'No Item Found'}, status=status.HTTP_404_NOT_FOUND)
@api_view(['GET', 'POST'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def client_details(request, *args, **kwargs):
    try:
        client = Client.objects.get(id=request.data["id"])
        clientLinks= ClientLink.objects.filter(client=client.id)
        print(len(clientLinks))
        serializerClient = ClientSerializer(client)
        serializerLink= ClientLinkSerializer(clientLinks,many=True)
        response=serializerClient.data
        response["clientlinks"]=serializerLink.data
        list = []
        link = []
        for l in serializerLink.data:


            link_detail = getChoix(l['link'])[0]
            link.append({'clientLinkId': l["id"], 'type': link_detail["type"], 'value': l["value"],
                         'title': link_detail["title"], 'image': link_detail["image"]})

        c = getInfo(request.data["id"])
        retrn = {'firstname': c['firstname'], 'picture':c['picture'], 'lastname': c['lastname'], 'description':c['description'], 'image':c['image'], 'mail':c['mail'],
                 'id': c['id'], 'name': c['name'], 'phone': c['phone'], 'links':link}
        list.append(retrn)
        return Response(list)
    except Client.DoesNotExist:
        return JsonResponse({'message': 'No Item Found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET', 'POST'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def get_profile(request, *args, **kwargs):
    try:
        client = Client.objects.get(user_id=request.user.id)

        serializer = ClientSerializer(client)

        return Response(serializer.data)
    except Client.DoesNotExist:
        return JsonResponse({'message': 'No Item Found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def update_profile(request, *args, **kwargs):
    try:
        data = simplejson.loads(request.body)
        print(data["firstname"])
        client = Client.objects.filter(user_id=request.user.id)
        client.update(firstname=data["firstname"] ,lastname=data["lastname"],description=data["description"], name=data["name"],country=data["country"],
                      adress=data["adress"], town=data["town"], postcode=data["postcode"], phone=data["phone"], image=data["image"], mail=data["mail"])
        serializer = ClientSerializer(client, many=True)
        return Response(serializer.data)
    except Client.DoesNotExist:
        return JsonResponse({'message': 'No Item Found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET', 'POST'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def client_list(request, *args, **kwargs):

    try:

        list = []
        client= Client.objects.get(user_id=request.user.id)
        connections = Connection.objects.filter(owner=client.id)
        serializer = ConnectionSerializer(connections, many=True)

        for c in serializer.data:
            client = getInfo(c['linked_to'])
            links = getLinks(client['id'])
            link = []
            for l in links:
                print(l)
                link_detail = getChoix(l['link'])[0]
                link.append({'clientLinkId':l["id"],'type':link_detail["type"],'value':l["value"],'title':link_detail["title"],'image':link_detail["image"]})
            print(link)
            retrn = {'cnx':c["id"],'description':client['description'],'image':client['image'],'mail':client['mail'],'client':client['id'],'name':client['name'],'phone':client['phone'],'links':link}
            list.append(retrn)
        return Response(list)
    except Connection.DoesNotExist:
        return JsonResponse({'message': 'No Item Found'}, status=status.HTTP_404_NOT_FOUND)







@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def connection_remove(request, *args, **kwargs):
    try:
        client = Client.objects.get(user_id=request.user.id)
        Connection.objects.filter(owner=client.id,linked_to=request.data["id"]).delete()
        return JsonResponse({'message': 'Done'}, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def user_link_create_or_update(request, *args, **kwargs):
    try:
        client = Client.objects.get(user_id=request.user.id)
        input = simplejson.loads(request.body)
        for item in input:
            clientLinks = ClientLink.objects.filter(client=client.id,link=item["link"])
            if not clientLinks:
                link_item = Link.objects.get(id=item["link"])
                newClientLink = ClientLink.objects.create(client=client,link=link_item,value=item["value"])
                newClientLink.save()
            else:
                clientLinks.update(client=client.id,link=item["link"],value=item["value"])



        return JsonResponse({'message': 'Done'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST, )


@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def connection_add(request, *args, **kwargs):
    try:

        owner = Client.objects.get(user_id=request.user.id)
        linked_to = Client.objects.get(id=request.data["client"])
        existConnection = Connection.objects.filter(owner=owner.id, linked_to=request.data["client"])
        if existConnection:
            return Response({'message': 'Connection already exist!'}, status=status.HTTP_400_BAD_REQUEST)

        new_connection = Connection.objects.create(owner=owner, linked_to=linked_to)
        new_connection.save()
        return JsonResponse({'message': 'Done'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST, )


@api_view(['GET', 'POST'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def client_add(request, *args, **kwargs):
    try:

        new_client = Client.objects.create(name=request.data["name"], password=request.data["password"], phone=request.data["phone"], mail=request.data["mail"])
        new_client.save()
        clientlink_add(new_client)

        return JsonResponse({'message': 'Done'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)





def clientlink_add(client):
    try:
        links = Link.objects.all()
        serializer = LinkSerializer(links)
        for l in links:
            print(l)
            newClientLink = ClientLink.objects.create(value='', client=client, link=l)
            newClientLink.save()



    except Exception as e:
        print(e)

'''
for l in links:
print(l)
newClientLink = ClientLink.objects.create(value=[""], client=["client"], link=["links"])
 print(newClientLink)
'''


def getInfo(id):
    try:
        print(id)
        clients = Client.objects.filter(id=id)
        serializer = ClientSerializer(clients, many=True)
        print(serializer.data)
        return serializer.data[0]
    except Client.DoesNotExist:
        return JsonResponse({'message': 'No Item Found'}, status=status.HTTP_404_NOT_FOUND)
def getIsFollwed(cnx,clientId):
    try:
        connexion = Connection.objects.filter(owner=cnx,linked_to=clientId)
        serializer = ConnectionSerializer(connexion, many=True)
        return not not serializer.data
    except Client.DoesNotExist:
        return JsonResponse({'message': 'No Item Found'}, status=status.HTTP_404_NOT_FOUND)

def getLinks(id):
    try:
        links = ClientLink.objects.filter(client=id)
        serializer = ClientLinkSerializer(links, many=True)
        return serializer.data
    except ClientLink.DoesNotExist:
        return JsonResponse({'message: No Item Found'}, status.HTTP_404_NOT_FOUND)

def getChoix(id):
    try:
        choix = Link.objects.filter(id=id)
        serializer = LinkSerializer(choix, many=True)
        return serializer.data
    except Link.DoesNotExist:
        return JsonResponse({'message: No Item Found'}, status.HTTP_404_NOT_FOUND)


















