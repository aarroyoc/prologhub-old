from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models

from blog.models import BlogPost

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.users.models import UserProfile

SUBPAGE_TYPES = ['blog.BlogPost', 'blog.ExternalBlogPost']


class HomePage(Page):
    about = RichTextField(blank=True, features=['bold', 'italic', 'link'])
    main_featured_post = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    featured_post1 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    featured_post2 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('about', classname="full"),
        MultiFieldPanel([
            PageChooserPanel('main_featured_post', SUBPAGE_TYPES),
            PageChooserPanel('featured_post1', SUBPAGE_TYPES),
            PageChooserPanel('featured_post2', SUBPAGE_TYPES)
        ], heading="Featured Posts")
    ]

    subpage_types = SUBPAGE_TYPES

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        tag = request.GET.get('tag')
        category = request.GET.get('category')
        author = request.GET.get('author')
        page = request.GET.get('page')

        if category:
            blogpages = self.get_children().live().filter(models.Q(externalblogpost__categories__name=category)|models.Q(blogpost__categories__name=category)).order_by('-first_published_at')
            search = f"in category: \"{category}\""
        elif tag:
            blogpages = self.get_children().live().filter(models.Q(externalblogpost__tags__name=tag)|models.Q(blogpost__tags__name=tag)).order_by('-first_published_at')
            search = f"tagged: \"{tag}\""
        elif author:
            blogpages = self.get_children().live().filter(owner__username=author).order_by('-first_published_at')
            if len(blogpages) > 0:
                owner = blogpages[0].owner
                search = f"written by: \"{owner.first_name} {owner.last_name}\""
            else:
                search = "we don't recognize that author"
        else:
            blogpages = self.get_children().live().order_by('-first_published_at')
            search = False

        paginator = Paginator(blogpages, 7)

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = super().get_context(request)
        context['blogpages'] = posts
        context['search'] = search
        return context
