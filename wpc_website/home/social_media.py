
from wagtail.core import blocks


class TwitterBlock(blocks.StructBlock):
    twitter_box_username = blocks.CharBlock(
        required=True,
        verbose_name='Username',
        help_text='Username or the Screenname of the twitter handle.')
    twitter_box_tweet_limit = blocks.IntegerBlock(
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


class WireBlock(blocks.StructBlock):
    search_keywords = blocks.CharBlock(
        required=True,
        default='',
        verbose_name='Keywords',
        help_text='Comma separated values for which the news and articles '
                  'from The Wire will be displayed.'
    )

    wire_url = 'https://thewire.in/wp-json/thewire/v2/posts/search?keyword=labour,worker,economy&' \
               'orderby=date&per_page=5&page=1&type=opinion'
