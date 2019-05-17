from django import forms

from django.db import models

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase, Tag as TaggitTag

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPost',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class ExternalBlogPostTag(TaggedItemBase):
    content_object = ParentalKey(
        'ExternalBlogPost',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon')
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'blog categories'


class TauPrologCodeBlock(blocks.StructBlock):
    id = blocks.CharBlock(help_text="Used to identify the code block for queries")
    prolog_code = blocks.TextBlock()

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context['rows'] = len(value['prolog_code'].splitlines()) + 1
        return context

    class Meta:
        template = 'blog/blocks/tau_prolog_code_block.html'


class TauPrologQueryBlock(blocks.StructBlock):
    id = blocks.CharBlock(help_text="Used to identify the query to run")
    for_code = blocks.CharBlock(help_text="Must match a Tau Prolog Code Block Id")
    query = blocks.CharBlock()

    class Meta:
        template = 'blog/blocks/tau_prolog_query_block.html'


class BlogPost(Page):
    intro = RichTextField(blank=True, features=['bold', 'italic', 'link'])
    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
    body = StreamField([
        ('content', blocks.RichTextBlock(features=['h2',
                                                  'h3',
                                                  'h4',
                                                  'bold',
                                                  'italic',
                                                  'ol',
                                                  'ul',
                                                  'hr',
                                                  'link',
                                                  'document-link',
                                                  'image',
                                                  'embed',
                                                  'code',
                                                  'superscript',
                                                  'subscript',
                                                  'strikethrough',
                                                  'blockquote'
                                                  ])),
        ('tau_prolog_code', TauPrologCodeBlock()),
        ('tau_prolog_query', TauPrologQueryBlock())
    ])

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
            FieldPanel('tags'),
        ], heading="Post Information"),
        FieldPanel('intro'),
        StreamFieldPanel('body')
    ]

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    parent_page_types = ['home.HomePage']
    subpage_types = []


class ExternalBlogPost(Page):
    intro = RichTextField(blank=True, features=['bold', 'italic', 'link'])
    tags = ClusterTaggableManager(through=ExternalBlogPostTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
    content_location = models.URLField()

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
            FieldPanel('tags'),
        ], heading="Post Information"),
        FieldPanel('intro'),
        FieldPanel('content_location')
    ]

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    parent_page_types = ['home.HomePage']
    subpage_types = []


