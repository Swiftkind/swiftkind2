from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render


from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.search import index
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from taggit.models import Tag, TaggedItemBase

class BlogPage(Page):
    """ Blog page models
    """

    author = models.ForeignKey(User, related_name='blogs', on_delete='CASCADE')
    body = RichTextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('body')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('author')
    ]


class BlogIndexPage(RoutablePageMixin, Page):
    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)

    @route(r'^$', name='blog')
    def index_route(self, request, *args, **kwargs):
        return super(BlogIndexPage, self).index_route(request, *args, **kwargs)

    @route('^tags/$', name='tag_archive')
    @route('^tags/([\w-]+)/$', name='tag_archive')
    def tag_archive(self, request, tag=None):

        try:
            tag = Tag.objects.get(slug=tag)
        except Tag.DoesNotExist:
            if tag:
                msg = 'There are no blog posts tagged with "{}"'.format(tag)
                messages.add_message(request, messages.INFO, msg)
            return redirect(self.url)

        posts = self.get_posts(tag=tag)
        context = {
            'tag': tag,
            'posts': posts
        }
        return render(request, 'blog/blog_index_page.html', context)

    def serve_preview(self, request, mode_name):
        # Needed for previews to work
        return self.serve(request)

    # Returns the child BlogPage objects for this BlogPageIndex.
    # If a tag is used then it will filter the posts by tag.
    def get_posts(self, tag=None):
        posts = BlogPage.objects.live().descendant_of(self)
        if tag:
            posts = posts.filter(tags=tag)
        return posts

    # Returns the list of Tags for all child posts of this BlogPage.
    def get_child_tags(self):
        tags = []
        for post in self.get_posts():
            # Not tags.append() because we don't want a list of lists
            tags += post.get_tags
        tags = sorted(set(tags))
        return tags
