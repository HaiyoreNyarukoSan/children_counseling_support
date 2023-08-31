from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from pyexpat.errors import messages

from analyzer.views import analyzer
from board.forms import ArticleForm, CommunicationForm, C_CommentForm, CounselorReviewForm, EditArticleForm
from board.models import Article, Communication, C_Comment, CounselorReview, Mentalstate
from django.contrib.auth.decorators import login_required, permission_required

from chat.forms import RoomForm
from users.models import Counselor
from users.permissions import UserGroups


# 파일 업로드 게시판
def a_list(request):
    articles = Article.objects.all().order_by('-id')

    article_per_page = 3

    paginator = Paginator(articles, article_per_page)

    page_number = request.GET.get('page')

    page = paginator.get_page(page_number)

    context = {'articles': articles, 'page': page}

    return render(request, 'Picture-list.html', context)


@login_required(login_url='users:login-patient', redirect_field_name='board:a_create')
@permission_required('board.view_article')
def a_detail(request, id):
    user = request.user
    article = get_object_or_404(Article, pk=id)
    if UserGroups.patient_group in user.groups.all() and not article.a_patient in user.patient_set.all():
        raise PermissionDenied

    if request.method == 'POST':
        if 'delete' in request.POST:
            # 삭제 버튼이 눌렸을 때
            article.delete()
            return redirect('board:a_list')

        editart_form = ArticleForm(request.POST, instance=article)  # POST 요청 시 폼에 데이터 채우기

        if editart_form.is_valid():
            editart_form.save()  # 수정 내용 저장
            return redirect('board:a_detail', id=id)
    else:
        editart_form = ArticleForm(instance=article)  # GET 요청 시 폼 초기화

    context = {
        'article': article,
        'editart_form': editart_form,
    }
    return render(request, 'Picture-detail.html', context)


@login_required(login_url='users:login-patient', redirect_field_name='board:a_create')
@permission_required('board.add_article')
def a_create(request):
    if request.method == 'POST':
        article_form = ArticleForm(data=request.POST, files=request.FILES)
        if article_form.is_valid():
            article = article_form.save()
            images = [article.a_tree_image, article.a_man_image, article.a_woman_image, article.a_house_image]
            total_score = analyzer(images)
            article.mentalstate = Mentalstate.objects.create(
                m_article=article,
                aggression=total_score['공격성'],
                anxiety=total_score['불안감'],
                dependency=total_score['의존성'],
                stress=total_score['스트레스'],
                timidity=total_score['소심함'],
                sociability=total_score['사회성'],
                depression=total_score['우울감'],
                independence=total_score['독립성'],
                achievement=total_score['성취감'],
                selfish=total_score['이기적인'])
            article.save()
            return redirect('board:a_detail', id=article.id)
    else:
        article_form = ArticleForm(a_writer=request.user)

    return render(request, 'Picture-create.html', {'article_form': article_form})


# 소통게시판
@login_required(login_url='users:login-patient', redirect_field_name='board:c_list')
@permission_required('board.view_communication', raise_exception=403)
def c_list(request):
    # 게시글 모두 가져와서 화면에 출력하는 일을 한다.
    communications = Communication.objects.all().order_by('-id')

    communication_per_page = 6

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
    editcommunication_form = None

    if request.method == 'POST':
        if 'delete' in request.POST:
            communication.delete()
            return redirect('board:c_list')
        editcommunication_form = CommunicationForm(request.POST, instance=communication)
        if editcommunication_form.is_valid():
            editcommunication_form.save()
            return redirect('board:c_detail', id=id)

        # 삭제 버튼이 눌린 경우, 삭제할 comment를 찾아서 삭제
        if 'delete_comment' in request.POST:
            comment_id = request.POST.get('delete_comment')
            comment_to_delete = C_Comment.objects.get(pk=comment_id)
            comment_to_delete.delete()
            return redirect('board:c_detail', id=id)

        c_comment_form = C_CommentForm(request.POST)
        if c_comment_form.is_valid():
            new_comment = c_comment_form.save(commit=False)
            new_comment.cc_commenter = request.user
            new_comment.communication = communication
            new_comment.save()
        return redirect('board:c_detail', id=id)
    else:
        editcommunication_form = CommunicationForm(instance=communication)
        # GET 요청일 때 CommentForm을 초기화
        c_comment_form = C_CommentForm()

    context = {
        'communication': communication,
        'comments': comments,
        'c_comment_form': c_comment_form,
        'editcommunication_form': editcommunication_form
    }

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
    search_query = request.GET.get('q')
    counselors = Counselor.objects.all().order_by('-id')

    if search_query:
        counselors = counselors.filter(c_user__username__icontains=search_query)

    counselor_per_page = 3

    paginator = Paginator(counselors, counselor_per_page)

    page_number = request.GET.get('page')

    page = paginator.get_page(page_number)

    context = {'page': page, 'search_query': search_query}

    return render(request, 'Counselor-list.html', context)


@login_required(login_url='users:login-patient', redirect_field_name='board:cs_list')
def cs_detail(request, id):
    counselor = Counselor.objects.get(pk=id)
    reviews = counselor.counselorreview_set.all()
    # required_permission = get_permission_name(CounselorReview, PermissionType.ADD)
    if 'delete-review' in request.POST:
        review_id = request.POST.get('delete-review')
        try:
            review_to_delete = CounselorReview.objects.get(pk=review_id)
            review_to_delete.delete()
        except CounselorReview.DoesNotExist:
            messages.error(request, '선택한 리뷰를 찾을 수 없습니다.')
        return redirect('board:cs_detail', id=id)
    elif request.method == 'POST' and request.user.has_perm('board.add_counselor review'):
        reviewform = CounselorReviewForm(request.POST)
        if reviewform.is_valid():
            review = reviewform.save(commit=False)
            review.r_counselor = counselor
            review.save()
            return redirect('board:cs_detail', id=id)
    else:
        reviewform = CounselorReviewForm(reviewer=request.user)
        roomform = RoomForm(reviewer=request.user)

    context = {'counselor': counselor, 'reviews': reviews, 'reviewform': reviewform, 'roomform': roomform}
    return render(request, 'Counselor-detail.html', context)


def main(request):
    counselors = Counselor.objects.all().order_by('-id')
    context = {'counselors': counselors}
    return render(request, 'Main.html', context)


def counselor_search(request):
    search_query = request.GET.get('q')  # 검색어 가져오기
    search_terms = search_query.split()

    if search_query:
        # Counselor 모델에서 검색 수행
        counselors = Counselor.objects.filter(
            Q(c_user__last_name__iexact=search_terms[0]) |
            Q(c_user__first_name__iexact=search_terms[0]) |
            Q(c_user__last_name__iexact=' '.join(search_terms)) |
            Q(c_user__first_name__iexact=' '.join(search_terms))
        )
    else:
        counselors = []

    counselor_per_page = 3

    paginator = Paginator(counselors, counselor_per_page)

    page_number = request.GET.get('page')

    page = paginator.get_page(page_number)

    context = {
        'search_query': search_query,
        'page': page,
    }

    return render(request, 'Counselor-list.html', context)
