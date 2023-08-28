from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from board.forms import ArticleForm, CommunicationForm, C_CommentForm, CounselorReviewForm
from board.models import Article, Communication, Comment, C_Comment, CounselorReview
from django.contrib.auth.decorators import login_required, permission_required

from users.models import Counselor, Patient
from users.permissions import UserGroups, PermissionType, get_permission_name


# 파일 업로드 게시판
def a_list(request):
    articles = Article.objects.all().order_by('-id')

    article_per_page = 1

    paginator = Paginator(articles, article_per_page)

    page_number = request.GET.get('page')

    page = paginator.get_page(page_number)

    context = {'articles': articles, 'page': page}

    return render(request, 'Picture-list.html', context)


@login_required(login_url='users:login-patient', redirect_field_name='board:a_create')
@permission_required('board.view_article')
def a_detail(request, id):
    user = request.user
    article = Article.objects.get(pk=id)
    if UserGroups.patient_group in user.groups.all() and not article.a_patient in user.patient_set.all():
        raise PermissionDenied
    context = {'article': article}
    return render(request, 'Picture-detail.html', context)


@login_required(login_url='users:login-patient', redirect_field_name='board:a_create')
@permission_required('board.add_article')
def a_create(request):
    if request.method == 'POST':
        article_form = ArticleForm(data=request.POST, files=request.FILES)
        if article_form.is_valid():
            article_form.save()
            return redirect('board:a_list')
    else:
        article_form = ArticleForm(a_writer=request.user)

    return render(request, 'Picture-create.html', {'article_form': article_form})


# 소통게시판
@login_required(login_url='users:login-patient', redirect_field_name='board:c_list')
@permission_required('board.view_communication')
def c_list(request):
    # 게시글 모두 가져와서 화면에 출력하는 일을 한다.
    communications = Communication.objects.all().order_by('-id')

    communication_per_page = 1

    paginator = Paginator(communications, communication_per_page)

    page_number = request.GET.get('page')

    page = paginator.get_page(page_number)

    context = {'communications': communications, 'page': page}

    return render(request, 'Communication-List.html', context)


@login_required(login_url='users:login-patient', redirect_field_name='board:c_detail')
@permission_required(['board.add_communication', 'board.change_communication'])
def c_detail(request, id):
    # 특정 id에 해당하는 Communication 객체 가져오기
    communication = get_object_or_404(Communication, pk=id)
    comments = C_Comment.objects.filter(communication=communication)
    print(comments)
    if request.method == 'POST':
        c_comment_form = C_CommentForm(request.POST)
        if c_comment_form.is_valid():
            new_comment = c_comment_form.save(commit=False)
            new_comment.cc_commenter = request.user
            new_comment.communication = communication
            new_comment.save()
        return redirect('board:c_detail', id=id)
    else:
        # GET 요청일 때 CommentForm을 초기화
        c_comment_form = C_CommentForm()

    context = {'communication': communication, 'comments': comments, 'c_comment_form': c_comment_form}

    return render(request, 'Communication-detail.html', context)


@login_required(login_url='users:login-patient', redirect_field_name='board:a_create')
@permission_required(['board.add_communication', 'board.change_communication'])
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
@login_required(login_url='users:choose_your_type', redirect_field_name='board:cs_list')
def cs_list(request):
    counselors = Counselor.objects.all().order_by('-id')

    counselor_per_page = 1

    paginator = Paginator(counselors, counselor_per_page)

    page_number = request.GET.get('page')

    page = paginator.get_page(page_number)

    context = {'counselors': counselors, 'page': page}

    return render(request, 'Counselor-list.html', context)


@login_required(login_url='users:login-patient', redirect_field_name='board:cs_list')
def cs_detail(request, id):
    if not request.user.is_authenticated:
        return redirect('home')  # 로그인 페이지 URL로 변경하세요.
    counselor = Counselor.objects.get(pk=id)
    # TODO : 수정 필요
    reviews = counselor.counselorreview_set.all()
    # required_permission = get_permission_name(CounselorReview, PermissionType.ADD)
    if request.method == 'POST' and request.user.has_perm('board.add_counselor review'):
        reviewform = CounselorReviewForm(request.POST)
        if reviewform.is_valid():
            review = reviewform.save(commit=False)
            review.r_counselor = counselor
            review.save()
            return redirect('board:cs_detail', id=id)
    else:
        reviewform = CounselorReviewForm()

    context = {'counselor': counselor, 'reviews': reviews, 'reviewform': reviewform}
    return render(request, 'Counselor-detail.html', context)


def main(request):
    counselors = Counselor.objects.all().order_by('-id')
    context = {'counselors': counselors}
    return render(request, 'Main.html', context)
