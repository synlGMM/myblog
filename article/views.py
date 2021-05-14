from django.shortcuts import render, redirect
from .models import ArticlePost, ArticleColumn
from django.contrib.auth.models import User
import markdown
from django.http import HttpResponse
from .forms import ArticlePostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# 引入Q对象
from django.db.models import Q
from comment.models import Comment
from comment.forms import CommentForm
from django.views import View

# Create your views here.
def article_list(request):
    # 根据GET请求中查询条件
    # 返回不同排序的对象数组
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')

    article_list = ArticlePost.objects.all()

    # 用户搜索逻辑
    if search:
        # 用 Q对象 进行联合搜索
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        # 将 search 参数重置为空
        search = ''

    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)

    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])

    if order == 'total_views':
        article_list = article_list.order_by('-total_views')

    paginator = Paginator(article_list, 3)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    # 前面的'articles'只是一个命名，在模板中通过这个命名获取传过去的数据，你也可以改成别的
    # 后面的articles是上一行代码中获得的页码文章
    context = { 'articles': articles, 'order': order, 'search': search, 'column': column, 'tag': tag}
    # 第一个参数是固定的request。第二个参数是指定要把数据传输到哪个模板,
    # 即article文件夹下面的list.html。第三个参数是要传输的数据。
    return render(request, 'article/list.html', context)

def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)
    comments = Comment.objects.filter(article=id)
    comment_form = CommentForm()
    # filter() 可以取出多个满足条件的对象，而get()只能取出一个，注意区分使用
    if request.user != article.author:
        article.total_views += 1
        article.save(update_fields=['total_views'])
    md = markdown.Markdown(
        extensions = [
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 目录扩展
        'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)

    context = { 'article': article, 'toc': md.toc, 'comments': comments, 'comment_form': comment_form,}

    return render(request, 'article/detail.html', context)

@login_required(login_url='/userprofile/login/')
def article_create(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            new_article.save()
            article_post_form.save_m2m()
            return redirect("article:article_list")
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        context = { 'article_post_form': article_post_form, 'columns': columns}
        return render(request, 'article/create.html', context)

@login_required(login_url='/userprofile/login/')
def article_delete(request, id):
    article = ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse('你没有权限进行此操作。')
    else:
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect("article:article_list")

@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        if request.user != article.author:
            return HttpResponse('抱歉，你无权删除这篇文章。')
        else:
            article.delete()
            return redirect("article:article_list")
    else:
        return HttpResponse('仅允许post请求')

@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    """
    更新文章的视图函数
    通过post方法提交表单，更新title，body字段
    GET方法进入初始表单页面
    id：文章的id
    """
    article = ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse('抱歉，你无权修改这篇文章。')
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
            if request.FILES.get('avatar'):
                article.avatar = request.FILES.get('avatar')
            article.tags.set(*request.POST.get('tags').split(','), clear=True)
            article.save()
            return redirect("article:article_detail", id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户 GET 请求获取数据
    elif request.method == 'GET':
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        context = { 'article': article, 'article_post_form': article_post_form, 'columns': columns, 'tags': ','.join([x for x in article.tags.names()]), 'avatar': article.avatar}
        return render(request, 'article/update.html', context )
    else:
        return HttpResponse('请使用GET或POST请求数据')

# 点赞数 +1
class IncreaseLikesView(View):
    """docstring for IncreaseLikesView"""
    def post(self, request, *arg, **kwargs):
        article = ArticlePost.objects.get(id=kwargs.get('id'))
        article.likes += 1
        article.save()
        return HttpResponse('success')