from django.shortcuts import render
from .models import ArticlePost
# Create your views here.
def article_list(request):
    # 从ArticlePost取出所有文章
    articles = ArticlePost.object.all()
    # 前面的'articles'只是一个命名，在模板中通过这个命名获取传过去的数据，你也可以改成别的
    # 后面的articles是上一行代码中获得的所有文章
    context = { 'articles': articles }
    # 第一个参数是固定的request。第二个参数是指定要把数据传输到哪个模板,
    # 即article文件夹下面的list.html。第三个参数是要传输的数据。
    return render(request, 'article/list.html', context)