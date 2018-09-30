from django import template

from home.models import FooterText

register = template.Library()


@register.inclusion_tag('tags/footer_text.html', takes_context=True)
def get_footer_text(context):
    footer_text = ""
    footer_title = ""
    phone_one = ""
    phone_two = ""
    phone_three = ""
    email = ""
    fb_link = ""
    twitter_link = ""

    if FooterText.objects.first() is not None:
        footer_text = FooterText.objects.first().f_body
        footer_title = FooterText.objects.first().f_title
        phone_one = FooterText.objects.first().phone_one
        phone_two = FooterText.objects.first().phone_two
        phone_three = FooterText.objects.first().phone_three
        email = FooterText.objects.first().email
        fb_link = FooterText.objects.first().fb_link
        twitter_link = FooterText.objects.first().twitter_link

    return {
        'footer_text': footer_text,
        'footer_title': footer_title,
        'phone_one': phone_one,
        'phone_two': phone_two,
        'phone_three': phone_three,
        'email': email,
        'fb_link': fb_link,
        'twitter_link': twitter_link,
        'request': context['request'],
    }
