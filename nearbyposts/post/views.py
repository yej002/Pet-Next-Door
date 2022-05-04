from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from .models import Post
from .services import get_nearby_posts_within, create_post, get_post_form
from .serializer import PostSerializer
from django.http import HttpResponseRedirect, HttpResponse

class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request):
        latitude = self.request.query_params.get('lat')
        longitude = self.request.query_params.get('lng')
        if latitude and longitude:
            posts= get_nearby_posts_within(
                latitude=float(latitude),
                longitude=float(longitude),
                km=3, # radius in kilometers
                limit=100 # page size
            )
        else:
            # TODO: fix this error handling
            pass
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request):
        title = self.request.data.get('title')
        content = self.request.data.get('content')
        tags = self.request.data.get('tags')
        if tags:
            tags = tags.split(',')
        else:
            tags = list()
        longitude = self.request.data.get('longitude')
        latitude = self.request.data.get('latitude')
        creator = self.request.data.get('creator')
        post = create_post(title, content, tags, longitude, latitude, creator)
        return HttpResponseRedirect('/home/?username=' + creator)
        # form = get_post_form(request.POST)
        # check whether it's valid:
        # if form.is_valid():
        #     title = form.cleaned_data.get('title')
        #     content = form.cleaned_data.get('content')
        #     tags = form.cleaned_data.get('tags')
        #     longitude = form.cleaned_data.get('longitude')
        #     latitude = form.cleaned_data.get('latitude')
        #     creator = form.cleaned_data.get('creator')
        #     post = create_post(title, content, tags, longitude, latitude, creator)
        #     return HttpResponseRedirect('/home/?username=' + creator)
        # else:
        #     # TODO: Fix form validation
        #     creator = form.cleaned_data.get('creator')
        #     return Response({'username': creator, 'form': form})

