from django.db import models
from django.contrib.auth.models import User

def upload_path(instance, filename):
       return '/'.join(['pictures', str(instance.name), filename])

class Client(models.Model):
       firstname = models.CharField(max_length=500)
       lastname = models.CharField(max_length=500)
       name = models.CharField(max_length=500)
       country = models.CharField(max_length=500)
       adress = models.CharField(max_length=500)
       town = models.CharField(max_length=500)
       postcode = models.CharField(max_length=500)
       description = models.CharField(max_length=500)
       phone = models.IntegerField()
       is_active = models.BooleanField(default=True)
       is_deleted = models.BooleanField(default=False)
       mail = models.CharField(max_length=300)
       image=models.CharField(max_length=500)
       author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')
       user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, )
       picture= models.ImageField(default="default.jpg", upload_to=upload_path)
       def __str__(self):
           return self.name

class Connection(models.Model):
       owner = models.ForeignKey(Client, related_name='owner', on_delete=models.CASCADE)
       linked_to = models.ForeignKey(Client, on_delete=models.CASCADE)


class Card(models.Model):
       is_active = models.BooleanField(default=True)
       client = models.OneToOneField(Client, on_delete=models.CASCADE)

class Link(models.Model):
       title = models.CharField(max_length=300)
       type = models.CharField(max_length=300)
       image= models.CharField(max_length=500)

       def __str__(self):
           return self.title

class Setting(models.Model):
       account_mode = models.CharField(max_length=300)
       theme = models.CharField(max_length=300)
       client = models.ForeignKey(Client, on_delete=models.CASCADE)


class ClientLink(models.Model):
       value = models.CharField(max_length=500)
       client = models.ForeignKey(Client, on_delete=models.CASCADE)
       link = models.ForeignKey(Link, on_delete=models.CASCADE)

