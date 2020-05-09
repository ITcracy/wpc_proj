from django.db import models
from django.db.models.fields import TextField
from wagtail.admin.edit_handlers import (FieldPanel, MultiFieldPanel,
                                         StreamFieldPanel)
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

from home.blocks import AboutStreamBlock


class AboutPage(Page):
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.PROTECT,
        related_name='+',
        help_text='Main image for the page',
        verbose_name='Main image')
    main_header = models.CharField(
        max_length=100,
        verbose_name='Main header',
        help_text='Text to displayed on the main image. Max 100 chars.')
    main_body = TextField(
        max_length=300,
        verbose_name='Image brief body',
        help_text='Few lines to be displayed on the image. Max 300 chars.')
    about_body = StreamField(
        AboutStreamBlock(), verbose_name="Page body", blank=True)
    lower_section = StreamField(
        AboutStreamBlock(), verbose_name="Lower section", blank=True)
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                ImageChooserPanel("main_image"),
                FieldPanel("main_header"),
                FieldPanel("main_body", classname="full"),
            ],
            heading="Hero Section"),
        StreamFieldPanel('about_body'),
        StreamFieldPanel('lower_section'),
    ]
    parent_page_types = ['home.HomePage']
