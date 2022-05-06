from django.http import HttpResponseRedirect
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from post.services import get_my_posts, create_post, PostForm


# create a view of homepage
class HomePageView(viewsets.GenericViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home/index.html'

# list of user's post and list a form for creat post
    def list(self, request):
        username = self.request.query_params.get('username')
        posts = get_my_posts(username)
        post_form = PostForm(initial={"creator": username})
        return Response({'username': username, 'posts': posts, 'form': post_form})

# create a post with following attributes
# defensive code with validation
    def create(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            tags = form.cleaned_data.get('tags')
            longitude = form.cleaned_data.get('longitude')
            latitude = form.cleaned_data.get('latitude')
            creator = form.cleaned_data.get('creator')
            create_post(title, content, tags, longitude, latitude, creator)
            return HttpResponseRedirect('/home/?username=' + creator)
        else:
            username = self.request.data.get('creator')
            posts = get_my_posts(username)
            return Response({'username': username, 'posts': posts, 'form': form})

