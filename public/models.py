from django.db import models
from django import forms
from django.conf import settings

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel


from modelcluster.fields import ParentalManyToManyField, ParentalKey

from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from .blocks import (
    HomePageBlock,
    ProjectPageBlock,
    ProcessPageBlock,
    WebAppPageBlock
)

from wagtail.snippets.models import register_snippet
from account.models import User
from .image import SwiftkindImage


class HomePage(Page):
    """ Home page models
    """
    parent_page_types = ['wagtailcore.Page']
    body = StreamField(
        HomePageBlock(), verbose_name="Page body", blank=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]


class ProjectPage(Page):
    """ Project page models
    """
    project = StreamField(
        ProjectPageBlock(), verbose_name="Page projects", blank=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel('project'),
    ]


class ProcessPage(Page):
    """ Process page models
    """
    body = StreamField(
        ProcessPageBlock(), verbose_name="Page body", blank=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]


class WebAppPage(Page):
    """ Web app page
    """
    body = StreamField(
        WebAppPageBlock(), verbose_name="Page body", blank=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
