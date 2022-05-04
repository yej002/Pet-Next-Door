from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.apps import apps
from post.services import get_my_posts, get_post_form, create_post


class HomePageView(viewsets.GenericViewSet):  
    renderer_classes = [TemplateHTMLRenderer]  
    template_name = 'home/index.html'

    def list(self, request):
        username = self.request.query_params.get('username')
        posts = get_my_posts(username)
        post_form = get_post_form(None)
        return Response({'username': username, 'posts': posts, 'form': post_form})
