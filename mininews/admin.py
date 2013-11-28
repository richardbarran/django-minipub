from django.contrib import admin

from .models import Article

class ArticleAdmin(admin.ModelAdmin):
	list_display = ('title', 'viewable', 'status', 'start')
	prepopulated_fields = {"slug": ("title",)}
	readonly_fields = ('created', 'modified', 'status_changed')

	TIMESTAMP_FIELDSET = ('Timestamps', {
			'description': 'When this record was created, last modified, and when '
				'the status was last changed.',
			'classes': ('collapse',),
			'fields': (('created', 'modified', 'status_changed'),)
		})

	fieldsets = (
		(None, {
			'fields': ('title', 'slug',)
		}),
		('Publication', {
			'description': "You can control here if an article is 'viewable' in the website. "
					"<br>An article is only 'viewable' if both its status is 'published', and"
					" - if the start and end dates are entered - if today's date is "
					"between the two."
					"<br>Note: when you are logged in to the 'admin', you can see "
					"this article, even if it's not published.",
			'fields': ('status', 'start', 'end')
		}),
		(None, {
			'fields': ('body',)
		}),
		('SEO', {
			'description': "Meta elements provide information about the web page, "
			"which can be used by search engines to help categorize the page correctly.",
			'classes': ('collapse',),
			'fields': ('meta_description', 'meta_keywords', 'sitemap_priority')
		}),
		TIMESTAMP_FIELDSET
	)

admin.site.register(Article, ArticleAdmin)
