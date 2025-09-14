import psycopg
from config import settings
import os

def checkExistingUser(session):
    print("Checking user in DB: ", session)
    with psycopg.connect(settings.DB_CONNECTION_STRING) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM spotify WHERE spotify.user = %s", (session,))
            res = cur.fetchone()
            print("DB RESPONSE: ", res)
            if res:
                return res
            else:
                return None


def addUser(session, accessToken, refreshToken):
    with psycopg.connect(settings.DB_CONNECTION_STRING) as conn:
        with conn.cursor() as cur:
            uuid = os.urandom(16).hex()
            print("ACCESS TOKEN")
            print(accessToken)
            print("REFRESH TOKEN")
            print(refreshToken)
            cur.execute("INSERT INTO spotify (id, spotify.user, access_token, refresh_token) VALUES (%s, %s, %s, %s)",(uuid, session, accessToken, refreshToken))


def updateAccessToken(session, accessToken):
    with psycopg.connect(settings.DB_CONNECTION_STRING) as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE spotify SET access_token = %s WHERE spotify.user = %s", (accessToken, session))