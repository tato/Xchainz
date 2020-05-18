import feedparser, pytz
from datetime import datetime, timedelta
from rfeed import *


madrid = pytz.timezone('Europe/Madrid')


def date_is_yesterday(date):
    yesterday = datetime.now(madrid) - timedelta(days=1)
    date = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %z')
    return yesterday.date() == date.date()


def make_item_from_entry(entry):
    return Item(
        title=entry.title,
        link=entry.link,
        description=entry.description,
        author=entry.author,
        guid=Guid(entry.guid),
        pubDate=datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z'),
    )
    

def main():
    d = feedparser.parse('https://rockpapershotgun.com/feed')
    yday = [ make_item_from_entry(e) for e in d.entries if date_is_yesterday(e.published) ]
    feed = Feed(
        title=d.feed.title,
        link=d.feed.link,
        description=d.feed.description,
        language=d.feed.language,
        lastBuildDate=datetime.strptime(d.feed.updated, '%a, %d %b %Y %H:%M:%S %z'),
        items = yday
    )
    with open('output.xml', 'w') as f:
        f.write(feed.rss())


if __name__ == '__main__':
    main()