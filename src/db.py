import psycopg
from config import settings
import os

def checkExistingUser(session):
    print("Checking user in DB: ", session)
    with psycopg.connect(settings.DB_CONNECTION_STRING) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM spotify WHERE user = %s", (session,))
            return cur.fetchone() is not None


def addUser(session, accessToken, refreshToken):
    with psycopg.connect(settings.DB_CONNECTION_STRING) as conn:
        with conn.cursor() as cur:
            uuid = os.urandom(16).hex()
            cur.execute("INSERT INTO spotify (id, user, access_token, refresh_token) VALUES (%s, %s, %s)",(uuid, session, accessToken, refreshToken))


def updateAccessToken(session, accessToken):
    with psycopg.connect(settings.DB_CONNECTION_STRING) as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE spotify SET access_token = %s WHERE user = %s", (accessToken, session))