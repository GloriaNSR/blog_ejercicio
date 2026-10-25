from datetime import timedelta
from io import BytesIO
from tempfile import TemporaryDirectory

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

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
