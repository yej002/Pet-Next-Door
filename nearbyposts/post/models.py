from django.db import models
from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator


# Post model
class Post(models.Model):
    id = models.BigAutoField(primary_key=True)  # unique identifier
    created_at = models.DateTimeField(auto_now_add=True)  # created at timestamp
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    creator = models.CharField(max_length=20)  # user who created the post
    content = models.CharField(max_length=2000)
    comment = ArrayField(models.CharField(max_length=200), default=list, blank=True)
    image_content = models.CharField(max_length=2000, blank=True)  # img url
    tags = ArrayField(models.CharField(max_length=20), default=list, blank=True)  # tags on the post
    liked_count = models.IntegerField(default=0)  # number of likes received
    latitude = models.FloatField(null=True, validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)])
    longitude = models.FloatField(null=True, validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)])
    location = models.PointField(null=True)  # GeoDjango Point field - contains longitude and latitude
