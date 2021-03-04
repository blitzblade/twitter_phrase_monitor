import os
db = "postgres://postgres:postgres@localhost/twitter_streamer_db"
# db = "postgres://postgres:baw48KdcN6yRQ37yVEWjuehtx@localhost/twitter_streamer_db"

os.environ["DATABASE_URL"] = db
print("Database Url")
