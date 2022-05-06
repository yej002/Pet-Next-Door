from rest_framework import serializers
from post.models import Post


#  Custom serializer to serialize Post when returning as http response
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id',
                  'created_at',
                  'updated_at',
                  'title',
                  'creator',
                  'content',
                  'comment',
                  'image_content',
                  'tags',
                  'liked_count',
                  'latitude',
                  'longitude']
