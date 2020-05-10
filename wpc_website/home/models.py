from __future__ import absolute_import, unicode_literals

from django.core.validators import RegexValidator
from django.db import models
from django.db.models.fields import TextField
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (FieldPanel, FieldRowPanel,
                                         InlinePanel, MultiFieldPanel,
                                         PageChooserPanel, StreamFieldPanel)
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

from .social_media import TwitterBlock


class HomePage(Page):
    slider_image1 = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.PROTECT,
        related_name='+',
        help_text='First image for the slider.',
        verbose_name='First Image')
    slider_image2 = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.PROTECT,
        related_name='+',
        help_text='Second image for the slider.',
        verbose_name='Second Image')
    slider_image3 = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.PROTECT,
        related_name='+',
        help_text='Third image for the slider.',
        verbose_name='Third Image')
    slider_h1 = models.CharField(
        max_length=100,
        verbose_name='First Slider Text',
        help_text='Text to displayed on first image. Max 100 chars.')
    slider_h2 = models.CharField(
        max_length=100,
        verbose_name='Second Slider Text',
        help_text='Text to displayed on second image. Max 100 chars.')
    slider_h3 = models.CharField(
        max_length=100,
        verbose_name='Third Slider Text',
        help_text='Text to displayed on third image. Max 100 chars.')
    brief_heading = models.CharField(
        max_length=50,
        verbose_name='Brief Title',
        help_text='One liner for WPC. Max 50 characters.')
    brief_body = TextField(
        max_length=500,
        verbose_name='Brief Body',
        help_text='WPC in short. First words that a user will read about WPC. Max 500 chars.')
    vision_heading = models.CharField(max_length=50, help_text='Max 50 chars.')
    vision_body = TextField(max_length=250, help_text='Max 250 chars.')
    agenda_h1 = models.CharField(max_length=50, help_text='Max 50 chars.')
    agenda_body1 = TextField(max_length=255, help_text='Max 255 chars.')
    agenda_page1 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Will open up the agenda page.',
        verbose_name='Agenda Page Link')

    agenda_h2 = models.CharField(max_length=50, help_text='Max 50 chars.')
    agenda_body2 = TextField(max_length=255, help_text='Max 255 chars.')
    agenda_page2 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Will open up the agenda page.',
        verbose_name='Agenda Page Link')

    agenda_h3 = models.CharField(max_length=50, help_text='Max 50 chars.')
    agenda_body3 = TextField(max_length=255, help_text='Max 255 chars.')
    agenda_page3 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Will open up the agenda page.',
        verbose_name='Agenda Page Link')

    agenda_h4 = models.CharField(max_length=50, help_text='Max 50 chars.')
    agenda_body4 = TextField(max_length=255, help_text='Max 255 chars.')
    agenda_page4 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Will open up the agenda page.',
        verbose_name='Agenda Page Link')

    more_about_us = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Will open up the page having details about WPC.',
        verbose_name='More About US Page Link')

    home_video_title = models.CharField(null=True, blank=True,
                                        max_length=50, help_text='Max 50 chars.')
    home_video_subtitle = models.CharField(
        null=True, blank=True, max_length=100, help_text='Max 100 chars.')
    home_video_image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.PROTECT,
        related_name='+',
        null=True,
        blank=True,
        help_text='Screenshot image of the video',
        verbose_name='Video screenshot/image.')
    home_video_url = models.URLField(
        null=True,
        blank=True,
        verbose_name='Video URL',
        help_text='Paste the video url from youtube.')

    featured_works_title = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        help_text='Title to displayed for works section. Max 50 chars.')

    featured_works = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Will display 3 featured works.',
        verbose_name='Works Page Link')

    social_board_title = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        help_text='Title to displayed for social board section. Max 50 chars.')

    social_board_body = TextField(max_length=300,
                                  blank=True,
                                  null=True,
                                  help_text='Text to displayed '
                                            'just below the social board section. '
                                            'Max 300 chars.')

    twitter_block = StreamField(
        [('twitter', TwitterBlock())],
        null=True,
        blank=True,
        verbose_name='Social Board',
        help_text='Link the social accounts here.')

    featured_blog_title = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        help_text='Title to displayed for blog section.Max 50 chars.')

    featured_blog_tagline = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        verbose_name='Blog Tagline',
        help_text='A tagline for blogs. Max 100 chars.')

    featured_blog = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Will display 3 featured blogs.',
        verbose_name='Blogs Page Link')

    quote_for_the_day = models.CharField(max_length=500, default="Some Quote",
                                         help_text='Max 500 chars.')
    quote_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='+',
        help_text='Image for the quote.',
        verbose_name='Quote Image')

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                ImageChooserPanel("slider_image1"),
                FieldPanel("slider_h1"),
                ImageChooserPanel("slider_image2"),
                FieldPanel("slider_h2"),
                ImageChooserPanel("slider_image3"),
                FieldPanel("slider_h3"),
            ],
            heading="Slider Section"),
        MultiFieldPanel(
            [
                FieldPanel("brief_heading"),
                FieldPanel("brief_body", classname="full"),
            ],
            heading="Brief Section",
            classname="collapsible"),
        MultiFieldPanel(
            [
                FieldPanel("vision_heading"),
                FieldPanel("vision_body", classname="full"),
                FieldPanel("agenda_h1"),
                FieldPanel("agenda_body1", classname="full"),
                PageChooserPanel('agenda_page1'),
                FieldPanel("agenda_h2"),
                FieldPanel("agenda_body2", classname="full"),
                PageChooserPanel('agenda_page2'),
                FieldPanel("agenda_h3"),
                FieldPanel("agenda_body3", classname="full"),
                PageChooserPanel('agenda_page3'),
                FieldPanel("agenda_h4"),
                FieldPanel("agenda_body4", classname="full"),
                PageChooserPanel('agenda_page4'),
                PageChooserPanel('more_about_us'),
            ],
            heading="Vision & Agenda",
            classname="collapsible"),
        MultiFieldPanel(
            [
                FieldPanel("home_video_title"),
                FieldPanel("home_video_subtitle"),
                ImageChooserPanel('home_video_image'),
                FieldPanel('home_video_url'),
            ],
            heading="Home Video",
            classname="collapsible"),
        MultiFieldPanel(
            [
                MultiFieldPanel([
                    FieldPanel('featured_works_title'),
                    PageChooserPanel('featured_works'),
                ]),
            ],
            heading="Featured Works Section",
            classname="collapsible"),
        MultiFieldPanel(
            [
                MultiFieldPanel([
                    FieldPanel("quote_for_the_day", classname="full"),
                    ImageChooserPanel('quote_image'),
                ]),
            ],
            heading="Quote Section",
            classname="collapsible"),
        MultiFieldPanel(
            [
                MultiFieldPanel([
                    FieldPanel('social_board_title'),
                    FieldPanel('social_board_body'),
                    StreamFieldPanel('twitter_block'),
                ]),
            ],
            heading="Social Board Section",
            classname="collapsible"),
        MultiFieldPanel(
            [
                MultiFieldPanel([
                    FieldPanel('featured_blog_title'),
                    FieldPanel('featured_blog_tagline'),
                    PageChooserPanel('featured_blog'),
                ]),
            ],
            heading="Featured Blogs Section",
            classname="collapsible")
    ]
    parent_page_types = ['wagtailcore.Page']


class FormField(AbstractFormField):
    """
    Wagtailforms is a module to introduce simple forms on a Wagtail site. It
    isn't intended as a replacement to Django's form support but as a quick way
    to generate a general purpose data-collection form or contact form
    without having to write code. We use it on the site for a contact form. You
    can read more about Wagtail forms at:
    http://docs.wagtail.io/en/latest/reference/contrib/forms/index.html
    """
    page = ParentalKey(
        'FormPage', related_name='form_fields', on_delete=models.CASCADE)


class FormPage(AbstractEmailForm):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+')
    body = TextField(
        max_length=450,
        verbose_name='Brief Image Body',
        help_text='Few words to display on main image.')
    additional_info = RichTextField(
        features=['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'bold',
                  'italic', 'hr', 'ol', 'ul', 'link', 'document-link'],
        blank=True, help_text='Additional Info about the page.')
    thank_you_text = RichTextField(blank=True,
                                   features=['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'bold',
                                             'italic', 'hr', 'ol', 'ul', 'link', 'document-link'],)

    # Note how we include the FormField object via an InlinePanel using the
    # related_name value
    content_panels = AbstractEmailForm.content_panels + [
        ImageChooserPanel('image'),
        FieldPanel('body'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('additional_info', classname="full"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]
    parent_page_types = ['home.HomePage']


@register_snippet
class FooterText(models.Model):
    """
    This provides editable text for the site footer. Again it uses the decorator
    `register_snippet` to allow it to be accessible via the admin. It is made
    accessible on the template via a template tag defined in home/templatetags/
    navigation_tags.py
    """
    f_title = models.CharField(
        max_length=50,
        verbose_name='Title',
        help_text='Text to displayed as footer title. Max 50 chars.')
    f_body = RichTextField(verbose_name='Body',
                           features=['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'bold',
                                     'italic', 'hr', 'ol', 'ul', 'link', 'document-link'],
                           )

    phone_regex = RegexValidator(regex=r'^\+?1?\d{8,15}$',
                                 message="Upto 15 digits allowed.")
    # validators should be a list
    phone_one = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    phone_two = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    phone_three = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    email = models.EmailField(blank=True)
    fb_link = models.TextField(blank=True)
    twitter_link = models.TextField(blank=True)

    panels = [
        FieldPanel('f_title'),
        FieldPanel('f_body'),
        FieldPanel('phone_one'),
        FieldPanel('phone_two'),
        FieldPanel('phone_three'),
        FieldPanel('email'),
        FieldPanel('fb_link'),
        FieldPanel('twitter_link')
    ]

    def __str__(self):
        return "Footer text"

    class Meta:
        verbose_name_plural = 'Footer Text'
