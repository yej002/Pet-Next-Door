from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Post
from .services import get_nearby_posts_within
from .serializer import PostSerializer


# View for Post application
class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request):
        """
        Default handler for GET method of Post
        This is exposed as an API using the Django Rest Framework
        This method looks up posts near the input location (lat, lng)
        @param request: HTTP request expected to contain lat and lng as the location
        @return: a list of posts near the input location
        """
        latitude = self.request.query_params.get('lat')
        longitude = self.request.query_params.get('lng')
        if latitude and longitude:
            posts = get_nearby_posts_within(
                latitude=float(latitude),
                longitude=float(longitude),
                distance=10,  # radius in kilometers
                limit=100  # page size
            )
        else:
            raise ValidationError('Longitude and Latitude are required parameters.')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
