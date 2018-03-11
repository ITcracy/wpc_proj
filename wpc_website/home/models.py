from __future__ import absolute_import, unicode_literals

from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel


class HomePage(Page):
    slider_image1 = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    slider_image2 = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    slider_image3 = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    slider_h1 = models.CharField(max_length=30)
    slider_h2 = models.CharField(max_length=30)
    slider_h3 = models.CharField(max_length=30)

    brief_heading = models.CharField(max_length=40)
    brief_body = models.CharField(max_length=450)

    vision_heading = models.CharField(max_length=30)
    vision_body = models.CharField(max_length=150)

    agenda_h1 = models.CharField(max_length=50)
    agenda_body1 = models.CharField(max_length=255)

    agenda_h2 = models.CharField(max_length=50)
    agenda_body2 = models.CharField(max_length=255)

    agenda_h3 = models.CharField(max_length=50)
    agenda_body3 = models.CharField(max_length=255)

    recent_work_h1 = models.CharField(max_length=50)
    recent_work_body1 = models.CharField(max_length=255)

    recent_work_h2 = models.CharField(max_length=50)
    recent_work_body2 = models.CharField(max_length=255)

    recent_work_h3 = models.CharField(max_length=50)
    recent_work_body3 = models.CharField(max_length=255)

    quote_for_the_day = models.CharField(max_length=150, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("agenda_h1"),
        FieldPanel("agenda_body1"),
        FieldPanel("agenda_h2"),
        FieldPanel("agenda_body2"),
        FieldPanel("agenda_h3"),
        FieldPanel("agenda_body3"),
        FieldPanel("recent_work_h1"),
        FieldPanel("recent_work_body1"),
        FieldPanel("recent_work_h2"),
        FieldPanel("recent_work_body2"),
        FieldPanel("recent_work_h3"),
        FieldPanel("recent_work_body3"),
        FieldPanel("quote_for_the_day"),
        ImageChooserPanel("slider_image1"),
        ImageChooserPanel("slider_image2"),
        ImageChooserPanel("slider_image3"),
    ]
