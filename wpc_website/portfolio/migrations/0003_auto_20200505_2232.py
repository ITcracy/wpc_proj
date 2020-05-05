# Generated by Django 3.0.5 on 2020-05-05 17:02

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_auto_20181007_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workimagepage',
            name='work_desc',
            field=wagtail.core.fields.StreamField([('heading_block', wagtail.core.blocks.StructBlock([('heading_text', wagtail.core.blocks.CharBlock(classname='title', required=True)), ('size', wagtail.core.blocks.ChoiceBlock(blank=True, choices=[('', 'Select a header size'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4')], required=False)), ('alignment', wagtail.core.blocks.ChoiceBlock(blank=False, choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')]))])), ('paragraph_block', wagtail.core.blocks.StructBlock([('alignment', wagtail.core.blocks.ChoiceBlock(blank=False, choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')])), ('paragraph_text', wagtail.core.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'hr', 'ol', 'ul', 'link', 'document-link'], icon='fa-paragraph'))])), ('image_block', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('caption', wagtail.core.blocks.CharBlock(required=False)), ('attribution', wagtail.core.blocks.CharBlock(required=False))])), ('block_quote', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.TextBlock()), ('attribute_name', wagtail.core.blocks.CharBlock(blank=True, label='e.g. Mary Berry', required=False))])), ('embed_block', wagtail.embeds.blocks.EmbedBlock(help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks', icon='fa-s15', template='blocks/embed_block.html'))], help_text='A complete description of the work.', verbose_name='Work Description'),
        ),
    ]
