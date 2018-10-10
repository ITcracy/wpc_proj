from __future__ import unicode_literals

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import redirect, render
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from taggit.models import Tag, TaggedItemBase
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         StreamFieldPanel)
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import StreamField
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from home.blocks import BaseStreamBlock


@register_snippet
class People(ClusterableModel):
    """
    A Django model to store People objects.
    It uses the `@register_snippet` decorator to allow it to be accessible
    via the Snippets UI (e.g. /admin/snippets/base/people/)

    `People` uses the `ClusterableModel`, which allows the relationship with
    another model to be stored locally to the 'parent' model (e.g. a PageModel)
    until the parent is explicitly saved. This allows the editor to use the
    'Preview' button, to preview the content, without saving the relationships
    to the database.
    https://github.com/wagtail/django-modelcluster
    """
    first_name = models.CharField("First name", max_length=254, help_text='Max 254 chars.')
    last_name = models.CharField("Last name", max_length=254, help_text='Max 254 chars.')
    job_title = models.CharField("Job title", max_length=254, help_text='Max 254 chars.')

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+')

    panels = [
        FieldPanel('first_name'),
        FieldPanel('last_name'),
        FieldPanel('job_title'),
        ImageChooserPanel('image')
    ]

    search_fields = Page.search_fields + [
        index.SearchField('first_name'),
        index.SearchField('last_name'),
    ]

    @property
    def thumb_image(self):
        # Returns an empty string if there is no profile pic or the rendition
        # file can't be found.
        try:
            return self.image.get_rendition('fill-50x50').img_tag()
        except:
            return ''

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'


class BlogPeopleRelationship(Orderable, models.Model):
    """
    This defines the relationship between the `People` and the BlogPage below.
    This allows People to be added to a BlogPage.

    We have created a two way relationship between BlogPage and People using
    the ParentalKey and ForeignKey
    """
    page = ParentalKey(
        'BlogPage',
        related_name='blog_person_relationship',
        on_delete=models.CASCADE)
    people = models.ForeignKey(
        'People',
        related_name='person_blog_relationship',
        on_delete=models.CASCADE)
    panels = [SnippetChooserPanel('people')]


class BlogCategoryRelationship(Orderable, models.Model):
    page = ParentalKey('BlogPage', related_name='categories')
    category = models.ForeignKey(
        'BlogCategory', related_name='+', on_delete=models.CASCADE)
    panels = [FieldPanel('category')]


class BlogPageTag(TaggedItemBase):
    """
    This model allows us to create a many-to-many relationship between
    the BlogPage object and tags. There's a longer guide on using it at
    http://docs.wagtail.io/en/latest/reference/pages/model_recipes.html#tagging
    """
    content_object = ParentalKey(
        'BlogPage', related_name='tagged_items', on_delete=models.CASCADE)


@register_snippet
class BlogCategory(ClusterableModel):
    name = models.CharField(
        max_length=80, unique=True, verbose_name=_('Category Name'))
    slug = models.SlugField(unique=True, max_length=80, help_text='Max 80 chars.')
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name="children",
        on_delete=models.CASCADE,
        help_text=_(
            'Categories, unlike tags, can have a hierarchy. You might have a '
            'Jazz category, and under that have children categories for Bebop'
            ' and Big Band. Totally optional.'))
    description = models.CharField(max_length=500, blank=True,
                                   help_text='Description for the category. Max 500 chars.')

    class Meta:
        ordering = ['name']
        verbose_name = _("Blog Category")
        verbose_name_plural = _("Blog Categories")

    panels = [
        FieldPanel('name'),
        FieldPanel('parent'),
        FieldPanel('description'),
    ]

    def __str__(self):
        return self.name

    def clean(self):
        if self.parent:
            parent = self.parent
            if self.parent == self:
                raise ValidationError('Parent category cannot be self.')
            if parent.parent and parent.parent == self:
                raise ValidationError('Cannot have circular Parents.')

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            count = BlogCategory.objects.filter(slug=slug).count()
            if count > 0:
                slug = '{}-{}'.format(slug, count)
            self.slug = slug
        return super(BlogCategory, self).save(*args, **kwargs)


class BlogPage(Page):
    """
    A Blog Page

    We access the People object with an inline panel that references the
    ParentalKey's related_name in BlogPeopleRelationship. More docs:
    http://docs.wagtail.io/en/latest/topics/pages.html#inline-models
    """
    introduction = models.TextField(
        help_text='Text to describe the page', blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=
        'Landscape mode only; horizontal width between 1000px and 3000px.')
    body = StreamField(BaseStreamBlock(), verbose_name="Page body", blank=True)
    subtitle = models.CharField(blank=True, max_length=255, help_text='Max 255 chars.')
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    date_published = models.DateField(
        "Date article published", blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle', classname="full"),
        FieldPanel('introduction', classname="full"),
        ImageChooserPanel('image'),
        StreamFieldPanel('body'),
        FieldPanel('date_published'),
        InlinePanel(
            'blog_person_relationship',
            label="Author(s)",
            panels=None,
            min_num=1),
        InlinePanel(
            'categories',
            label='Category',
            panels=None,
            min_num=0,
        ),
        FieldPanel('tags'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    def authors(self):
        """
        Returns the BlogPage's related People. Again note that we are using
        the ParentalKey's related_name from the BlogPeopleRelationship model
        to access these objects. This allows us to access the People objects
        with a loop on the template. If we tried to access the blog_person_
        relationship directly we'd print `blog.BlogPeopleRelationship.None`
        """
        authors = [n.people for n in self.blog_person_relationship.all()]

        return authors

    @property
    def get_categories(self):
        categories = [n.category for n in self.categories.all()]
        for category in categories:
            category.url = '/' + '/'.join(
                s.strip('/')
                for s in [self.get_parent().url, 'categories', category.slug])
        return categories

    @property
    def get_tags(self):
        """
        Similar to the authors function above we're returning all the tags that
        are related to the blog post into a list we can access on the template.
        We're additionally adding a URL to access BlogPage objects with that tag
        """
        tags = self.tags.all()
        for tag in tags:
            tag.url = '/' + '/'.join(
                s.strip('/')
                for s in [self.get_parent().url, 'tags', tag.slug])
        return tags

    # Specifies parent to BlogPage as being BlogIndexPages
    parent_page_types = ['BlogIndexPage']

    # Specifies what content types can exist as children of BlogPage.
    # Empty list means that no child content types are allowed.
    subpage_types = []

    @property
    def blog_page(self):
        return self.get_parent().specific

    def get_context(self, request, *args, **kwargs):
        context = super(BlogPage, self).get_context(request, *args, **kwargs)
        context['blog_page'] = self.blog_page
        return context


class BlogIndexPage(RoutablePageMixin, Page):
    """
    Index page for blogs.
    We need to alter the page model's context to return the child page objects,
    the BlogPage objects, so that it works as an index page

    RoutablePageMixin is used to allow for a custom sub-URL for the tag views
    defined above.
    """
    introduction = models.TextField(
        help_text='Text to describe the page', blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=
        'Landscape mode only; horizontal width between 1000px and 3000px.')

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        ImageChooserPanel('image'),
    ]

    # Speficies that only BlogPage objects can live under this index page
    parent_page_types = ['home.HomePage']
    subpage_types = ['BlogPage']

    # Defines a method to access the children of the page (e.g. BlogPage
    # objects). On the demo site we use this on the HomePage
    def children(self):
        return self.get_children().specific().live()

    # Overrides the context to list all child items, that are live, by the
    # date that they were published
    # http://docs.wagtail.io/en/latest/getting_started/tutorial.html#overriding-context
    def get_context(self, request):
        context = super(BlogIndexPage, self).get_context(request)
        context['posts'] = BlogPage.objects.descendant_of(
            self).live().order_by('-date_published')
        context['blog_page'] = self
        return context

    # This defines a Custom view that utilizes Tags. This view will return all
    # related BlogPages for a given Tag or redirect back to the BlogIndexPage.
    # More information on RoutablePages is at
    # http://docs.wagtail.io/en/latest/reference/contrib/routablepage.html
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
        context = {'tag': tag, 'posts': posts, 'blog_page': self}
        return render(request, 'blog/blog_index_page.html', context)

    @route('^categories/$', name='categories_archive')
    @route('^categories/([\w-]+)/$', name='categories_archive')
    def categories_archive(self, request, category=None):
        try:
            category = BlogCategory.objects.get(slug=category)
        except BlogCategory.DoesNotExist:
            if category:
                msg = 'There are no blog posts in "{}" category'.format(
                    category)
                messages.add_message(request, messages.INFO, msg)
            return redirect(self.url)

        posts = self.get_posts(category=category)
        context = {'category': category, 'posts': posts, 'blog_page': self}
        return render(request, 'blog/blog_index_page.html', context)

    def serve_preview(self, request, mode_name):
        # Needed for previews to work
        return self.serve(request)

    # Returns the child BlogPage objects for this BlogPageIndex.
    # If a tag is used then it will filter the posts by tag.
    # If a category is used then it will filter the posts by category.
    def get_posts(self, tag=None, category=None):
        posts = BlogPage.objects.live().descendant_of(self)
        if tag:
            posts = posts.filter(tags=tag)
        if category:
            posts = posts.filter(categories__category=category)
        return posts

    # Returns the list of Tags for all child posts of this BlogPage.
    def get_child_tags(self):
        tags = []
        for post in self.get_posts():
            # Not tags.append() because we don't want a list of lists
            tags += post.get_tags
        tags = sorted(set(tags))
        return tags

    def get_child_categories(self):
        categories = []
        for post in self.get_posts():
            categories += post.get_categories
        categories = sorted(set(categories))
        return categories

    def get_recent_posts(self):
        posts = BlogPage.objects.live().descendant_of(self)[:3]
        return posts
