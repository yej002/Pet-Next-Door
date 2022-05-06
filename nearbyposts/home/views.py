from django.http import HttpResponseRedirect
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from post.services import get_posts_by_user, create_post, PostForm


# View to handle homepage requests
class HomePageView(viewsets.GenericViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home/index.html'

    def list(self, request):
        """
        Home page GET method handler
        @param request: input request expected to contain a username for the current user
        @return: all necessary info for the template to render (username, user's posts, post creation form)
        """
        username = self.request.query_params.get('username')
        posts = get_posts_by_user(username)  # fetch all posts created by username
        post_form = PostForm(initial={"creator": username})  # build post creation form
        return Response({'username': username, 'posts': posts, 'form': post_form})

    #
    def create(self, request):
        """
        Home page POST method handler - post creation
        @param request: input request which contains the data collected from the form
        @return: created Post object
        """
        form = PostForm(request.POST)  # bound the form with input data
        if form.is_valid():  # validate the input
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            tags = form.cleaned_data.get('tags')
            longitude = form.cleaned_data.get('longitude')
            latitude = form.cleaned_data.get('latitude')
            creator = form.cleaned_data.get('creator')
            create_post(title, content, tags, longitude, latitude, creator)  # store the post
            return HttpResponseRedirect('/home/?username=' + creator)
        else:  # invalid data; form now contains error information
            username = self.request.data.get('creator')
            posts = get_posts_by_user(username)
            return Response({'username': username, 'posts': posts, 'form': form})
