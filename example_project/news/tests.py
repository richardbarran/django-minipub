from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .factories import ArticleFactory
from .models import Article

import datetime

"""
Welcome... here are all the tests for the minipub application.

minipub models are all abstract, and no urls.py is defined by default, so testing
is a bit tricky. So instead we test this news app which implements all the
minipub functionality.

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
        """Only live articles should be seen."""

        # By default the factory publishes articles.
        self.assertQuerySetEqual(Article.objects.live().all(),
                                 ['<Article: Some news about me>'], transform=repr)
        self.assertEqual(self.article1.status, Article.STATUS.published)
        self.assertEqual(self.article1.live(), True)

        self.article1.status = Article.STATUS.draft
        self.article1.save()
        self.assertQuerySetEqual(Article.objects.live().all(),
                                 [])
        self.assertEqual(self.article1.live(), False)

    def test_start(self):
        """Only articles with a start date in the past can be seen."""

        self.article1.start = datetime.date(2999, 1, 1)
        self.article1.save()
        self.assertQuerySetEqual(Article.objects.live().all(),
                                 [])
        self.assertEqual(self.article1.live(), False)

    def test_end(self):
        """Only articles with an end date in the future can be seen."""

        self.article1.end = datetime.date(1901, 1, 1)
        self.article1.save()
        self.assertQuerySetEqual(Article.objects.live().all(),
                                 [])
        self.assertEqual(self.article1.live(), False)

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

    def test_draft_preview(self):
        """Helper property: is article draft?"""

        self.assertEqual(self.article1.staff_preview, False)

        self.article1.status = Article.STATUS.draft
        self.article1.save()

        self.assertEqual(self.article1.staff_preview, True)


class ArticleListTest(TestCase):
    """The landing page has a list of all articles."""

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
        self.assertQuerySetEqual(response.context['article_list'],
                                 ['<Article: article 2>', '<Article: article 3>', '<Article: article 1>'],
                                 transform=repr)

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

        self.assertQuerySetEqual(response.context['article_list'],
                                 ['<Article: article 2>', '<Article: article 3>'], transform=repr)

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

        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['article_list'],
                                 ['<Article: article 2>', '<Article: article 3>', '<Article: article 1>'],
                                 transform=repr)

    def test_get_date_list(self):
        """Archive view has a list of years for which we have articles."""

        response = self.client.get('/news/')
        self.assertQuerySetEqual(response.context['date_list'],
                                 ['datetime.date(2012, 1, 1)', 'datetime.date(2011, 1, 1)'], transform=repr)

        self.article1.status = Article.STATUS.draft
        self.article1.save()

        response = self.client.get('/news/')
        self.assertQuerySetEqual(response.context['date_list'],
                                 ['datetime.date(2012, 1, 1)'], transform=repr)

    def test_get_date_list_staff(self):
        """Archive view has a list of years for which we have articles - staff will
        see all articles.

        This behaviour is a result of us overriding the get_queryset() method in the view.
        """

        self.article1.status = Article.STATUS.draft
        self.article1.save()

        user = User.objects.create_user('john.doe',
                                        'john.doe@example.com',
                                        'secret')
        user.is_staff = True
        user.save()
        self.assertTrue(self.client.login(username='john.doe', password='secret'))

        response = self.client.get('/news/')
        self.assertQuerySetEqual(response.context['date_list'],
                                 ['datetime.date(2012, 1, 1)', 'datetime.date(2011, 1, 1)'], transform=repr)


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

    def test_list_live(self):
        """Only show years for which we have live articles."""

        self.article3.status = Article.STATUS.draft
        self.article3.save()

        response = self.client.get('/news/')

        self.assertEqual(list(response.context['date_list']),
                         [datetime.date(2011, 1, 1)])

    def test_year_not_live(self):
        """Articles that are not live do not appear in the year page.
        By extension, a year with no live articles gives a 404"""

        self.article3.status = Article.STATUS.draft
        self.article3.save()

        response = self.client.get('/news/year/2012/')
        self.assertEqual(response.status_code, 404)

    def test_year_not_live_staff(self):
        """Staff members can see articles even if not published."""

        self.article3.status = Article.STATUS.draft
        self.article3.save()

        # At this point, a GET would result in a 404, same as in
        # previous test.
        user = User.objects.create_user('john.doe',
                                        'john.doe@example.com',
                                        'secret')
        user.is_staff = True
        user.save()
        self.assertTrue(self.client.login(username='john.doe', password='secret'))

        # Staff users can see this page.
        response = self.client.get('/news/year/2012/')
        self.assertEqual(response.status_code, 200)


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

    def test_live(self):
        """Articles that are not live cannot be seen."""

        self.article1.status = Article.STATUS.draft
        self.article1.save()

        response = self.client.get('/news/some-news-about-me/')
        self.assertEqual(response.status_code, 404)

    def test_live_staff(self):
        """Staff members can see articles that are not live."""

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
        self.assertContains(response, f'<lastmod>{today_as_string}</lastmod>')
