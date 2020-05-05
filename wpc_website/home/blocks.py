from wagtail.core.blocks import (CharBlock, ChoiceBlock, RichTextBlock,
                                 StreamBlock, StructBlock, TextBlock)
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock


class ImageBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """
    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)

    class Meta:
        icon = 'image'
        template = "blocks/image_block.html"


class FullWidthImageBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """
    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)

    class Meta:
        icon = 'image'
        template = "blocks/image_full_width_block.html"


class HeadingBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to select h2 - h4 sizes for headers
    """
    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(
        choices=[('', 'Select a header size'), ('h2', 'H2'), ('h3', 'H3'),
                 ('h4', 'H4')],
        blank=True,
        required=False)
    alignment = ChoiceBlock(
        [('left', 'Left'), ('center', 'Center'), ('right', 'Right')],
        blank=False,
        required=True
    )

    class Meta:
        icon = "title"
        template = "blocks/heading_block.html"


class BlockQuote(StructBlock):
    """
    Custom `StructBlock` that allows the user to attribute a quote to the author
    """
    text = TextBlock()
    attribute_name = CharBlock(
        blank=True, required=False, label='e.g. Mary Berry')

    class Meta:
        icon = "fa-quote-left"
        template = "blocks/blockquote.html"


class TextEditorBlock(StructBlock):
    alignment = ChoiceBlock(
        [('left', 'Left'), ('center', 'Center'), ('right', 'Right')],
        blank=False,
        required=True
    )
    paragraph_text = RichTextBlock(
        icon="fa-paragraph",
        features=['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'bold',
                  'italic', 'hr', 'ol', 'ul', 'link', 'document-link'])

    class Meta:
        icon = "fa-quote-left"
        template = "blocks/paragraph_block.html"


# StreamBlocks
class BaseStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """
    heading_block = HeadingBlock()
    paragraph_block = TextEditorBlock()
    image_block = ImageBlock()
    block_quote = BlockQuote()
    embed_block = EmbedBlock(
        help_text=
        'Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks',
        icon="fa-s15",
        template="blocks/embed_block.html")


class AboutStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """
    heading_block = HeadingBlock()
    paragraph_block = TextEditorBlock()
    image_block = ImageBlock()
    full_width_image_block = FullWidthImageBlock()
    block_quote = BlockQuote()
    embed_block = EmbedBlock(
        help_text=
        'Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks',
        icon="fa-s15",
        template="blocks/embed_block.html")
