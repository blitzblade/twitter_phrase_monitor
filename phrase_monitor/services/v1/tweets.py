import os
import traceback
import time
from phrase_monitor.application import db
from phrase_monitor.libs.logger import Logger


class TweetService:

    @staticmethod
    def get_feeds():
        try:
            query = "SELECT * from blogs"
            feeds_data = db.execute(query).fetchall()
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

    @staticmethod
    def edit_phrase(id, phrase):
        try:
            query = "UPDATE stream_phrases SET phrase = :phrase WHERE id = :id"
            db.execute(query, {"phrase": phrase, "id": id})
            db.commit()
            os.system("sudo systemctl restart twitter-streamer-worker")
            result = True
        except Exception as ex:
            result = False
            db.rollback()
            Logger.error(__name__, "edit_phrase", "02", "Exception occurred: {}".format(str(ex)),
                         traceback.format_exc())
        return result

    @staticmethod
    def get_phrase_by_id(id):
        try:
            query = "SELECT * from stream_phrases WHERE id = :id"
            phrase = db.execute(query, {"id": id}).fetchone()
        except Exception as ex:
            phrase = None
            db.rollback()
            Logger.error(__name__, "get_phrase_by_id", "02", "Exception occurred: {}".format(str(ex)),
                         traceback.format_exc())
        return phrase

    @staticmethod
    def get_phrase_by_name(phrase):
        try:
            query = "SELECT * from stream_phrases WHERE phrase = :phrase"
            phrase = db.execute(query, {"phrase": phrase}).fetchone()
        except Exception as ex:
            phrase = None
            db.rollback()
            Logger.error(__name__, "get_phrase_by_name", "02", "Exception occurred: {}".format(str(ex)),
                         traceback.format_exc())
        return phrase

    @staticmethod
    def add_phrase(user_id, phrase):
        try:
            query = "INSERT INTO stream_phrases (user_id,phrase,created_date) VALUES (:u,:p,:c)"
            ts = time.gmtime()
            timestamp = time.strftime("%x", ts)
            db.execute(query, {"u": user_id, "p": phrase, "c": timestamp})
            db.commit()
            os.system("sudo systemctl restart twitter-streamer-worker")

            result = True
        except Exception as ex:
            result = False
            db.rollback()
            Logger.error(__name__, "get_phrase_by_name", "02", "Exception occurred: {}".format(str(ex)),
                         traceback.format_exc())
        return result

    @staticmethod
    def get_phrases(user_id):
        if user_id is None:
            query = {
                'query': "SELECT * from stream_phrases",
                'params': {}
            }
        else:
            query = {
                'query': "SELECT * from stream_phrases WHERE user_id = :user_id",
                'params': {"user_id": user_id}
            }

        try:

            phrases_data = db.execute(query['query'], query['params']).fetchall()
            phrases = []
            for phrase in phrases_data:
                phrases.append({
                    'phrase': phrase.phrase,
                    'created_date': phrase.created_date
                })
        except Exception as ex:
            phrases = None
            db.rollback()
            Logger.error(__name__, "get_phrases", "02", "Exception occurred: {}".format(str(ex)),
                         traceback.format_exc())
        return phrases

    @staticmethod
    def get_phrase_occurrences():
        try:
            query = """
                    WITH sum_of_minutes AS (SELECT COUNT(created_date) as number_of_times, MAX(created_date) as date, phrase_id FROM tracking
                    GROUP BY phrase_id, created_date)
            	    select number_of_times, date, phrase, phrase_id FROM sum_of_minutes JOIN stream_phrases ON stream_phrases.id = sum_of_minutes.phrase_id;
                    """
            phrase_data = db.execute(query).fetchall()
            # print("phrase_data | ", phrase_data)
            phrase_occurrences = []
            for phrase in phrase_data:
                phrase_occurrences.append({
                    'number_of_times': phrase.number_of_times,
                    'phrase': phrase.phrase,
                    'created_date': phrase.date
                })
        except Exception as ex:
            phrase_occurrences = None
            db.rollback()
            Logger.error(__name__, "get_phrase_occurrences", "02", "Exception occurred: {}".format(str(ex)),
                         traceback.format_exc())
        return phrase_occurrences

    @staticmethod
    def get_average_phrase_per_minute():
        try:
            query = """
                    WITH sum_of_minutes AS (SELECT COUNT(created_date) as number_of_times, MAX(created_date) as date, phrase_id FROM tracking
                    GROUP BY phrase_id, created_date)

                    SELECT SUM(number_of_times) AS number_of_tweets, COUNT(phrase_id) as number_of_entries, MAX(phrase) as phrase FROM sum_of_minutes 
                    JOIN stream_phrases ON stream_phrases.id = sum_of_minutes.phrase_id
                    GROUP BY phrase;
                    """
            phrase_data = db.execute(query).fetchall()

            phrase_occurrences = [
                {"average_per_min": round(float(phrase["number_of_tweets"]) / float(phrase["number_of_entries"]), 2),
                 "phrase": phrase["phrase"]} for phrase in phrase_data]

        except Exception as ex:
            phrase_occurrences = None
            db.rollback()
            Logger.error(__name__, "get_phrase_occurrences", "02", "Exception occurred: {}".format(str(ex)),
                         traceback.format_exc())

        return phrase_occurrences

    @staticmethod
    def get_chart_data_for_minutes():
        try:
            query = """
                    SELECT COUNT(tracking.created_date) as number_of_times, MAX(tracking.created_date) as date, phrase FROM tracking JOIN 
            						stream_phrases ON 
            						tracking.phrase_id = stream_phrases.id WHERE tracking.created_date 
            						BETWEEN CURRENT_TIMESTAMP - INTERVAL '30 minutes' AND CURRENT_TIMESTAMP
                                    GROUP BY phrase, tracking.created_date ORDER BY tracking.created_date asc
                    """
            phrase_data = db.execute(query).fetchall()
            phrase_occurrences = []
            for phrase in phrase_data:
                phrase_occurrences.append({
                    'number_of_times': phrase.number_of_times,
                    'phrase': phrase.phrase,
                    'created_date': phrase.date
                })

        except Exception as ex:
            phrase_occurrences = None
            db.rollback()
            Logger.error(__name__, "get_chart_data_for_minutes", "02", "Exception occurred: {}".format(str(ex)),
                         traceback.format_exc())

        return phrase_occurrences
