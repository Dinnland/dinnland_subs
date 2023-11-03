from django.urls import path
from django.conf.urls.static import static

from publications.apps import PublicationsConfig
from publications import views
from users.apps import UsersConfig
from users.views import *
from publications.views import *


app_name = PublicationsConfig.name

urlpatterns = [
    # mail_app
    path('base/', base),
    # # path('', cache_page(5)(HomeListView.as_view(extra_context={'title': 'DinnMail'})), name='home'),
    path('', HomeListView.as_view(extra_context={'title': 'Dinnland_subs'}), name='home'),
    #
    # path('contacts/', index_contacts, name='contacts'),
    path('not_authenticated/', NotAuthenticated.as_view(extra_context={'title': 'Dinnland_subs'}), name='not_authenticated'),
    # path('cabinet/', CabinetView.as_view(), name="cabinet"),Publication

    path('pubs/', views.PublicationListView.as_view(), name='publication_list'),
    path('create-publication/', PublicationCreateView.as_view(), name='createpublication'),
    path('view-publication/<int:pk>/', PublicationDetailView.as_view(extra_context={'title': 'Dinnland_subs'}), name='viewpublication'),
    path('edit-publication/<int:pk>/', PublicationUpdateView.as_view(), name='editpublication'),
    path('delete-publication/<int:pk>/', PublicationDeleteView.as_view(), name='deletepublication'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
