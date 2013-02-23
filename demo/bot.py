
from gnotty.bots import RSSBot


class MezzanineBot(RSSBot):

    def __init__(self, *args, **kwargs):
        kwargs["feeds"] = [
            "http://stackoverflow.com/feeds/tag/mezzanine",
            "http://stackoverflow.com/feeds/tag/cartridge",
        ]
        super(MezzanineBot, self).__init__(*args, **kwargs)
