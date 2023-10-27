from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.


def base(request):
    """ Базовый шаблон с меню, футером и тд """
    context = {'title': 'Dinnland-subs'}
    # return render(request, 'subs/base1.html', context)
    return render(request, 'subs/base.html', context)


