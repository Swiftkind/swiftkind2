from django.db import models
from django import forms
from django.conf import settings

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


from modelcluster.fields import ParentalManyToManyField, ParentalKey

from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    PageChooserPanel,
    InlinePanel,
)

from wagtail.snippets.models import register_snippet
from account.models import User


class HomePage(Page):
    """ Home page models
    """
    hero_title = models.CharField(max_length=525, blank=True, null=True)
    hero_text = models.TextField(blank=True)
    hero_cta_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Hero CTA link',
    )
    featured_section_1_title = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    feature_section_1_cover = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    featured_section_1 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Featured section 1'
    )

    featured_section_2_title = models.CharField(
        max_length=256, 
        blank=True,
        null=True
    )
    feature_section_2_cover = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    featured_section_2 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Featured section 2'
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_text'),
            PageChooserPanel('hero_cta_link'),
        ]),
        MultiFieldPanel([
            MultiFieldPanel([
                FieldPanel('featured_section_1_title'),
                ImageChooserPanel('feature_section_1_cover'),
                PageChooserPanel('featured_section_1'),
                ]),
            MultiFieldPanel([
                FieldPanel('featured_section_2_title'),
                ImageChooserPanel('feature_section_2_cover'),
                PageChooserPanel('featured_section_2'),
                ])
        ], heading="Featured homepage sections", classname="collapsible")
    ]


class TeamMembersPage(Page):
    members = ParentalManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True)
    description = models.TextField(blank=True, null=True)
    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('members', widget=forms.CheckboxSelectMultiple)
    ]
