import psycopg
from config import settings
import os
from utils.hash import hashToken

def checkSpotifyExistingUser(session):
    with psycopg.connect(settings.DB_CONNECTION_STRING) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM spotify WHERE session = %s", (session,))
            res = cur.fetchone()
            if res:
                return res
            else:
                return None


def addSpotifyUser(session, accessToken, refreshToken):
    with psycopg.connect(settings.DB_CONNECTION_STRING) as conn:
        with conn.cursor() as cur:
            uuid = os.urandom(16).hex()
            cur.execute("INSERT INTO spotify (id, session, access_token, refresh_token) VALUES (%s, %s, %s, %s)",(uuid, session, hashToken(accessToken), hashToken(refreshToken)))


def updateSpotifyAccessToken(session, accessToken):
    with psycopg.connect(settings.DB_CONNECTION_STRING) as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE spotify SET access_token = %s WHERE session = %s", (hashToken(accessToken), session))


def checkLetterboxExistingUser(session):
    with psycopg.connect(settings.DB_CONNECTION_STRING) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM letterbox WHERE session = %s", (session,))
            res = cur.fetchone()
            if res:
                return res
            else:
                return None


def addLetterboxUser(session, accessToken, refreshToken):
    with psycopg.connect(settings.DB_CONNECTION_STRING) as conn:
        with conn.cursor() as cur:
            uuid = os.urandom(16).hex()
            cur.execute("INSERT INTO letterbox (id, session, access_token, refresh_token) VALUES (%s, %s, %s, %s)",(uuid, session, hashToken(accessToken), hashToken(refreshToken)))


def updateLetterboxAccessToken(session, accessToken):
    with psycopg.connect(settings.DB_CONNECTION_STRING) as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE letterbox SET access_token = %s WHERE session = %s", (hashToken(accessToken), session))