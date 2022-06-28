from django.urls import path
from .views import client_add, connection_add, connection_remove, client_info, client_list, LinkList, LinkDetails, \
   CardList, CardDetails, SettingList, SettingDetails, ConnectionList, ConnectionDetails, client_Count, ClientLinkList, \
   ClientLinkDetails, get_profile, update_profile, user_link_create_or_update, client_details, client_links_list

urlpatterns = [
   path('clients/info/', client_info),
   path('client-details/',client_details),
   path('profile/', get_profile),
   path('profile/update/', update_profile),
   path('clients/count/', client_Count),
   path('clients/list/', client_list),
   path('connection/remove/', connection_remove),
   path('connection/add/',  connection_add),
   path('links/', LinkList.as_view()),
   path('client-links/create/', user_link_create_or_update),
   path('links/<client>/', LinkDetails.as_view()),
   path('cards/', CardList.as_view()),
   path('cards/<client>/', CardDetails.as_view()),
   path('setting/', SettingList.as_view()),
   path('setting/<client>/', SettingDetails.as_view()),
   path('connection/', ConnectionList.as_view()),
   path('connection/<int:pk>/', ConnectionDetails.as_view()),
   path('client/link/', client_links_list),
   path('client/link/<int:pk>/', ClientLinkDetails.as_view()),
   path('client/add/', client_add),

]

