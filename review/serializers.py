from rest_framework import serializers
from .models import Like, Rating, Comment,LikeComment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    
    class Meta:
        model = Comment
        fields = '__all__'
    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        comment = Comment.objects.create(author=user, **validated_data)
        return comment


class RatingSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Rating
        fields = '__all__'
    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        rating = Rating.objects.create(author=user, **validated_data)
        return rating

    def validate_rating(self, rating):
        if  0 < rating < 6:
            raise serializers.ValidationError(
                'rating must be beetween 0 and 5')
        return rating
    
    def validate_product(self, product):
        if self.Meta.model.objects.filter(product=product).exists():
            raise serializers.ValidationError('Вы уже оставили рейтинг на этот продукт')
        return product  


 


class LikeSerializer(serializers.ModelSerializer):
    product = serializers.ReadOnlyField()
    author = serializers.ReadOnlyField()

    class Meta:
        model = Like
        fields = '__all__'
    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        like = Like.objects.create(author=user, **validated_data)
        return like
    

class LikeCommentSerializer(serializers.ModelSerializer):
    comment = serializers.ReadOnlyField()
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = LikeComment
        fields = '__all__'
    

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        likecomment = LikeComment.objects.create(author=user, **validated_data)
        return likecomment
 
    
