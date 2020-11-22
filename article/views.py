from django.shortcuts import render, redirect
from .models import ArticlePost
from django.contrib.auth.models import User
import markdown
from django.http import HttpResponse
from .forms import ArticlePostForm


# Create your views here.
def article_list(request):
    # 从ArticlePost取出所有文章
    articles = ArticlePost.objects.all()
    # 前面的'articles'只是一个命名，在模板中通过这个命名获取传过去的数据，你也可以改成别的
    # 后面的articles是上一行代码中获得的所有文章
    context = { 'articles': articles }
    # 第一个参数是固定的request。第二个参数是指定要把数据传输到哪个模板,
    # 即article文件夹下面的list.html。第三个参数是要传输的数据。
    return render(request, 'article/list.html', context)

def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)

    article.body = markdown.markdown(article.body,
        extensions = [
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        ])

    context = { 'article': article }

    return render(request, 'article/detail.html', context)

def article_create(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=1)
            new_article.save()
            return redirect("article:article_list")
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        article_post_form = ArticlePostForm()
        context = { 'article_post_form': article_post_form }
        return render(request, 'article/create.html', context)


def article_delete(request, id):
    article = ArticlePost.objects.get(id=id)
    article.delete()
    return redirect("article:article_list")