from django.db import models

# Create your models here.
from django.db.models.fields import TextField, DateField
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from home.blocks import BaseStreamBlock

#
# class WorkPreviewPage(Page):
#     """
#     This is a page preview of work. The content of this page will be displayed on the
#     PortfolioIndexPage.
#     """


class CarouselItem(Orderable):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    page = ParentalKey('WorkImagePage', related_name='carousel_items')
    panels = [
        ImageChooserPanel('image')
    ]


class WorkImagePage(Page):
    """
    This is a page describing work. This page will contain images along with text.
    """
    preview_image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.PROTECT,
        related_name='+',
        help_text='Image for the preview.',
        verbose_name='Preview Image')
    preview_heading = models.CharField(
        max_length=50,
        verbose_name='Preview Title',
        help_text='One liner for this work that will be displayed '
                  'as a heading with preview image. '
                  'Max 50 characters.')

    work_summary = TextField(
        max_length=800,
        verbose_name='Work Summary',
        help_text='A short summary of the work. Max 800 chars.')
    work_date = models.DateField(
        verbose_name='Date',
        help_text='Date/Start date of the work.',
        blank=True,
        null=True)

    work_video_title = models.CharField(
        null=True,
        blank=True,
        max_length=50, help_text='Max 50 chars.')

    work_video_subtitle = models.CharField(
        null=True,
        blank=True,
        max_length=100, help_text='Max 100 chars.')

    work_video_image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='+',
        help_text='Screenshot image of the video',
        verbose_name='Video screenshot/image.')
    work_video_url = models.URLField(
        verbose_name='Video URL',
        null=True,
        blank=True,
        help_text='Paste the video url from youtube.')

    work_desc = StreamField(
        BaseStreamBlock(), verbose_name='Work Description',
        help_text='A complete description of the work.')

    content_panels = Page.content_panels + [
            MultiFieldPanel(
                [
                    ImageChooserPanel("preview_image"),
                    FieldPanel("preview_heading"),
                ],
                heading="Preview Section", help_text=''),
            InlinePanel('carousel_items', label="Work Images"),
            FieldPanel("work_summary", classname="full"),
            FieldPanel("work_date"),

            MultiFieldPanel(
                [
                    FieldPanel("work_video_title"),
                    FieldPanel("work_video_subtitle"),
                    ImageChooserPanel('work_video_image'),
                    FieldPanel('work_video_url'),
                ],
                heading="Work Video",
                classname="collapsible"),
            StreamFieldPanel('work_desc'),
        ]
    # Specifies parent to WorkImagePage as being BlogIndexPages
    parent_page_types = ['PortfolioIndexPage']


class PortfolioIndexPage(Page):
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.PROTECT,
        related_name='+',
        help_text='Image for the header.',
        verbose_name='Header Image')
    portfolio_heading = models.CharField(
        max_length=50,
        verbose_name='Portfolio Title',
        help_text='One liner for all the works. Max 50 chars.')
    portfolio_body = TextField(
        max_length=500,
        verbose_name='Portfolio Body',
        help_text='Brief about portfolio. Max 500 chars.')

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                ImageChooserPanel("header_image"),
                FieldPanel("portfolio_heading"),
                FieldPanel("portfolio_body", classname="full"),
            ],
            heading="Header Section")
    ]

    parent_page_types = ['home.HomePage']
    # Speficies that only PortfolioPage objects can live under this index page
    subpage_types = ['WorkImagePage']

    # Defines a method to access the children of the page (e.g. PortfolioPage
    # objects). On the demo site we use this on the HomePage
    def children(self):
        return self.get_children().specific().live()

    # Overrides the context to list all child items, that are live, by the
    # date that they were published
    # http://docs.wagtail.io/en/latest/getting_started/tutorial.html#overriding-context
    def get_context(self, request):
        context = super(PortfolioIndexPage, self).get_context(request)
        context['works'] = WorkImagePage.objects.descendant_of(
            self).live().order_by('-work_date')
        context['portfolio_page'] = self
        return context

    def serve_preview(self, request, mode_name):
        # Needed for previews to work
        return self.serve(request)

    # Returns the child PortfolioPage objects for this BlogPageIndex.
    # If a tag is used then it will filter the posts by tag.
    # If a category is used then it will filter the posts by category.
    def get_recent_works(self):
        works = WorkImagePage.objects.live().descendant_of(self)[:6]

        return works


