.. _extra_statuses-label:

Refining the concept of a 'Live' object
---------------------------------------

Let's imagine that your articles can be ``published``, but that at some point in time you will want
to manually move them to an 'archived' section in the website.

Models
~~~~~~
First, you will define in your model the complete list of statuses available:

.. code-block:: python

    class MyCustomModel(MininewsModel):

        STATUS = Choices('draft', 'published', 'archived')

And you'll also tweak your ``get_absolute_url()`` to handle the new options:

.. code-block:: python

    def get_absolute_url(self):
        if self.status == self.STATUS.archived:
            return reverse('the_url_for_the_archived_page', kwargs={'slug': self.slug})
        else:
            return reverse('the_url_for_the_published_page', kwargs={'slug': self.slug})

Views
~~~~~
Secondly, in your ``views.py`` you will have 2 sets of views:

- the views for the main pages.
- the views for the archived pages.

And the urls would look something like::

    /news/
    /news/<article slug>/
    /archives/
    /archives/<article slug>/

In the views, you will split out the articles to be displayed in the main section:

.. code-block:: python

    class ArticleDetailView(MininewsDetailView):
        model = Article
        context_object_name = 'article'
        mininews_live = ('published',)

And then the articles to show in the archives section:

.. code-block:: python

    class ArticleArchivesDetailView(MininewsDetailView):
        model = Article
        context_object_name = 'article'
        mininews_live = ('archived',)

We have added a new attribute - ``mininews_live``. This will override the ``STATUS`` defined
on the model.
