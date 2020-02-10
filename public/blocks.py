import os

from django import forms
from django.conf import settings
from django.forms.utils import ErrorList
from django.core.exceptions import ValidationError

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.core.blocks import (
    CharBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    TextBlock,
    PageChooserBlock,
    URLBlock,
    RawHTMLBlock,
    ChooserBlock,
    EmailBlock
)
from account.models import User


# Home Page
class HeroBlock(StructBlock):
    hero_title = RawHTMLBlock(required=False, help_text="Raw HTML format")
    hero_body = TextBlock(required=False)
    button_label = CharBlock(required=False)
    button_link = StreamBlock([
        ('page', PageChooserBlock(label="Page", required=False, help_text="Choose only one link", icon='doc-full')),
        ('external_url', URLBlock(label="External URL", required=False, help_text="Choose only one link")),
    ], required=False, max_num=1)

    class Meta:
        icon = "title"
        template = "public/blocks/homepage_block/homepage_hero.html"
        

class DevelopmentContentBlock(StructBlock):
    content_title = CharBlock(required=False)
    content_services_title = RichTextBlock(required=False)
    content_body = TextBlock(required=False)
    button_label = CharBlock(required=False)
    button_link = StreamBlock([
        ('page', PageChooserBlock(label="page", required=False, help_text="Choose only one link", icon="doc-full")),
        ('external_url', URLBlock(label="external URL", required=False, help_text="Choose only one link", icon="site")),
    ], required=False, max_num=1)
    image = StreamBlock([
        ('svg_image', DocumentChooserBlock(label="SVG Image", required=False, help_text="SVG format only", icon="image")),
        ('other_image', ImageChooserBlock(label="Other Image", required=False, help_text="JPEG/PNG format", icon="image")),
    ], required=False, max_num=1)

    class Meta:
        icon = "form"


class DevelopmentItemsBlock(StructBlock):
    item_title = CharBlock(required=False)
    item_body = TextBlock(required=False)

    class Meta:
        icon = "list-ul"


class DevelopmentBlock(StreamBlock):
    content = DevelopmentContentBlock()
    items = DevelopmentItemsBlock()

    class Meta:
        icon = "form"
        template = "public/blocks/homepage_block/homepage_development.html"


class DesignBlock(StructBlock):
    design_title = CharBlock(required=False)
    design_service_title = RichTextBlock(required=False)
    design_body = TextBlock(required=False)
    image = StreamBlock([
        ('svg_image', DocumentChooserBlock(label="SVG Image", required=False, help_text="SVG format only", icon="image")),
        ('other_image', ImageChooserBlock(label="Other Image", required=False, help_text="JPEG/PNG format", icon="image")),
    ], required=False)
    design_footer = TextBlock(required=False)

    class Meta:
        icon = "form"
        template = "public/blocks/homepage_block/homepage_design.html"


class TeamContentBlock(StructBlock):
    team_title = CharBlock(required=False)
    team_body = TextBlock(required=False)

    class Meta:
        icon = "form"


class TeamChooserBlock(ChooserBlock):
    target_model = User
    widget = forms.Select

    class Meta:
        icon = "icon"

    # Return the key value for the select field
    def value_for_form(self, value):
        if isinstance(value, self.target_model):
            return value.pk
        else:
            return value


class TeamMembersBlock(StructBlock):
    members = TeamChooserBlock()
    avatar = StreamBlock([
        ('svg_image', DocumentChooserBlock(label="SVG Image", required=False, help_text="SVG format only", icon="image")),
        ('other_image', ImageChooserBlock(label="Other Image", required=False, help_text="JPEG/PNG format", icon="image")),
    ], required=False, max_num=1)
    position = CharBlock(required=False,)

    class Meta:
        icon = "user"


class TeamBlock(StreamBlock):
    content = TeamContentBlock()
    members = TeamMembersBlock()

    class Meta:
        icon = "group"
        template = "public/blocks/homepage_block/homepage_team.html"


class ClientBlock(StructBlock):
    client_body = TextBlock(required=False)

    class Meta:
        icon = "form"
        template = "public/blocks/homepage_block/homepage_client.html"


class HiringBlock(StructBlock):
    hiring_title = CharBlock(required=False)
    hiring_body = TextBlock(required=False)
    button_label = CharBlock(required=False)
    button_link = StreamBlock([
        ('page', PageChooserBlock(label="page", required=False, help_text="Choose only one link", icon="doc-full")),
        ('external_url', URLBlock(label="external URL", required=False, help_text="Choose only one link", icon="site")),
    ], required=False, max_num=1)

    class Meta:
        icon = "doc-full"
        template = "public/blocks/homepage_block/homepage_hiring.html"


class TestimonyMembersBlock(StructBlock):
    testimony = TextBlock(required=False)
    member = CharBlock(required=False)
    position = CharBlock(required=False)
    company_label = CharBlock(required=False)
    company_link = StreamBlock([
        ('page', PageChooserBlock(label="page", required=False, help_text="Choose only one link", icon="doc-full")),
        ('external_url', URLBlock(label="external URL", required=False, help_text="Choose only one link", icon="site")),
    ], required=False, max_num=1)
    
    class Meta:
        icon = "user"

    
class TestimonyTitleBlock(StructBlock):
    title = CharBlock(required=False)

    class Meta:
        icon = "title"


class TestimonyBlock(StreamBlock):
    testimony_title = TestimonyTitleBlock()
    members = TestimonyMembersBlock()

    class Meta:
        icon = "group"
        template = "public/blocks/homepage_block/homepage_testimony.html"


class ContactBlock(StructBlock):
    iframe_link = StreamBlock([
        ('page', PageChooserBlock(label="page", required=False, help_text="Choose only one link", icon="doc-full")),
        ('external_url', URLBlock(label="external URL", required=False, help_text="Choose only one link", icon="site")),
    ], required=False, max_num=1)
    contact_title = CharBlock(required=False)
    contact_body = TextBlock(required=False)
    email = EmailBlock(required=False)

    class Meta:
        icon = "form"
        template = "public/blocks/homepage_block/homepage_contact.html"


class HomePageBlock(StreamBlock):
    hero_block = HeroBlock()
    development_block = DevelopmentBlock()
    design_block = DesignBlock()
    team_block = TeamBlock()
    client_block = ClientBlock()
    hiring_block = HiringBlock()
    testimony_block = TestimonyBlock()
    contact_block = ContactBlock()


# Project Page
class ProjectBlock(StructBlock):
    image = StreamBlock([
        ('svg_image', DocumentChooserBlock(label="SVG Image", required=False, help_text="SVG format only", icon="image")),
        ('other_image', ImageChooserBlock(label="Other Image", required=False, help_text="JPEG/PNG format", icon="image")),
    ], required=False, max_num=1)
    image_link = StreamBlock([
        ('page', PageChooserBlock(label="page", required=False, help_text="Choose only one link", icon="doc-full")),
        ('external_url', URLBlock(label="external URL", required=False, help_text="Choose only one link", icon="site")),
    ], required=False, max_num=1)
    project_title = CharBlock(required=False)
    project_content_1 = TextBlock(required=False)
    project_content_2 = TextBlock(required=False)

    class Meta:
        icon = "doc-full"


class ProjectPageBlock(StreamBlock):
    project = ProjectBlock()


# Process Page
class ProcessHeroBlock(StructBlock):
    process_title_1 = CharBlock(required=False)
    process_content_1 = TextBlock(required=False)
    process_title_2 = CharBlock(required=False)
    process_content_2 = TextBlock(required=False)
    image = StreamBlock([
        ('svg_image', DocumentChooserBlock(label="SVG Image", required=False, help_text="SVG format only", icon="image")),
        ('other_image', ImageChooserBlock(label="Other Image", required=False, help_text="JPEG/PNG format", icon="image")),
    ], required=False, max_num=1)
    
    class Meta:
        icon = "title"
        template = "public/blocks/process_block/process_hero.html"


class StageBlock(StreamBlock):
    stage = RawHTMLBlock(required=False)
    image = StreamBlock([
        ('svg_image', DocumentChooserBlock(label="SVG Image", required=False, help_text="SVG format only", icon="image")),
        ('other_image', ImageChooserBlock(label="Other Image", required=False, help_text="JPEG/PNG format", icon="image")),
    ], required=False, max_num=1, icon="image")

    class Meta:
        icon = "list-ul"
        template = "public/blocks/process_block/process_stage.html"


class StandpointBlock(StructBlock):
    title = CharBlock(required=False)
    statement = TextBlock(required=False)
    member = CharBlock(required=False)
    position = CharBlock(required=False)

    class Meta:
        icon = "user"
        template = "public/blocks/process_block/process_standpoint.html"


class LogoTitleBlock(StructBlock):
    title = CharBlock(required=False)

    class Meta:
        icon= "title"


class LogoDetailsBlock(StructBlock):
    details_title = CharBlock(required=False)
    details_content = TextBlock(required=False)
    image = StreamBlock([
        ('svg_image', DocumentChooserBlock(label="SVG Image", required=False, help_text="SVG format only", icon="image")),
        ('other_image', ImageChooserBlock(label="Other Image", required=False, help_text="JPEG/PNG format", icon="image")),
    ], required=False, max_num=1)

    class Meta:
        icon = "form"


class LogoBlock(StreamBlock):
    title = LogoTitleBlock()
    details = LogoDetailsBlock()

    class Meta:
        icon = "list-ul"
        template = "public/blocks/process_block/process_logo.html"


class ProcessPageBlock(StreamBlock):
    hero_block = ProcessHeroBlock()
    stage_block = StageBlock()
    standpoint_block = StandpointBlock()
    logo_block = LogoBlock()


# Web App Page
# Workflow and Marketplace
class WebAppHeaderBlock(StructBlock):
    main_image = StreamBlock([
        ('svg_image', DocumentChooserBlock(label="SVG Image", required=False, help_text="SVG format only", icon="image")),
        ('other_image', ImageChooserBlock(label="Other Image", required=False, help_text="JPEG/PNG format", icon="image")),
    ], required=False, max_num=1)
    label = CharBlock(required=False)

    class Meta:
        icon = "image"
        template = "public/blocks/webapp_block/webapp_header.html"


class WebAppBriefBlock(StructBlock):
    tagline_title = CharBlock(required=False)
    tagline_content_1 = TextBlock(required=False)
    tagline_content_2 = TextBlock(required=False)
    brief_title = CharBlock(required=False)
    brief_content = TextBlock(required=False)

    class Meta:
        icon = "doc-full"
        template = "public/blocks/webapp_block/webapp_brief.html"


class WebAppImageBlock(StructBlock):
    image = StreamBlock([
        ('svg_image', DocumentChooserBlock(label="SVG Image", required=False, help_text="SVG format only", icon="image")),
        ('other_image', ImageChooserBlock(label="Other Image", required=False, help_text="JPEG/PNG format", icon="image")),
    ], required=False)

    class Meta:
        icon = "image"
        template = "public/blocks/webapp_block/webapp_image.html"


class WebAppResearchTitleBlock(StructBlock):
    phase = CharBlock(required=False)
    research_title = CharBlock(required=False)
    research_body = TextBlock(required=False)

    class Meta:
        icon = "title"


class WebAppResearchTestsBlock(StructBlock):
    research_test = CharBlock(required=False)
    research_result = CharBlock(required=False)

    class Meta:
        icon = "doc-full"


class WebAppResearchInterviewBlock(StreamBlock):
    research_title = WebAppResearchTitleBlock()
    research = WebAppResearchTestsBlock()
    questions = CharBlock(required=False, icon="help")

    class Meta:
        icon = "form"
        template = "public/blocks/webapp_block/webapp_research_interview.html"


class WebAppResearchMembersBlock(StructBlock):
    avatar = StreamBlock([
        ('svg_image', DocumentChooserBlock(label="SVG Image", required=False, help_text="SVG format only", icon="image")),
        ('other_image', ImageChooserBlock(label="Other Image", required=False, help_text="JPEG/PNG format", icon="image")),
    ], required=False, max_num=1)
    member = CharBlock(required=False)
    testimony = TextBlock(required=False)

    class Meta:
        icon = "user"


class WebAppResearchDiscussionBlock(StreamBlock):
    research_title = WebAppResearchTitleBlock()
    member = WebAppResearchMembersBlock()

    class Meta:
        icon = "group"
        template = "public/blocks/webapp_block/webapp_research_discussion.html"


class WebAppResearchFlowBlock(StreamBlock):
    research_title = WebAppResearchTitleBlock()
    image = WebAppHeaderBlock()

    class Meta:
        icon = "image"
        template = "public/blocks/webapp_block/webapp_research_flow.html"


class NextProjectBlock(StructBlock):
    title = CharBlock(required=False)
    project_name = CharBlock(required=False)
    project_link = StreamBlock([
        ('page', PageChooserBlock(label="page", required=False, help_text="Choose only one link", icon="doc-full")),
        ('external_url', URLBlock(label="external URL", required=False, help_text="Choose only one link", icon="site")),
    ], required=False, max_num=1)
    project_label = CharBlock(required=False)
    image = StreamBlock([
        ('svg_image', DocumentChooserBlock(label="SVG Image", required=False, help_text="SVG format only", icon="image")),
        ('other_image', ImageChooserBlock(label="Other Image", required=False, help_text="JPEG/PNG format", icon="image")),
    ], required=False, max_num=1)

    class Meta:
        icon = "arrow-right"
        template = "public/blocks/webapp_block/webapp_next.html"


class WebAppPageBlock(StreamBlock):
    header_block = WebAppHeaderBlock()
    brief_block = WebAppBriefBlock()
    image_block = WebAppImageBlock()
    interview_block = WebAppResearchInterviewBlock()
    discussion_block = WebAppResearchDiscussionBlock()
    flow_block = WebAppResearchFlowBlock()
    next_block = NextProjectBlock()