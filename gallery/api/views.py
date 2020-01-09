from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from gallery.models import uploadss, uploads
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token 
from .serializers import gallerySerializer, registrationSerializer

#class api_show_image(ListAPIView):
 #   queryset = uploadss.objects.all()
  #  serializer_class =  gallerySerializer

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_show_image(request, id_image, slug):

    blog = uploads.objects.get(id = id_image)
    serializer = gallerySerializer(blog)

    return Response(serializer.data)




@api_view(['PUT',])
def api_put_image(request, id_image, slug):

    blog = uploads.objects.get(id = 25)
    serializer = gallerySerializer(blog, data=request.data)
    data = {}
    if serializer.is_valid():
          serializer.save()
          data['success'] = 'updated successfully'
          return Response(data=data)

    return Response(serializer.data)

@api_view(['DELETE',])
def api_delete_image(request, id_image, slug):

    blog = uploads.objects.get(id = id_image)
    operation = blog.delete()
    data = {}
    if operation:
        data['success'] = 'successfully deleted'
    else:
        data['failure'] = 'failed to delete'
    

    return Response(data=data)

@api_view(['POST',])
def api_upload_image(request,slug):

    user = User.objects.get(pk = 5)
    blog = uploads(username= user)

    if request.method == 'POST':
        serializer = gallerySerializer(blog, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
def api_newUser(request):
    if request.method == 'POST':
        serializer = registrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['Success'] = 'successfully Registered a new user'
            data['email'] = user.email
            data['Success'] = user.username
            token = Token.objects.get(user=user).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)