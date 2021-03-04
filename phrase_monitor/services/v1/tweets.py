import traceback

from phrase_monitor.application import db
from phrase_monitor.libs.logger import Logger


class TweetService:

    @staticmethod
    def get_feeds():
        try:
            feeds_data = db.execute("SELECT * from blogs").fetchall()
            feeds = []
            for feed in feeds_data:
                feeds.append({
                    'user_id': feed.user_id,
                    'text': feed.text,
                    'created_date': feed.created_date
                })
        except Exception as ex:
            feeds = None
            db.rollback()
            Logger.error(__name__, "get_feeds", "02", "Exception occurred: {}".format(str(ex)),
                         traceback.format_exc())
        return feeds
