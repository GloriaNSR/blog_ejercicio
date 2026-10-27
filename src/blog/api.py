from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from .models import Article


class ArticleAPISerializer(serializers.ModelSerializer):
    titulo = serializers.CharField(source='title', max_length=200)
    cuerpo = serializers.CharField(source='content')
    estado = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id', 'titulo', 'cuerpo', 'estado')
        read_only_fields = ('id', 'estado')

    def get_estado(self, article):
        return 'publicado' if article.is_published else 'borrador'

    def create(self, validated_data):
        title = validated_data['title']
        slug_base = slugify(title)[:200] or 'articulo'
        slug = slug_base
        suffix = 2
        while Article.objects.filter(slug=slug).exists():
            suffix_text = f'-{suffix}'
            slug = f'{slug_base[:200 - len(suffix_text)]}{suffix_text}'
            suffix += 1

        request = self.context['request']
        return Article.objects.create(
            title=title,
            slug=slug,
            excerpt='',
            content=validated_data['content'],
            author=request.user.get_username()[:120],
            is_published=False,
        )


class ArticleListCreateAPIView(APIView):
    authentication_classes = (TokenAuthentication,)

    def get_permissions(self):
        if self.request.method == 'POST':
            return (IsAdminUser(),)
        return (AllowAny(),)

    def get(self, request):
        articles = Article.objects.filter(is_published=True)
        serializer = ArticleAPISerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleAPISerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        article = serializer.save()
        return Response(
            ArticleAPISerializer(article).data,
            status=HTTP_201_CREATED,
        )


class ArticleDetailAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk, is_published=True)
        serializer = ArticleAPISerializer(article)
        return Response(serializer.data)
