from django.urls import path

from subs.apps import SubsConfig
from subs.views import base

app_name = SubsConfig.name

urlpatterns = [
    # mail_app
    path('base/', base),
    # path('', cache_page(5)(HomeListView.as_view(extra_context={'title': 'DinnMail'})), name='home'),
    path('', HomeListView.as_view(extra_context={'title': 'DinnMail'}), name='home'),

    path('contacts/', index_contacts, name='contacts'),
    path('not_authenticated/', NotAuthenticated.as_view(extra_context={'title': 'Dinnstore'}), name='not_authenticated'),
    path('cabinet/', CabinetView.as_view(), name="cabinet"),

    # mailing_settings
    path('create-mailing/', MailingSettingsCreateView.as_view(), name='mailing_create'),
    path('mailing-settings-list/', MailingSettings1ListView.as_view(extra_context={'title': 'DinnMail'}), name="mailinglist"),
    path('mailing-settings/<int:pk>/update/', MailingSettingsUpdateView.as_view(), name='mailing_upd'),
    path('mailing-settings/<int:pk>/delete/', MailingSettingsDeleteView.as_view(), name='mailing_del'),
    # path('mailinglist/', MailingSettings1ListView.as_view(extra_context={'title': 'DinnMail'}), name="mailinglist"),

    # path('profile/', ProfileDataView.as_view(), name="profile"),


    # client
    path('create-client/', ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/update/', ClientUpdateView.as_view(), name='client_upd'),
    path('client-list/', ClientListView.as_view(), name='client_list'),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_del'),


    # MessageToMailing
    path('create-message-to-mail/', MessageToMailingCreate.as_view(), name='mail_create'),
    path('message-to-mail/<int:pk>/update/', MessageToMailingUpdateView.as_view(), name='message_upd'),
    path('message-to-mail/<int:pk>/delete/', MessageToMailingDeleteView.as_view(), name='mail_del'),
    # path('mail/<int:pk>/update/', MessageToMailingUpdateView.as_view(), name='Message_upd'),
    path('message-to-mail-list/', MessageToMailingListView.as_view(), name='mail_list'),



    # Logs
    path('mailing-logs/<int:pk>', MailingLogsListView.as_view(), name='mailing_log'),
    # path('all-mailing-logs/<int:pk>', MailingLogsListView.as_view(), name='all_mailing_log'),


    path('update_status/<int:pk>/', MailingStatusUpdateView.as_view(), name='update_status'),

    # moderator_kabinet
    path('moderator/', ModeratorViews.as_view(), name="moderator"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
