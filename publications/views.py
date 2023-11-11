from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from rest_framework.permissions import IsAuthenticated
from publications.forms import *
from pytils.translit import slugify
from django.urls import reverse_lazy, reverse
from users.models import User


def base(request):
    """ Базовый шаблон с меню, футером и тд """
    context = {'title': 'Dinnland-publications'}
    return render(request, 'publications/base.html', context)


class HomeListView(LoginRequiredMixin,  ListView):
    """Главная стр с TemplateView LoginRequiredMixin,  ListView"""
    model = Publication
    template_name = 'publications/includes/home.html'
    login_url = 'publications:not_authenticated'


class PublicationListView(LoginRequiredMixin, ListView):
    """Список публикаций"""
    model = Publication
    template_name = 'publications/publication_list.html'
    context_object_name = 'publication_list'

    def get_queryset(self, queryset=None, *args, **kwargs):
        """Метод для вывода ТОЛЬКО опубликованных публикаций"""
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(sign_of_publication=True)
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['publication_all'] = Publication.objects.all().order_by('-date_of_create')
        context_data['publication_last_3_date'] =\
            Publication.objects.filter(sign_of_publication=True).order_by('-date_of_create')[:3]
        if self.request.user.groups.first() == 'moderator':
            context_data['qwerty'] = 'moderator'
        elif self.request.user.groups.first() == 'Moderator':
            context_data['qwerty'] = 'Moderator'
        else:
            context_data['qwerty'] = 'ne moderator'
        context_data['user_gr_name'] = self.request.user.groups.name
        context_data['user_gr_first'] = self.request.user.groups.first()
        return context_data


class AuthorPublicationListView(LoginRequiredMixin, ListView):
    """Список публикаций конкретного автора"""
    model = Publication
    template_name = 'publications/author_publication_list.html'
    context_object_name = 'author_publication_list'

    def get_queryset(self, queryset=None, *args, **kwargs):
        """Метод для вывода Для конкретного автора опубликованных публикаций"""
        author_pk = self.kwargs.get('pk')
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(sign_of_publication=True)
        queryset = queryset.filter(owner=author_pk).order_by('-date_of_create')
        return queryset

    def get_context_data(self, **kwargs):
        author_pk = self.kwargs.get('pk')
        context_data = super().get_context_data(**kwargs)
        context_data['author_publication_all'] = Publication.objects.filter(owner=author_pk)
        context_data['author_pk'] = User.objects.filter(pk=author_pk)
        return context_data


class PublicationCreateView(LoginRequiredMixin, CreateView):
    """Страница для создания публикации"""
    model = Publication
    form_class = PublicationForm
    permission_classes = [IsAuthenticated]
    success_url = reverse_lazy('publications:publication_list')

    def form_valid(self, form):
        """Динамическое формирование Slug, присвоение хозяина публикации"""
        if form.is_valid():
            form.instance.owner = self.request.user
            new_publication = form.save()
            new_publication.slug = slugify(new_publication.header)
            new_publication.save()
        return super().form_valid(form)


class PublicationDetailView(LoginRequiredMixin, DetailView):
    """Страница с публикацией"""
    model = Publication

    def get_object(self, queryset=None):
        """Метод для подсчета просмотров"""

        self.object = super().get_object(queryset)
        self.object.quantity_of_views += 1
        self.object.save()
        return self.object

    def get_success_url(self):
        return reverse('publications:viewpublication', args=[self.kwargs.get('pk')])


class PublicationUpdateView(LoginRequiredMixin, UpdateView):
    """Страница для Изменения блога"""
    model = Publication
    form_class = PublicationForm

    def form_valid(self, form):
        """Динамическое формирование Slug"""
        if form.is_valid():
            form.instance.owner = self.request.user
            new_publication = form.save()
            new_publication.slug = slugify(new_publication.header)
            new_publication.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('publications:viewpublication', args=[self.kwargs.get('pk')])


class PublicationDeleteView(LoginRequiredMixin, DeleteView):
    """Страница для удаления блога"""
    model = Publication
    success_url = reverse_lazy('publications:publication_list')

    # def get_queryset(self, queryset=None, *args, **kwargs):
    #     """Метод для вывода ТОЛЬКО опубликованных публикаций"""
    #     queryset = super().get_queryset(*args, **kwargs)
    #     queryset = queryset.filter(sign_of_publication=True)
    #     return queryset


class NotAuthenticated(ListView):
    """not_authenticated"""
    model = Publication
    template_name = 'publications/not_authenticated.html'
