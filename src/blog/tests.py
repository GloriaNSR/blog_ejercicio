from datetime import timedelta
from io import BytesIO
from tempfile import TemporaryDirectory

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import AboutPage, Article


class ArticlePagesTests(TestCase):
    def setUp(self):
        AboutPage.objects.get_or_create(
            pk=1,
            defaults={'content': 'Presentación de ejemplo.'},
        )
        self.newest = Article.objects.create(
            title='Robots exploradores',
            slug='robots-exploradores',
            excerpt='Un resumen del artículo.',
            content='## Exploración\n\nLos robots pueden explorar.',
            author='Ada',
            published_at=timezone.now(),
            is_published=True,
        )
        self.oldest = Article.objects.create(
            title='Sensores básicos',
            slug='sensores-basicos',
            content='Contenido del artículo.',
            author='Ada',
            published_at=timezone.now() - timedelta(days=2),
            is_published=True,
        )
        self.draft = Article.objects.create(
            title='Borrador secreto',
            slug='borrador-secreto',
            content='Todavía no publicado.',
            author='Ada',
            is_published=False,
        )

    def test_home_shows_only_published_articles_newest_first(self):
        response = self.client.get(reverse('blog:home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.newest.title)
        self.assertContains(response, self.oldest.title)
        self.assertNotContains(response, self.draft.title)
        self.assertContains(response, 'Contenido del artículo.')
        self.assertLess(
            response.content.index(self.newest.title.encode()),
            response.content.index(self.oldest.title.encode()),
        )

    def test_home_explains_when_there_are_no_published_articles(self):
        Article.objects.filter(is_published=True).update(is_published=False)

        response = self.client.get(reverse('blog:home'))

        self.assertContains(response, 'Todavía no hay artículos publicados')

    def test_published_article_shows_metadata_and_formatted_content(self):
        response = self.client.get(
            reverse('blog:article_detail', args=[self.newest.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.newest.title)
        self.assertContains(response, self.newest.author)
        self.assertContains(response, '<h2>Exploración</h2>', html=True)
        self.assertContains(response, '<p>Los robots pueden explorar.</p>', html=True)

    def test_associated_image_is_shown_on_home_and_article_page(self):
        with TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root):
            image_bytes = BytesIO()
            Image.new('RGB', (1, 1)).save(image_bytes, format='PNG')
            self.newest.image.save(
                'robot.png',
                SimpleUploadedFile('robot.png', image_bytes.getvalue(), content_type='image/png'),
                save=True,
            )

            home_response = self.client.get(reverse('blog:home'))
            detail_response = self.client.get(
                reverse('blog:article_detail', args=[self.newest.slug])
            )

        self.assertContains(home_response, '<img', html=False)
        self.assertContains(detail_response, '<img', html=False)
        self.assertContains(home_response, '/media/articles/robot.png')
        self.assertContains(detail_response, '/media/articles/robot.png')

    def test_draft_is_not_accessible_by_its_known_slug(self):
        response = self.client.get(
            reverse('blog:article_detail', args=[self.draft.slug])
        )

        self.assertEqual(response.status_code, 404)

    def test_unknown_article_uses_site_404_page(self):
        with self.settings(DEBUG=False):
            response = self.client.get(
                reverse('blog:article_detail', args=['no-existe'])
            )

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, 'Señal perdida', status_code=404)

    def test_about_page_shows_editable_content_and_primary_navigation(self):
        AboutPage.objects.filter(pk=1).update(
            content='## Mi presentación\n\nTexto actualizado desde el panel.'
        )

        response = self.client.get(reverse('blog:about'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h1>Sobre mí</h1>', html=True)
        self.assertContains(response, '<h2>Mi presentación</h2>', html=True)
        self.assertContains(response, 'Texto actualizado desde el panel.')
        self.assertContains(response, 'href="/">Portada</a>', html=False)
        self.assertContains(response, 'href="/sobre-mi/">Sobre mí</a>', html=False)
        self.assertNotContains(response, '<script')


class EditorialAccessTests(TestCase):
    def setUp(self):
        AboutPage.objects.get_or_create(
            pk=1,
            defaults={'content': 'Presentación editable.'},
        )

    def test_anonymous_visitor_is_redirected_from_admin(self):
        response = self.client.get('/admin/')

        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)

    def test_authorized_editor_can_update_about_page_from_admin(self):
        editor = get_user_model().objects.create_superuser(
            username='editor',
            email='editor@example.com',
            password='test-password',
        )
        self.client.force_login(editor)

        response = self.client.post(
            reverse('admin:blog_aboutpage_change', args=[1]),
            {
                'content': 'Presentación actualizada desde Django Admin.',
                '_save': 'Guardar',
            },
        )

        self.assertEqual(response.status_code, 302)
        page_response = self.client.get(reverse('blog:about'))
        self.assertContains(page_response, 'Presentación actualizada desde Django Admin.')


class ArticleAPITests(TestCase):
    def setUp(self):
        self.published = Article.objects.create(
            title='Artículo publicado',
            slug='articulo-publicado',
            content='Contenido público.',
            author='Ada',
            is_published=True,
        )
        self.draft = Article.objects.create(
            title='Artículo borrador',
            slug='articulo-borrador',
            content='Contenido privado.',
            author='Ada',
            is_published=False,
        )
        self.admin = get_user_model().objects.create_user(
            username='api-editor',
            password='test-password',
            is_staff=True,
        )
        self.admin_token = Token.objects.create(user=self.admin)
        self.client = APIClient()

    def test_list_is_public_and_contains_only_published_articles(self):
        response = self.client.get(reverse('blog:api_articles'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'id': self.published.pk,
                    'titulo': self.published.title,
                    'cuerpo': self.published.content,
                    'estado': 'publicado',
                }
            ],
        )

    def test_published_detail_is_public_and_draft_detail_is_hidden(self):
        published_response = self.client.get(
            reverse('blog:api_article_detail', args=[self.published.pk])
        )
        draft_response = self.client.get(
            reverse('blog:api_article_detail', args=[self.draft.pk])
        )
        missing_response = self.client.get(
            reverse('blog:api_article_detail', args=[99999])
        )

        self.assertEqual(published_response.status_code, 200)
        self.assertEqual(published_response.json()['estado'], 'publicado')
        self.assertEqual(draft_response.status_code, 404)
        self.assertEqual(missing_response.status_code, 404)

    def test_post_requires_an_admin_token(self):
        response = self.client.post(
            reverse('blog:api_articles'),
            {'titulo': 'Nuevo borrador', 'cuerpo': 'Contenido.'},
            format='json',
        )

        self.assertIn(response.status_code, (401, 403))
        self.assertFalse(Article.objects.filter(title='Nuevo borrador').exists())

    def test_non_staff_token_cannot_create_article(self):
        reader = get_user_model().objects.create_user(
            username='reader',
            password='test-password',
        )
        token = Token.objects.create(user=reader)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = self.client.post(
            reverse('blog:api_articles'),
            {'titulo': 'No autorizado', 'cuerpo': 'Contenido.'},
            format='json',
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Article.objects.filter(title='No autorizado').exists())

    def test_admin_token_creates_unpublished_article_with_contract_fields(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.admin_token.key}'
        )

        response = self.client.post(
            reverse('blog:api_articles'),
            {'titulo': 'Nuevo artículo API', 'cuerpo': 'Texto del borrador.'},
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            set(response.json()),
            {'id', 'titulo', 'cuerpo', 'estado'},
        )
        self.assertEqual(response.json()['estado'], 'borrador')
        article = Article.objects.get(pk=response.json()['id'])
        self.assertFalse(article.is_published)
        self.assertEqual(article.author, self.admin.get_username())
        self.assertEqual(article.slug, 'nuevo-articulo-api')
        self.assertEqual(article.excerpt, '')

    def test_duplicate_titles_get_unique_slugs(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.admin_token.key}'
        )

        first = self.client.post(
            reverse('blog:api_articles'),
            {'titulo': 'Título repetido', 'cuerpo': 'Uno.'},
            format='json',
        )
        second = self.client.post(
            reverse('blog:api_articles'),
            {'titulo': 'Título repetido', 'cuerpo': 'Dos.'},
            format='json',
        )

        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 201)
        self.assertEqual(
            set(Article.objects.filter(title='Título repetido').values_list(
                'slug', flat=True
            )),
            {'titulo-repetido', 'titulo-repetido-2'},
        )

    def test_invalid_payloads_do_not_create_articles(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.admin_token.key}'
        )
        invalid_payloads = (
            {'cuerpo': 'Sin título.'},
            {'titulo': 'Sin cuerpo.'},
            {'titulo': '   ', 'cuerpo': 'Cuerpo.'},
            {'titulo': 'Título vacío', 'cuerpo': '   '},
            {'titulo': 'x' * 201, 'cuerpo': 'Cuerpo.'},
        )
        original_count = Article.objects.count()

        for payload in invalid_payloads:
            with self.subTest(payload=payload):
                response = self.client.post(
                    reverse('blog:api_articles'),
                    payload,
                    format='json',
                )
                self.assertEqual(response.status_code, 400)

        self.assertEqual(Article.objects.count(), original_count)
