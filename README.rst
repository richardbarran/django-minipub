Django-mininews
===============

A toolkit that provides boilerplate code used in creating apps for Articles, Blogs, etc...

Why?
----
The author has written several Blog/News type applications for clients; after a 
while he noticed that:

- Most blog engines for Django are feature-rich - see Zinnia for example.
- Most of the websites built only need a subset of those features.
- For each site, the client needs differ slightly - for
  example, specifying which WYSIWYG editor to use; or adding tagging; or using
  expiry dates.
- Several of the blog/news applications on Pypi look like abandonware; probably
  because they were just too complex for their author to keep on maintaining...
- Clients are (understandably) curious about features that exist in a third-party
  app, appear in the admin interface of their website, but are not actually used
  (and the same questions get raised each time a new
  intern takes over managing the client's blog page).

The answer to the above was to create a toolkit that included a very limited
feature set, but that was *very* easy to customise. In fact, django-mininews by
default does not ship with a urls.py - the intent is that you will *never* use
it 'out of the box', but rather as a starting point for your own application.

So, what does it do?
--------------------
Basically, it provides an abstract model with:

- Publication fields: status, start date, and end date.
- SEO fields (meta + sitemap priority).
- A set of timestamps to monitor each record (timestamp created, last modified,
  last change of status).
- Erm, that's it.

The above fields are then used in plenty of boilerplate code for the admin, views,
sitemaps, and so on.

TODO:
- Atom feeds.
- The list view shows the latest articles/posts... add alongside this the ListView
  so that devs can add custom ordering (and not be forced to use 'date, descending').
- Add OpenGraph template snippet (article tags)
