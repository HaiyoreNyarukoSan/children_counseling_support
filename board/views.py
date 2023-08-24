from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from board.forms import ArticleForm, CommunicationForm, C_CommentForm, CounselorReviewForm
from board.models import Article, Communication, Comment, C_Comment, CounselorReview
from django.contrib.auth.decorators import login_required

from users.models import Counselor, Patient


# 파일 업로드 게시판
def a_list(request):
    articles = Article.objects.all().order_by('-id')
    context = {'articles': articles}
    return render(request, 'Picture-list.html', context)


def a_detail(request, id):
    articles = Article.objects.filter(pk=id)
    context = {'articles': articles}
    return render(request, 'Picture-detail.html', context)


def a_create(request):
    if request.method == 'POST':
        article_form = ArticleForm(data=request.POST, files=request.FILES)

        if article_form.is_valid():
            # ArticleForm에 고른 환자를 받아서 new_post에 반영하기
            new_post = article_form.save(commit=False)
            new_post.a_patient = request.user.patient_set.first()
            new_post.save()
            return redirect('board:a_list')

    else:
        # TODO : 환자 목록도 보내서, ArticleForm에서 환자 1명 고를 수 있게 하기
        # patients = request.user.patient_set.all()
        # context={'patients':patients}
        article_form = ArticleForm()

    return render(request, 'Picture-create.html', {'article_form': article_form})


# 소통게시판
def c_list(request):
    # 게시글 모두 가져와서 화면에 출력하는 일을 한다.
    communications = Communication.objects.all().order_by('-id')
    context = {'communications': communications}
    return render(request, 'Communication-List.html', context)


def c_detail(request, id):
    # 특정 id에 해당하는 Communication 객체 가져오기
    communication = get_object_or_404(Communication, pk=id)
    comments = C_Comment.objects.filter(communication=communication)
    print(comments)
    if request.method == 'POST':
        if request.user.is_authenticated:  # 로그인한 사용자만 댓글을 작성할 수 있도록
            c_comment_form = C_CommentForm(request.POST)
            if c_comment_form.is_valid():
                new_comment = c_comment_form.save(commit=False)
                new_comment.cc_commenter = request.user
                new_comment.communication = communication
                new_comment.save()
            return redirect('board:c_detail', id=id)
        else:
            # 로그인되지 않은 사용자에게 어떻게 처리할지 결정하세요
            # 예를 들어 로그인 페이지로 리다이렉션하거나 에러 메시지를 표시할 수 있 습니다.
            pass
    else:
        # GET 요청일 때 CommentForm을 초기화
        c_comment_form = C_CommentForm()

    context = {'communication': communication, 'comments': comments, 'c_comment_form': c_comment_form}

    return render(request, 'Communication-detail.html', context)


def c_create(request):
    if request.method == 'POST':
        communication_form = CommunicationForm(request.POST)

        if communication_form.is_valid():
            new_post = communication_form.save(commit=False)
            new_post.com_patient = request.user.patient_set.first()
            new_post.save()
            return redirect('board:c_list')
    else:
        communication_form = CommunicationForm()

    return render(request, 'Communication-Create.html', {'communication_form': communication_form})


# 상담사 게시판
def cs_list(request):
    counselors = Counselor.objects.all().order_by('-id')
    context = {'counselors': counselors}
    return render(request, 'Counselor-list.html', context)


@login_required
def cs_detail(request, id):
    counselor = Counselor.objects.get(pk=id)
    reviews = counselor.counselorreview_set.all()

    if request.method == 'POST':
        reviewform = CounselorReviewForm(request.POST)
        if reviewform.is_valid():
            patient = get_object_or_404(Patient, p_user=request.user)
            content = reviewform.cleaned_data['r_content']
            # rating = reviewform.cleaned_data['r_rating']

            CounselorReview.objects.create(
                r_patient=patient,
                r_counselor=counselor,
                r_content=content,
                # r_rating=rating
            )
            return redirect('board:cs_detail', id=id)
    else:
        reviewform = CounselorReviewForm()

    context = {'counselor': counselor, 'reviews': reviews, 'reviewform': reviewform}
    return render(request, 'Counselor-detail.html', context)
