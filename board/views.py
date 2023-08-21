from django.shortcuts import render, redirect

from board.forms import ArticleForm
from board.models import Article


def a_list(request):
    articles = Article.objects.all().order_by('-id')
    context = {'articles': articles}
    return render(request, 'Picture-list.html', context)


def a_create(request):
    if request.method == 'POST':
        article_form = ArticleForm(data=request.POST, files=request.FILES)

        print(request.FILES)

        if article_form.is_valid():
            new_post = article_form.save(commit=False)
            new_post.save()
            return redirect('board:a_list')

    else:

        article_form = ArticleForm()

    return render(request, 'Art-list.html', {'article_form': article_form})

# def article_add(request):
#     form = ArticleForm()
#     a_content = {"form": form}
#
#     if request.method == "POST":
#         a_title = request.POST["title"]
#         a_content = request.POST["content"]
#         a_tree_image = request.FILES["a_tree_image"]
#         a_man_image = request.FILES["a_man_image"]
#         a_woman_image = request.FILES["a_woman_image "]
#         a_house_image = request.FILES["a_house_image"]
#
#         article = Article.objects.create(
#             title=a_title,
#             content=a_content,
#             a_tree_image=a_tree_image,
#             a_man_image=a_man_image,
#             a_woman_image=a_woman_image,
#             a_house_image=a_house_image
#         )
#     return render(request, "templates/Art-list.html", a_content)
