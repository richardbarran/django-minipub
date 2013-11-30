from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.test.utils import override_settings

from .factories import ArticleFactory
from .models import Article

import datetime
import decimal

"""
Welcome... here are all the tests for the mininews application.

mininews models are all abstract, and no urls.py is defined by default, so testing
is a bit tricky. So instead we test this news app which implements all the 
mininews functionality.

Use of factory-boy
------------------

The unit tests use factory-boy extensively to generate test data. One reason for using
it is that because the models will often be extended, we have no
way of knowing exactly what required fields might exist on the model - and our
tests would fail. Factory-boy will automatically fill in some dummy values - and can
be inherited easily if you're writing an app that extends this one.

"""


class ArticleModelTest(TestCase):
    """Various tests on the Article model."""

    def setUp(self):

        self.article1 = ArticleFactory(title='Some news about me')

    def test_status(self):
        """Only published articles should be seen."""

        # By default the factory publishes articles.
        self.assertQuerysetEqual(Article.objects.viewable().all(),
                                 ['<Article: Some news about me>'])

        self.article1.status = Article.STATUS.draft
        self.article1.save()
        self.assertQuerysetEqual(Article.objects.viewable().all(),
                                 [])
        self.assertEqual(self.article1.viewable(), False)

    def test_start(self):
        """Only articles with a start date in the past can be seen."""

        self.article1.start = datetime.date(2999, 1, 1)
        self.article1.save()
        self.assertQuerysetEqual(Article.objects.viewable().all(),
                                 [])
        self.assertEqual(self.article1.viewable(), False)

    def test_end(self):
        """Only articles with an end date in the future can be seen."""

        self.article1.end = datetime.date(1901, 1, 1)
        self.article1.save()
        self.assertQuerysetEqual(Article.objects.viewable().all(),
                                 [])
        self.assertEqual(self.article1.viewable(), False)

    def test_dates(self):
        """Start date has to be before the end date."""
        self.article1.start = datetime.date(2010, 1, 2)
        self.article1.end = datetime.date(2010, 1, 2)
        self.article1.clean()

        self.article1.end = datetime.date(2010, 1, 1)
        with self.assertRaisesMessage(ValidationError, 'The end date cannot be before the start date.'):
            self.article1.clean()

    def test_default_start(self):
        """Set a default value for the start date."""

        article = ArticleFactory(start=None, status=Article.STATUS.draft)
        article.save()

        self.assertEqual(article.start, None)

        article.status = Article.STATUS.published
        article.save()

        self.assertNotEqual(article.start, None)

class ArticleListTest(TestCase):
    """The landing page has a (paginated) list of all articles."""

    def setUp(self):

        self.article1 = ArticleFactory(title='article 1',
                                       start=datetime.date(day=23, month=12, year=2011))
        self.article2 = ArticleFactory(title='article 2',
                                       start=datetime.date(day=25, month=12, year=2012))
        self.article3 = ArticleFactory(title='article 3',
                                       start=datetime.date(day=24, month=12, year=2012))

    def test_get(self):
        """Get main page of the app - should contain a list of the latest articles."""

        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/article_archive.html')

        # Note that results are ordered by date.
        self.assertQuerysetEqual(response.context['article_list'],
                                 ['<Article: article 2>', '<Article: article 3>', '<Article: article 1>'])

        self.assertContains(response, 'article 1')
        self.assertContains(response, 'article 2')
        # etc...

        # And we have the urls to the detail page.
        self.assertContains(response, '/news/')

    def test_not_published(self):
        """Articles that are not published are not shown."""

        self.article1.status = Article.STATUS.draft
        self.article1.save()

        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(response.context['article_list'],
                                 ['<Article: article 2>', '<Article: article 3>'])

    def test_nothing(self):
        """Still show the page even if no articles are available."""

        self.article1.status = Article.STATUS.draft
        self.article1.save()
        self.article2.status = Article.STATUS.draft
        self.article2.save()
        self.article3.status = Article.STATUS.draft
        self.article3.save()

        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(response.context['article_list'], [])

    def test_pagination(self):
        Article.objects.all().delete()
        for i in range(1, 23):
            ArticleFactory(title='article{0:0>3}'.format(i),
                           start=datetime.date(day=i, month=12, year=2011))

        response = self.client.get('/news/')

        self.assertEqual(len(response.context['article_list']),
                         20)
        # Check first and last items.
        self.assertEqual(response.context['article_list'][0].title,
                                 'article022')
        self.assertEqual(response.context['article_list'][19].title,
                                 'article003')

        # Now get the second page of results.
        response = self.client.get('/news/', {'page': 2})

        self.assertEqual(len(response.context['article_list']),
                         2)
        # Check first and last items.
        self.assertEqual(response.context['article_list'][0].title,
                                 'article002')
        self.assertEqual(response.context['article_list'][1].title,
                                 'article001')

class ArticleListYearTest(TestCase):
    """The landing page lists all the years for which we have articles.
    Then we can filter down the show just the articles for a given year."""

    def setUp(self):

        self.article1 = ArticleFactory(title='article 1',
                                       start=datetime.date(day=23, month=12, year=2011))
        self.article2 = ArticleFactory(title='article 2',
                                       start=datetime.date(day=24, month=12, year=2011))
        self.article3 = ArticleFactory(title='article 3',
                                       start=datetime.date(day=24, month=12, year=2012))

    def test_get(self):
        """Check that we have the years."""

        response = self.client.get('/news/')

        self.assertEqual(list(response.context['date_list']),
                          [datetime.date(2012, 1, 1),
                           datetime.date(2011, 1, 1)])

        # The years are listed in the template.
        self.assertContains(response, '2012</a>')
        self.assertContains(response, '2011</a>')

    def test_list_viewable(self):
        """Only show years for which we have viewable articles."""

        self.article3.status = Article.STATUS.draft
        self.article3.save()

        response = self.client.get('/news/')

        self.assertEqual(list(response.context['date_list']),
                          [datetime.date(2011, 1, 1)])


    def test_get_year_page(self):
        """We can request the articles for a given year."""

        response = self.client.get('/news/year/2012/')

        # Only that year's articles are available.
        self.assertQuerysetEqual(response.context['article_list'],
                                 ['<Article: article 3>'])

    def test_year_not_viewable(self):
        """Articles that are not viewable do not appear in the year page.
        By extension, a year with no viewable articles gives a 404"""

        self.article3.status = Article.STATUS.draft
        self.article3.save()

        response = self.client.get('/news/year/2012/')
        self.assertEqual(response.status_code, 404)

class ArticleDetailTest(TestCase):

    def setUp(self):

        self.article1 = ArticleFactory(title='Some news about me')

    def test_get(self):
        """Get an article detail page."""
        response = self.client.get('/news/some-news-about-me/')
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'news/article_detail.html')

        # Check that various fields of the article are there.
        self.assertEqual(response.context['article'], self.article1)
        self.assertContains(response, self.article1.title)

    def test_published(self):
        """Articles that are not published cannot be seen."""

        self.article1.status = Article.STATUS.draft
        self.article1.save()

        response = self.client.get('/news/some-news-about-me/')
        self.assertEqual(response.status_code, 404)

    def test_published_staff(self):
        """Staff members can see articles that are not published."""

        self.article1.status = Article.STATUS.draft
        self.article1.save()

        user = User.objects.create_user('john.doe',
                                        'john.doe@example.com',
                                        'secret')
        user.is_staff = True
        user.save()
        self.assertTrue(self.client.login(username='john.doe', password='secret'))

        response = self.client.get('/news/some-news-about-me/')
        self.assertEqual(response.status_code, 200)

class SitemapTest(TestCase):

    def setUp(self):

        self.article1 = ArticleFactory(title='Test article')

    def test_get(self):
        """Get the sitemap, there's just one entry in it."""
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)

        # Has the url.
        self.assertContains(response, '<loc>http://example.com/news/test-article/</loc>')

        # Has the modified date - which will always be today.
        today_as_string = datetime.date.today().today().strftime('%Y-%m-%d')
        self.assertContains(response, '<lastmod>{0}</lastmod>'.format(today_as_string))

    def test_priority(self):
        """Get the sitemap, set the priority level of an article."""

        self.article1.sitemap_priority = decimal.Decimal('0.2')
        self.article1.save()

        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '<priority>0.2</priority>')

    def test_priority_field(self):
        """Validation for the sitemap_priority field."""

        # Values between 0 and 1 are fine.
        self.article1.sitemap_priority = decimal.Decimal('0.2')
        self.article1.save()

        # Outside that range is ungood.
        self.article1.sitemap_priority = decimal.Decimal('-1.0')
        with self.assertRaisesMessage(ValidationError, 'Please enter a number between 0 and 1'):
            self.article1.full_clean()

        self.article1.sitemap_priority = decimal.Decimal('1.2')
        with self.assertRaisesMessage(ValidationError, 'Please enter a number between 0 and 1'):
            self.article1.full_clean()
