from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from board.forms import ArticleForm, CommunicationForm, CommentForm
from board.models import Article, Communication
from django.contrib.auth.decorators import login_required


def a_list(request):
    articles = Article.objects.all().order_by('-id')
    context = {'articles': articles}
    return render(request, 'Picture-list.html', context)


def a_create(request):
    if request.method == 'POST':
        article_form = ArticleForm(data=request.POST, files=request.FILES)

        if article_form.is_valid():
            new_post = article_form.save(commit=False)
            new_post.save()
            return redirect('board:a_list')

    else:

        article_form = ArticleForm()

    return render(request, 'Picture-create.html', {'article_form': article_form})


def c_list(request):
    # 게시글 모두 가져와서 화면에 출력하는 일을 한다.
    communications = Communication.objects.all().order_by('-id')
    context = {'communications': communications}
    return render(request, 'Communication-List.html', context)


def c_create(request):
    if request.method == 'POST':
        communication_form = CommunicationForm(request.POST)

        if communication_form.is_valid():
            new_post = communication_form.save(commit=False)
            new_post.save()
            return redirect('board:c_list')
    else:
        communication_form = CommunicationForm()

    return render(request, 'Communication-Create.html', {'communication_form': communication_form})


@login_required
def communication_combined(request):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_post = comment_form.save(commit=False)
            new_post.commenter = request.user
            new_post.save()
            return HttpResponseRedirect(reverse('Communication-detail'))
    else:
        comments = Communication.objects.all().order_by('-id')
        comment_form = CommentForm()
        context = {'comments': comments, 'comment_form': comment_form}
        return render(request, 'Communication-detail.html', context)

# def comment_list(request):
#     comments = Communication.objects.all().order_by('-id')
#     context = {'comments': comments}
#     return render(request, 'Communication-detail.html', context)
#
#
# def commnet_create(request):
#     if request.method == 'POST':
#         comment_form = CommentForm(request.POST)
#
#         if comment_form.is_valid():
#             new_post = comment_form.save(commit=False)
#             new_post.save()
#             return redirect('board:c_list')
#     else:
#         comment_form = CommentForm()
#
#     return render(request, 'Communication-detail.html', {'comment_form': comment_form})
