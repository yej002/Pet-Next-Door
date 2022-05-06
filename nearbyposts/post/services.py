from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import fromstr
from django.forms import ModelForm, Textarea, HiddenInput
from .models import Post


#  PostForm class based on Django ModelForm
class PostForm(ModelForm):
    class Meta:
        model = Post
        #  build form with the below fields
        fields = ('title', 'content', 'longitude',
                  'latitude', 'tags', 'creator')
        # hide creator field (creator assigned during form creation)
        widgets = {
            'content': Textarea(attrs={'rows': 3}),
            'creator': HiddenInput()
        }


def get_posts_by_user(username: str):
    """
    get posts created by the given username
    @param username: the target username
    @return: a list of posts created by the target username
    """
    return Post.objects.filter(creator=username).order_by('created_at')


def get_nearby_posts_within(latitude: float, longitude: float,
                            distance: int = 1, limit: int = None, srid: int = 4326):
    """
    get posts within the distance from the input location

    @param latitude: latitude of the target location
    @param longitude: longitude of the target location
    @param distance: the radius of the area to search posts in
    @param limit: maximum number of posts
    @param srid: coordinates system spatial reference identifier
    @return: a list of posts within the radius sorted by distance
    """
    coordinates = Point(longitude, latitude, srid=srid)
    point = GEOSGeometry(coordinates, srid=4326)
    return Post.objects.alias(distance=Distance('location',
                                                coordinates)).filter(location__distance_lte=(point,
                                                                                             D(km=distance))).order_by(
        'distance')[0:limit]


def create_post(title: str, content: str, tags: list,
                longitude: str, latitude: str, creator: str):
    """
    create a post object in the database
    @param title: title of the post
    @param content: content of the post
    @param tags: tags of the post
    @param longitude: longitude of the post
    @param latitude: latitude of the post
    @param creator: creator of the post
    @return: the created post
    """
    post = Post(
        title=title,
        content=content,
        tags=tags,
        longitude=longitude,
        latitude=latitude,
        creator=creator,
        # store an extra location for distance calculation
        location=fromstr(f'POINT({longitude} {latitude})', srid=4326)
    )
    post.save()
    return post
