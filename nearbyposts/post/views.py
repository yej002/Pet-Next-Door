from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Post
from .services import get_nearby_posts_within
from .serializer import PostSerializer


# create a class for view of the post
class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# using function of get_nearby_posts_within() to calculate distance
# and return the posts as response
# defensive coding for validation
    def list(self, request):
        latitude = self.request.query_params.get('lat')
        longitude = self.request.query_params.get('lng')
        if latitude and longitude:
            posts = get_nearby_posts_within(
                latitude=float(latitude),
                longitude=float(longitude),
                km=10,  # radius in kilometers
                limit=100  # page size
            )
        else:
            raise ValidationError('Longitude and Latitude are required parameters.')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
