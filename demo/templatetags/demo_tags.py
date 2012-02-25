
from mezzanine import template


register = template.Library()


@register.filter
def retweets_in_search_fixer(tweets):
    """
    Retweets in Twitter's search data don't contain a proper retweet
    structure and come out using the old "RT" format. Fix them.
    """
    for i, tweet in enumerate(tweets):
        if tweet.text.startswith("RT "):
            tweets[i].text = tweet.text.replace("RT ", "")
        else:
            link = '<a href="http://twitter.com/%s">@%s</a>: '
            link %= (tweet.user_name, tweet.user_name)
            tweets[i].text = link + tweets[i].text
    return tweets
