
from wagtail.core import blocks


class TwitterBlock(blocks.StructBlock):
    twitter_box_username = blocks.CharBlock(
        required=True,
        verbose_name='Username',
        help_text='Username or the Screenname of the twitter handle.')
    twitter_box_tweet_limit = blocks.CharBlock(
        required=True,
        max_length=2,
        default=2,
        verbose_name='Tweets limit',
        help_text='Max number of tweets to be displayed on the homepage. Default will be 2.'
    )

    class Meta:
        template = 'blocks/twitter.html'
        icon = 'cogs'
        label = 'Twitter Widget'