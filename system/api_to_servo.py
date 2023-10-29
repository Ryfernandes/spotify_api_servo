import serial
import requests
import base64

from flask import Flask, redirect, request
import urllib.parse
import string
import random

CURRENTLY_PLAYING_URL = 'https://api.spotify.com/v1/me/player/currently-playing?market=US'
ID = "MY_ID"
SECRET = "MY_SECRET"
REDIRECT = "http://localhost:8888/callback"

ARDUINO_CONNECTION = serial.Serial(port = "COM3", baudrate = 115200, timeout = 0.1)

HIP_HOP_PLAYLIST = ["Drake", "Kendrick Lamar", "Dr. Dre", "Travis Scott", "Young Thug", "Don Toliver", "Quavo", "Offset", "Chief Keef", "Swae Lee", "The Weeknd", "Playboi Carti", "21 Savage", "Future", "Pop Smoke", "Lil Uzi Vert", "Kid Cudi", "Anime", "XXXTENTACION", "Joey Bada$$", "Jack Harlow", "Big Sean", "J. Cole", "JID", "A$AP Rocky", "Lil Wayne", "JAY-Z", "Migos", "Frank Ocean", "Polo G", "Mac Miller", "Wiz Khalifa", "Denzel Curry", "Childish Gambino", "Pusha T", "Chance the Rapper", "Lil Baby", "Metro Boomin", "MAVI", "Smino", "Tory Lanez", "KayCyy", "Vince Staples", "Miguel", "50 Cent", "The Notorious B.I.G."]

awaitToken = False
token = ""

def write(degrees):
    ARDUINO_CONNECTION.write(bytes(str(degrees), "utf-8"))

def currentArtist(inputToken):
    headers = {"Authorization": "Bearer " + inputToken}
    
    response = requests.get(CURRENTLY_PLAYING_URL, headers = headers)
    try:
        jsonResponse = response.json()
    except Exception as error:
        print("Error with request:", error)
        return []
    else:
        try:
            artists = [artist for artist in jsonResponse['item']['artists']]
            artistNames = ([artist['name'] for artist in artists])
        except:
            artistNames = []
            print(jsonResponse)
            print("Error with json data (request sucessful)")

        return artistNames

def randomString(length):
    characters = string.ascii_letters + string.digits
    randomChars = []
    
    for x in range(length):
        randomChars.append(random.choice(characters))

    randomStr = "".join(randomChars)
    print(randomStr)

    return randomStr

app = Flask(__name__)

@app.route("/login")
def login():
    state = randomString(16)
    scope = "user-read-private user-read-email user-read-currently-playing"

    authorizationURL = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode({
        "response_type": "code",
        "client_id": ID,
        "scope": scope,
        "redirect_uri": REDIRECT,
        "state": state
    })

    return redirect(authorizationURL)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    state = request.args.get("state")

    if state is None:
        return redirect('/#' + urllib.parse.urlencode({'error': 'state_mismatch'}))
    else:
        idSecret = f"{ID}:{SECRET}"
        idSecretEncoded = idSecret.encode("utf-8")
        base64AuthEncoded = base64.b64encode(idSecretEncoded)
        base64Auth = base64AuthEncoded.decode("utf-8")

        url = "https://accounts.spotify.com/api/token"

        headers = {"content-type": "application/x-www-form-urlencoded", 
                "Authorization": "Basic " + str(base64Auth), "Content-Type": "application/x-www-form-urlencoded"}
        
        data = {"code": code,
                "redirect_uri": REDIRECT,
                "grant_type": "authorization_code"}

        response = requests.post(url, headers = headers, data = data)

        try:
            jsonResponse = response.json()
        except Exception as error:
            print("Error with token request:", error)
        else:
            try:
                newToken = jsonResponse["access_token"]
                print(newToken)
            except:
                print(jsonResponse)
                print("Error with json token data (request sucessful)")

        global token
        token = newToken
        global awaitToken
        awaitToken = False
        return "Successful Authorization"

def newAuthorizationCode():
    awaitToken = True
    app.run(port = 8888)

newAuthorizationCode()

currentMsg = 0
write(currentMsg)
lastMsg = currentMsg

while True:
    if not awaitToken:
        artists = currentArtist(token)
        if len(artists) != 0:
            if "Justin Bieber" in artists:
                currentMsg = 90
            elif bool(set(HIP_HOP_PLAYLIST) & set(artists)):
                currentMsg = 0
            else:
                currentMsg = 180

            if currentMsg != lastMsg:
                write(currentMsg)
                lastMsg = currentMsg
                print(lastMsg)
    else:
        print("uh oh")
