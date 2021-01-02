from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from article.models import ArticlePost
from .forms import CommentForm
from .models import Comment

# 文章评论
@login_required(login_url='/userprofile/login/')
def post_comment(request, article_id, parent_comment_id=None):
    article = get_object_or_404(ArticlePost, id=article_id)
    # get_object_or_404(): 它和module.objects.get()功能类似。区别是在生产环境下，如果用户请求一个不存在的对象时，module.objects.get()会返回error500(服务器内部错误), 而get_object_or_404 会返回Error404。 相比之下，返回404错误更加准确。
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user

            # 二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                # 如果回复层级超过两级，则转换为两级
                new_comment.parent_id = parent_comment.get_root().id
                # 被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                return HttpResponse('200 OK')
            new_comment.save()
            return redirect(article)
            # redirect(): 返回到一个适当的URL中： 即用户发表评论后, 重新定向到文章详情页面。 当其中的参数是一个model对象时, 会自动调用这个Model对象的get_absolute_url()方法。因此马上修改article的模型。
        else:
            return HttpResponse('表单填写有误，请重新填写。')
    # 处理GET请求
    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'article_id': article_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comment/reply.html', context)
    # 处理其他请求
    else:
        return HttpResponse('仅接受 POST/GET 请求')

