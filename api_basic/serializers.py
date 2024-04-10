from rest_framework import fields, serializers
from api_basic.models import Article


class ArticleSerializers(serializers.ModelSerializer):
    class Meta :
        model = Article
        fields = ['id','Title','Author', 'Email','Date']

 
    Title = serializers.CharField(max_length=50)
    Author =serializers.CharField(max_length=50)
    Email = serializers.EmailField(max_length=50)
    # Date =  serializers.date.today() 

    def create(self, validated_data):
        return Article.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.Title = validated_data.get('Title', instance.Title)
        instance.Author = validated_data.get('Author', instance.Author)
        instance.Email = validated_data.get('Email', instance.Email)
        instance.Date = validated_data.get('Date', instance.Date)
        instance.save()
        return instance