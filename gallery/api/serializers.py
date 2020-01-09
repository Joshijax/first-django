from rest_framework import serializers
from django.contrib.auth.models import User
from gallery.models import uploadss, uploads

#class gallerySerializer(serializers.ModelSerializer):
#    class Meta:
 #       model = uploads
 #       fields = ['filename',]


class gallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = uploads
        fields = ['file','file_name','file_name',  'filetype', 'uploaded_at']

class registrationSerializer(serializers.ModelSerializer):
    password2 =serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    class Meta:
        model = User
        fields = ['email','username','password', 'password2',]
        extra_kwargs= {
            'password' :{'write_only' : True}
        }

        
    def save(self):
        user = User(
            email= self.validated_data['email'],
            username = self.validated_data['username'],
        )
        password= self.validated_data['password']
        password2=self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'password does not match'})
        user.set_password(password)
        user.save()
        return user