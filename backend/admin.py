from django.contrib import admin
from .models import Client, Card, Connection, Link, Setting, ClientLink
# Register your  models here.

admin.site.register(Client)
admin.site.register(Card)
admin.site.register(Connection)
admin.site.register(Link)
admin.site.register(Setting)
admin.site.register(ClientLink)
