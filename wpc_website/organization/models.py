from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

# Create your models here.


@register_snippet
class Organization(models.Model):
    """
    Database model to store list of organization supporting WPC movement
    """
    name = models.CharField("Org Name", max_length=100)
    address = models.TextField(
        "Address", help_text="Organization full address")
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.PROTECT,
        related_name='+',
        help_text='Company logo or some reference image.',
        verbose_name='Company Image')
    website = models.URLField(
        'Organization Website',
        null=True,
        blank=True,
        help_text='Organization website url')
    intro = models.CharField(
        'Introduction',
        help_text='A small intro about the organization.',
        max_length=120,
        null=True,
        blank=True)
    panels = [
        FieldPanel('name'),
        FieldPanel('address'),
        ImageChooserPanel('image'),
        FieldPanel('website'),
        FieldPanel('intro')
    ]

    search_fields = Page.search_fields + [
        index.SearchField('name'),
        index.SearchField('address'),
    ]

    def __str__(self):
        return '{}'.format(self.name)


class OrganizationPage(Page):
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
    parent_page_types = ['home.HomePage']
    subpage_types = []
