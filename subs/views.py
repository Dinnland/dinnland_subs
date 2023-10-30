from django.views.generic import TemplateView
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView, TemplateView, DeleteView

# from apps.blog.models import Blog
from subs.models import *
from subs.forms import *
# from subs.services import get_filter_user_group
#
#
def base(request):
    """ Базовый шаблон с меню, футером и тд """
    context = {'title': 'Dinnland-subs'}
    # return render(request, 'subs/base1.html', context)
    return render(request, 'subs/base.html', context)

#
#
class HomeListView(LoginRequiredMixin,  ListView):
    """Главная стр с TemplateView LoginRequiredMixin,  ListView"""
    model = MailingSettings

    template_name = 'subs/home.html'
    login_url = 'mail_app:not_authenticated'
#
#     def get_context_data(self, **kwargs):
#         context_data = super().get_context_data(**kwargs)
#         context_data['count_mail_all'] = MailingSettings.objects.all().count()
#         context_data['count_mail_active'] = MailingSettings.objects.filter(mailing_status__in=['started']).count()
#         context_data['count_clients'] = Client.objects.distinct().count()
#
#         context_data['bloga3'] = Blog.objects.all()[:3]
#         context_data['blog_last_3_date'] = Blog.objects.filter(sign_of_publication=True).order_by('-date_of_create')[:3]
#         context_data['user'] = self.request.user
#         return context_data
#
# def index_contacts(request):
#     """Стр с контактами"""
#     context = {
#         'header': 'Контакты'
#                }
#     return render(request, 'subs/contacts.html', context)
#
# # create ----------------------------------------------------------------
#
#
# class MailingSettingsCreateView(CreateView):
#     model = MailingSettings
#     form_class = MailingSettingsForm
#     template_name = 'subs/mailing_form.html'
#     success_url = reverse_lazy('mail_app:cabinet')
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs
#
#     def form_valid(self, form):
#         form.instance.owner = self.request.user
#         return super().form_valid(form)
#
#
# # class ClientCreateView(CreateView):
# #     model = Client
# #     form_class = ClientForm
# #     template_name = 'mail_app/mailing_form.html'
# #     success_url = reverse_lazy('mail_app:cabinet')
# #
# #     def form_valid(self, form):
# #         form.instance.owner = self.request.user
# #         return super().form_valid(form)
#
#
# # class MessageToMailingCreate(CreateView):
# #     model = MessageToMailing
# #     form_class = MessageToMailingForm
# #     template_name = 'mail_app/mailing_form.html'
# #     success_url = reverse_lazy('mail_app:cabinet')
# #
# #     def form_valid(self, form):
# #         form.instance.owner = self.request.user
# #         return super().form_valid(form)
#
#
# # list ----------------------------------------------------------------
#
#
# # class MailingSettings1ListView(LoginRequiredMixin, ListView):
# #     """Главная стр с продуктами"""
# #     model = MailingSettings
# #     template_name = 'mail_app/mailingsettings_list.html'
# #     context_object_name = 'mailing_list'
# #
# #     # Ограничение доступа анонимных пользователей
# #     login_url = 'catalog:not_authenticated'
# #     def get_queryset(self):
# #         """Ограничение:модератор видит все рассылки, юзер только свои"""
# #         if self.request.user.groups.filter(name='moderator'):
# #             queryset = MailingSettings.objects.all()
# #         else:
# #             queryset = MailingSettings.objects.filter(owner_id=self.request.user.pk)
# #
# #
# #         owner_id = self.request.user.pk
# #         state = self.request.GET.get('status')
# #         if self.request.GET.get('status'):
# #             queryset = MailingSettings.objects.filter(owner_id=owner_id)
# #
# #
# #         return queryset
# #
# #     def get_context_data(self, **kwargs):
# #         context = super().get_context_data(**kwargs)
# #         context['filter_form'] = MailingFilterForm(self.request.GET)
# #         return context
#
#
#
# # class ClientListView(LoginRequiredMixin, ListView):
# #     model = Client
# #     template_name = 'mail_app/client_list.html'
# #     context_object_name = 'client_list'
# #
# #     def get_queryset(self):
# #         """Ограничение:модератор видит всех клиентов , юзер только своих"""
# #         if self.request.user.groups.filter(name='moderators'):
# #             queryset = Client.objects.all()
# #         else:
# #             queryset = Client.objects.filter(owner_id=self.request.user.pk)
# #         return queryset
# #
# #
# # class MessageToMailingListView(LoginRequiredMixin, ListView):
# #     model = MessageToMailing
# #     template_name = 'mail_app/message_to_mailing_list.html'
# #     context_object_name = 'mail_list'
# #
# #     def get_queryset(self):
# #         """Ограничение:модератор видит все сообщения, юзер только свои"""
# #         if self.request.user.groups.filter(name='moderators'):
# #             queryset = MessageToMailing.objects.all()
# #         else:
# #             queryset = MessageToMailing.objects.filter(owner_id=self.request.user.pk)
# #         return queryset
#
#
# # update ----------------------------------------------------------------
#
#
# # class MailingSettingsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
# #     model = MailingSettings
# #     # form_class = MailingSettingsForm
# #     template_name = 'mail_app/mailing_form.html'
# #     success_url = reverse_lazy('mail_app:cabinet')
# #     # success_url = reverse_lazy('mail_app:home')
# #
# #
# #     def form_valid(self, form):
# #         if form.instance.owner == self.request.user:
# #             form = super().form_valid(form)
# #         else:
# #             form = MailingSettingsFormNotUser
# #             return form
# #
# #     def get_queryset(self):
# #         """Ограничение:модератор видит все рассылки, юзер только свои"""
# #         if self.request.user.groups.filter(name='moderators'):
# #             queryset = MailingSettings.objects.all()
# #         else:
# #             queryset = MailingSettings.objects.filter(owner_id=self.request.user.pk)
# #         # return queryset
# #
# #         owner_id = self.request.user.pk
# #         # state = self.request.GET.get('status')
# #         if self.request.GET.get('status'):
# #             queryset = MailingSettings.objects.filter(owner_id=owner_id)
# #         return queryset
# #     def get_form_class(self, queryset=None):
# #         """Тут в зависимости от группы юзера выводятся разные формы продукта"""
# #         self.object = super().get_object(queryset)
# #         form_class = get_filter_user_group(del_group='moderator', user=self.request.user)
# #         return form_class
# #
# #     def test_func(self):
# #             return self.request.user == self.get_object().owner
#
#
# # class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
# #     model = Client
# #     form_class = ClientForm
# #     template_name = 'mail_app/mailing_form.html'
# #     success_url = reverse_lazy('mail_app:client_list')
# #
# #     def form_valid(self, form):
# #         form.instance.owner = self.request.user
# #         return super().form_valid(form)
# #
# #     def test_func(self):
# #         return self.request.user == self.get_object().owner
#
#
# # class MessageToMailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
# #     model = MessageToMailing
# #     form_class = MessageToMailingForm
# #     template_name = 'mail_app/mailing_form.html'
# #     success_url = reverse_lazy('mail_app:mail_list')
# #
# #     def form_valid(self, form):
# #         form.instance.owner = self.request.user
# #         return super().form_valid(form)
# #
# #     def test_func(self):
# #         return self.request.user == self.get_object().owner
#
# # delete ----------------------------------------------------------------
#
#
# # class MailingSettingsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
# #     model = MailingSettings
# #     template_name = 'mail_app/confirm_delete.html'
# #     success_url = reverse_lazy('mail_app:cabinet')
# #
# #     def test_func(self):
# #         return self.request.user == self.get_object().owner
# #
# #
# # class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
# #     model = Client
# #     template_name = 'mail_app/confirm_delete.html'
# #     success_url = reverse_lazy('mail_app:client_list')
# #
# #     def test_func(self):
# #         return self.request.user == self.get_object().owner
# #
# #
# # class MessageToMailingDeleteView(LoginRequiredMixin, DeleteView):
# #     # UserPassesTestMixin,
# #     model = MessageToMailing
# #     template_name = 'mail_app/confirm_delete.html'
# #     success_url = reverse_lazy('mail_app:mail_list')
# #
# #     def test_func(self):
# #         return self.request.user == self.get_object().owner
#
#
# # other -------------------------------------------------------------------------
#
#
# class ProfileDataView(TemplateView):
#     template_name = 'mail_app/cabinet.html'
#
#     def get_context_data(self, **kwargs):
#         context_data = super().get_context_data(**kwargs)
#         owner_id = self.request.user.pk
#         context_data['count_mailing_all'] = MailingSettings.objects.filter(owner_id=owner_id).count()
#         context_data['count_mailing_active'] = MailingSettings.objects.filter(mailing_status__in=['started'],
#                                                                               owner_id=owner_id).count()
#         context_data['count_mail_massage'] = MessageToMailing.objects.filter(owner_id=owner_id).count()
#         context_data['count_clients'] = Client.objects.filter(owner_id=owner_id).count()
#         return context_data
#
#
# class CabinetView(TemplateView):
#     template_name = 'mail_app/cabinet.html'
#
#     def get(self, request, *args, **kwargs):
#
#         profile_data_view = ProfileDataView()
#         profile_data_view.request = request
#         profile_context = profile_data_view.get_context_data(**kwargs)
#
#         # mailing_list_view = MailingListView()
#         mailing_list_view = MailingSettings1ListView()
#
#         mailing_list_view.request = request
#         queryset = mailing_list_view.get_queryset()
#         count_mailing_all = queryset.count()
#         mailing_context = {
#             'mailing_list': queryset,
#             'count_mailing_all': count_mailing_all,
#         }
#
#         combined_context = {**profile_context, **mailing_context}
#         combined_context['filter_form'] = MailingFilterForm(request.GET)
#
#         return render(request, self.template_name, combined_context)
#
#
# class ModeratorViews(UserPassesTestMixin, TemplateView):
#     template_name = 'mail_app/moderators.html'
#
#     def test_func(self):
#         f = self.request.user.groups.filter(name='moderator').exists()
#         return f
#
#     def get_context_data(self, **kwargs):
#         context_data = super().get_context_data(**kwargs)
#         return context_data
#
#
# class MailingStatusUpdateView(View):
#     def post(self, request, *args, **kwargs):
#         mailing_id = kwargs['pk']
#         new_status = request.POST.get('new_status')
#         mailing = MailingSettings.objects.get(pk=mailing_id)
#         mailing.mailing_status = new_status
#         mailing.save()
#
#         return redirect('mail_app:cabinet')
#
#
# class NotAuthenticated(ListView):
#     """not_authenticated"""
#     model = MailingSettings
#     template_name = 'mail_app/not_authenticated.html'
