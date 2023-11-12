from django.urls import path
from django.conf.urls.static import static
from publications.apps import PublicationsConfig
from publications import views
from users.views import *
from publications.views import *


app_name = PublicationsConfig.name
dinnland_title = {'title': 'Dinnland_subs'}

urlpatterns = [
    path('base/', base),
    # # path('', cache_page(5)(HomeListView.as_view(extra_context={'title': 'DinnMail'})), name='home'),
    path('', HomeListView.as_view(extra_context=dinnland_title), name='home'),
    path('not_authenticated/', NotAuthenticated.as_view(extra_context=dinnland_title), name='not_authenticated'),
    path('publications/', views.PublicationListView.as_view(extra_context=dinnland_title), name='publication_list'),
    path('free_publications/', views.FreePublicationListView.as_view(extra_context=dinnland_title),
         name='free_publication_list'),
    path('paid_publications/', views.PaidPublicationListView.as_view(extra_context=dinnland_title),
         name='paid_publication_list'),
    path('publications/author/<int:pk>/', views.AuthorPublicationListView.as_view(
        extra_context={'title': 'Dinnland_subs'}), name='author_publication_list'),
    path('create-publication/', PublicationCreateView.as_view(
        extra_context=dinnland_title), name='createpublication'),
    path('view-publication/<int:pk>/', PublicationDetailView.as_view(
        extra_context=dinnland_title), name='viewpublication'),
    path('edit-publication/<int:pk>/', PublicationUpdateView.as_view(
        extra_context=dinnland_title), name='editpublication'),
    path('delete-publication/<int:pk>/', PublicationDeleteView.as_view(
        extra_context=dinnland_title), name='deletepublication'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
