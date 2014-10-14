import datetime

from django.test import TestCase
from django.contrib.auth.models import User

from .factories import ArticleFactory
from .models import Article


"""
Tests for the `mininews_live` attribute.

Note that we do not run test for the List views - the get_queryset() method is the same as for 
the ArticleDetail view, so we just test that.

"""

class ArticleModelTest(TestCase):

    """Various tests on the Article model."""

    def test_default_start(self):
        """Set a default value for the start date."""

        # Should set a date when status goes to published.
        article1 = ArticleFactory(start=None, status=Article.STATUS.draft)
        article1.save()

        self.assertEqual(article1.start, None)

        article1.status = Article.STATUS.published
        article1.save()

        self.assertNotEqual(article1.start, None)

        # Should also set a date when status goes to archived.
        article2 = ArticleFactory(start=None, status=Article.STATUS.draft)
        article2.save()

        self.assertEqual(article2.start, None)

        article2.status = Article.STATUS.archived
        article2.save()

        self.assertNotEqual(article2.start, None)

class ArticleDetailTest(TestCase):

    def setUp(self):

        self.article1 = ArticleFactory(title='Some news about me')

    def test_published_status(self):
        """Get an article detail page - article is published."""
        self.article1.status = 'published'
        self.article1.save()

        response = self.client.get('/news_with_archive/news/some-news-about-me/')
        self.assertEqual(response.status_code, 200)


    def test_published_other_status(self):
        """Articles that are not 'live' cannot be seen."""

        for status in ('draft', 'archived'):
            self.article1.status = status
            self.article1.save()

            response = self.client.get('/news_with_archive/news/some-news-about-me/')
            self.assertEqual(response.status_code, 404)

    def test_archived_status(self):
        """Get an article detail page - article is archived."""
        self.article1.status = 'archived'
        self.article1.save()

        response = self.client.get('/news_with_archive/archived/some-news-about-me/')
        self.assertEqual(response.status_code, 200)


    def test_archived_other_status(self):
        """Articles that are not 'live' cannot be seen."""

        for status in ('draft', 'published'):
            self.article1.status = status
            self.article1.save()

            response = self.client.get('/news_with_archive/archived/some-news-about-me/')
            self.assertEqual(response.status_code, 404)

    def test_draft_staff(self):
        """Staff members can see articles that are draft."""

        user = User.objects.create_user('john.doe',
                                        'john.doe@example.com',
                                        'secret')
        user.is_staff = True
        user.save()
        self.assertTrue(self.client.login(username='john.doe', password='secret'))

        self.article1.status = Article.STATUS.draft
        self.article1.save()

        response = self.client.get('/news_with_archive/news/some-news-about-me/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/news_with_archive/archived/some-news-about-me/')
        self.assertEqual(response.status_code, 200)

    def test_bad_status_staff(self):
        """Staff members can only see articles that are either in the 'correct' status
        for that page, or draft.
        E.g. they cannot see 'published' articles on a 'archives' pages."""

        user = User.objects.create_user('john.doe',
                                        'john.doe@example.com',
                                        'secret')
        user.is_staff = True
        user.save()
        self.assertTrue(self.client.login(username='john.doe', password='secret'))

        response = self.client.get('/news_with_archive/news/some-news-about-me/')
        self.assertEqual(response.status_code, 404)

        self.article1.status = Article.STATUS.published
        self.article1.save()

        response = self.client.get('/news_with_archive/archived/some-news-about-me/')
        self.assertEqual(response.status_code, 404)

class ArticleListTest(TestCase):

    """The landing page has a list of all articles."""

    def setUp(self):

        self.article1 = ArticleFactory(title='article 1',
                                       start=datetime.date(day=23, month=12, year=2011))
        self.article2 = ArticleFactory(title='article 2',
                                       start=datetime.date(day=25, month=12, year=2012),
                                       status='published')
        self.article3 = ArticleFactory(title='article 3',
                                       start=datetime.date(day=24, month=12, year=2012))

    def test_get(self):
        """The list pages should only show articles of the correct status."""

        # Show 'published' articles.
        response = self.client.get('/news_with_archive/news/')
        self.assertEqual(response.status_code, 200)

        # Note that results are ordered by date.
        self.assertQuerysetEqual(response.context['article_list'],
                                 ['<Article: article 2>'])

        # Show 'archived' articles.
        response = self.client.get('/news_with_archive/archived/')
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(response.context['article_list'],
                                 ['<Article: article 3>', '<Article: article 1>'])


    def test_urls(self):
        """Check the urls to the detail pages."""

        # Show 'published' articles.
        response = self.client.get('/news_with_archive/news/')

        self.assertEqual(response.context['article_list'][0].get_absolute_url(),
            '/news_with_archive/news/article-2/')

        # Show 'archived' articles.
        response = self.client.get('/news_with_archive/archived/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['article_list'][0].get_absolute_url(),
            '/news_with_archive/archived/article-3/')
        self.assertEqual(response.context['article_list'][1].get_absolute_url(),
            '/news_with_archive/archived/article-1/')

class SitemapTest(TestCase):

    def setUp(self):

        self.article1 = ArticleFactory(title='Test article')

    def test_published_articles(self):
        """Articles in the main section of the site."""
        self.article1.status = Article.STATUS.published
        self.article1.save()
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)

        # Is published, not archived.
        self.assertContains(response, '<loc>http://example.com/news_with_archive/news/test-article/</loc>')
        self.assertNotContains(response, '<loc>http://example.com/news_with_archive/archived/test-article/</loc>')

    def test_archived_articles(self):
        """Articles in the archived section of the site."""
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)

        # Is published, not archived.
        self.assertNotContains(response, '<loc>http://example.com/news_with_archive/news/test-article/</loc>')
        self.assertContains(response, '<loc>http://example.com/news_with_archive/archived/test-article/</loc>')

    def test_draft_articles(self):
        """Draft articles appear nowhere."""
        self.article1.status = Article.STATUS.draft
        self.article1.save()

        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)

        # Is published, not archived.
        self.assertNotContains(response, '<loc>http://example.com/news_with_archive/news/test-article/</loc>')
        self.assertNotContains(response, '<loc>http://example.com/news_with_archive/archived/test-article/</loc>')
