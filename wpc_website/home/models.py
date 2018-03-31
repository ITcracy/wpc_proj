from __future__ import absolute_import, unicode_literals
from django.db import models
from django.db.models.fields import TextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, PageChooserPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

from .social_media import TwitterBlock


class HomePage(Page):
    slider_image1 = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.PROTECT,
        related_name='+',
        help_text='First image for the slider.',
        verbose_name='First Image'
    )
    slider_image2 = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.PROTECT,
        related_name='+',
        help_text='Second image for the slider.',
        verbose_name='Second Image'
    )
    slider_image3 = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.PROTECT,
        related_name='+',
        help_text='Third image for the slider.',
        verbose_name='Third Image'
    )
    slider_h1 = models.CharField(max_length=100,
                                 verbose_name='First Slider Text',
                                 help_text='Text to displayed on first image.'
                                 )
    slider_h2 = models.CharField(max_length=100,
                                 verbose_name='Second Slider Text',
                                 help_text='Text to displayed on second image.'
                                 )
    slider_h3 = models.CharField(max_length=100,
                                 verbose_name='Third Slider Text',
                                 help_text='Text to displayed on third image.'
                                 )
    brief_heading = models.CharField(max_length=40,
                                     verbose_name='Brief Title',
                                     help_text='WPC in 40 characters.')
    brief_body = TextField(max_length=450,
                           verbose_name='Brief Body',
                           help_text='WPC in short. First words that a user will read about WPC.')
    vision_heading = models.CharField(max_length=30)
    vision_body = TextField(max_length=150)
    agenda_h1 = models.CharField(max_length=50)
    agenda_body1 = TextField(max_length=255)
    agenda_h2 = models.CharField(max_length=50)
    agenda_body2 = TextField(max_length=255)
    agenda_h3 = models.CharField(max_length=50)
    agenda_body3 = TextField(max_length=255)
    agenda_h4 = models.CharField(max_length=50)
    agenda_body4 = TextField(max_length=255)

    featured_works_title = models.CharField(
        null=True,
        blank=True,
        max_length=40,
        help_text='Title to displayed for works section.'
    )

    featured_works = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Will display 3 featured works.',
        verbose_name='Works Page Link'
    )

    twitter_block = StreamField([
        ('twitter', TwitterBlock())
    ],
        null=True,
        blank=True,
        verbose_name='Twitter Link',
        help_text='Link the twitter handle here.')

    featured_blog_title = models.CharField(
        null=True,
        blank=True,
        max_length=40,
        help_text='Title to displayed for blog section.'
    )

    featured_blog_tagline = models.CharField(
        max_length=200,
        verbose_name='Blog Tagline',
        help_text='A tagline for blogs.'
    )

    featured_blog = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Will display 3 featured blogs.',
        verbose_name='Blogs Page Link'
    )

    quote_for_the_day = models.CharField(max_length=150, null=True, blank=True)
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel("slider_image1"),
            FieldPanel("slider_h1"),
            ImageChooserPanel("slider_image2"),
            FieldPanel("slider_h2"),
            ImageChooserPanel("slider_image3"),
            FieldPanel("slider_h3"),
        ], heading="Slider Section"),

        MultiFieldPanel([
            FieldPanel("brief_heading"),
            FieldPanel("brief_body", classname="full"),
            ], heading="Brief Section", classname="collapsible"),

        MultiFieldPanel([
            FieldPanel("vision_heading"),
            FieldPanel("vision_body", classname="full"),
            FieldPanel("agenda_h1"),
            FieldPanel("agenda_body1", classname="full"),
            FieldPanel("agenda_h2"),
            FieldPanel("agenda_body2", classname="full"),
            FieldPanel("agenda_h3"),
            FieldPanel("agenda_body3", classname="full"),
            FieldPanel("agenda_h4"),
            FieldPanel("agenda_body4", classname="full"),
        ], heading="Vision & Agenda", classname="collapsible"),

        MultiFieldPanel([
            MultiFieldPanel([
                FieldPanel('featured_works_title'),
                PageChooserPanel('featured_works'),
            ]),
        ], heading="Featured Works Section", classname="collapsible"),

        FieldPanel("quote_for_the_day", classname="full"),
        StreamFieldPanel('twitter_block'),
        MultiFieldPanel([
            MultiFieldPanel([
                FieldPanel('featured_blog_title'),
                FieldPanel('featured_blog_tagline'),
                PageChooserPanel('featured_blog'),
            ]),
        ], heading="Featured Blogs Section", classname="collapsible")
    ]
