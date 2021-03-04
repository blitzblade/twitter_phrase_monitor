import psycopg2
from psycopg2.extras import RealDictCursor
import sys

def print_err(err):
    print(str(err) + " on line " + str(sys.exc_info()[2].tb_lineno))

class TwitterDb:
    def __init__(self):
        # self.pwd = "postgres"
        self.pwd = "password"
        self.host = "localhost"
        self.conn = psycopg2.connect("dbname=twitter_streamer_db user=postgres password={} host={}".format(self.pwd,self.host))
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)

    def get_cur(self):
        try:
            self.cur.execute("SELECT 1 FROM stream_phrases;")
            return self.cur
        except Exception as ex:
            self.conn = psycopg2.connect("dbname=twitter_streamer_db user=postgres password={} host={}".format(self.pwd,self.host))
            print_err(ex)
            return self.conn.cursor(cursor_factory=RealDictCursor)

    def get_phrases(self):
        self.cur = self.get_cur()
        self.cur.execute("SELECT * FROM stream_phrases;")
        data = self.cur.fetchall()
        return data

    def get_phrase(self, phrase_id):
        self.cur = self.get_cur()
        self.cur.execute("SELECT * FROM stream_phrases WHERE id = %s;", [phrase_id])
        return self.cur.fetchone()

    def create_occurrence(self, phrase_id):
        self.cur = self.get_cur()
        self.cur.execute("INSERT INTO tracking (phrase_id, created_date) VALUES (%s, DATE_TRUNC('minute',CURRENT_TIMESTAMP))",[phrase_id])
        self.conn.commit()

    def get_tracked_phrases(self):
        query = """
        WITH sum_of_minutes AS (SELECT COUNT(created_date) as number_of_times, MAX(created_date) as date, phrase_id FROM tracking
        GROUP BY phrase_id, created_date)
	    select number_of_times, date, phrase, phrase_id FROM sum_of_minutes JOIN stream_phrases ON stream_phrases.id = sum_of_minutes.phrase_id;
        """
        self.cur = self.get_cur()
        self.cur.execute(query)
        return self.cur.fetchall()
    
    def get_average_phrase_per_minute(self):
        query = """
        WITH sum_of_minutes AS (SELECT COUNT(created_date) as number_of_times, MAX(created_date) as date, phrase_id FROM tracking
        GROUP BY phrase_id, created_date)

        SELECT SUM(number_of_times) AS number_of_tweets, COUNT(phrase_id) as number_of_entries, MAX(phrase) as phrase FROM sum_of_minutes 
        JOIN stream_phrases ON stream_phrases.id = sum_of_minutes.phrase_id
        GROUP BY phrase;
        """
        self.cur = self.get_cur()
        self.cur.execute(query)
        return self.cur.fetchall()
    
    def get_average_phrase_per_minute_by_id(self, phrase_id):
        query = """
        WITH sum_of_minutes AS (SELECT COUNT(created_date) as number_of_times, MAX(created_date) as date, phrase_id FROM tracking
        GROUP BY phrase_id, created_date)

        SELECT SUM(number_of_times) AS number_of_tweets, COUNT(phrase_id) as number_of_entries, MAX(phrase) as phrase FROM sum_of_minutes 
        JOIN stream_phrases ON stream_phrases.id = sum_of_minutes.phrase_id where phrase_id = %s
        GROUP BY phrase;
        """
        self.cur = self.get_cur()
        self.cur.execute(query, [phrase_id])
        data = self.cur.fetchone()

        return int(data["number_of_tweets"])/int(data["number_of_entries"])

    def get_chart_data_for_minutes(self):
        query = """
        SELECT COUNT(tracking.created_date) as number_of_times, MAX(tracking.created_date) as date, phrase FROM tracking JOIN 
						stream_phrases ON 
						tracking.phrase_id = stream_phrases.id WHERE tracking.created_date 
						BETWEEN CURRENT_TIMESTAMP - INTERVAL '30 minutes' AND CURRENT_TIMESTAMP
                        GROUP BY phrase, tracking.created_date ORDER BY tracking.created_date asc
        """
        self.cur = self.get_cur()
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_chart_data_by_phrase(self, phrase_id, duration='minute'):
        query = """
        WITH sub_query AS (SELECT date_trunc('{duration}', tracking.created_date) as created_date, phrase FROM tracking JOIN 
        stream_phrases ON 
        tracking.phrase_id = stream_phrases.id where stream_phrases.id = {phrase_id}),

        sub_query2 AS ( SELECT COUNT(created_date) as number_of_times, MAX(created_date) as date, phrase FROM sub_query
            GROUP BY phrase, created_date ORDER BY created_date DESC LIMIT 50)
            
        SELECT * FROM sub_query2 ORDER by date ASC;
        """.format(duration=duration, phrase_id=phrase_id)
        self.cur = self.get_cur()
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_rolling_average(self, phrase_id):
        query = """
        SELECT COUNT(tracking.created_date), phrase FROM tracking JOIN 
						stream_phrases ON 
						tracking.phrase_id = stream_phrases.id WHERE stream_phrases.id = {phrase_id} AND tracking.created_date 
						BETWEEN CURRENT_TIMESTAMP - INTERVAL '30 minutes' AND CURRENT_TIMESTAMP
                        GROUP BY phrase;
        """.format(phrase_id=phrase_id)

        self.cur = self.get_cur()
        self.cur.execute(query)
        total = self.cur.fetchone()
        return int(total["count"])/30 if total else 0
        


