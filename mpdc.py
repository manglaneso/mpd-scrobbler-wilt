#!/usr/bin/python
import mpd
import os
import json
import requests
from time import sleep

Auth = 'https://modal.moe/api/api-token-auth/'
Scrobble = 'https://modal.moe/api/scrobbles/'

post = requests.post
get = requests.get


class Wilt:

    def __init__(self):
        self.user = input('Username: ')
        self.password = input('Password: ')
        self.mpd_location = input('mpd IP: ')
        self.mpd_port = input('mpd port: ')
        #self.mpd_pass = input('mpd pass: ') # Uncomment if you have a password protecting mpd 
        self.logged_in = False
        self.header = {'Authorization': 'Token {}'.format(self.login())}
        self.last_played = ''  # Clarity

    def login(self):
        r = post(Auth, data={'username': self.user, 'password': self.password})
        if 'token' in r.text:
            self.logged_in = True
            os.system('clear')
        else:
            print('Something went wrong - Not logged in!')
            return None
        return json.loads(r.text)['token']

    def scrobble(self, scrobble):
        if scrobble['song'] != self.last_played:
            print("Now Playing:", scrobble['song'], "-", scrobble['artist'])
            r = post(Scrobble, data=scrobble, headers=self.header)
            self.last_played = scrobble['song']
        else:
            return None

Wilt = Wilt()

def query_mpd():
    try:
        client = mpd.MPDClient(use_unicode=True)
        client.connect(Wilt.mpd_location, Wilt.mpd_port) # Change for the IP you run mpd on
        #client.password(Wilt.mpd_pass) # Set if you have a password protecting mpd 
        currsong = client.currentsong()
        song = currsong['title']
        artist = currsong['artist']
        #album = currsong['album']
        Wilt.scrobble({'song': song, 'artist': artist})
    except Exception as detail:
        print('Non fatal exception. Query failed:', detail)

if __name__ == '__main__':
    while 1:
        query_mpd()
sleep(25)
