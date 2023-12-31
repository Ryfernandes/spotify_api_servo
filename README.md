# spotify_api_servo
Accesses data from the Spotify API and sends it to Arduino to control a servo motor that shows different images throughout its rotation

The arduino folder houses all of the code that I uploaded to my arduino board, while the system folder has the code that I ran on my computer's command line. This application uses Flask in order to send the user through the authorization process dictated by Spotify. Additionally, I used the code examples on the Spotify API website linked below in order to guide me through writing code to interact with the API. Finally, the code examples were written in javascript and cURL, and used methods I was unfamiliar with, so I used ChatGPT to help understand what the equivalent libraries and methods I would need to use in python would be for interaction with the API.

The physical components of the project consist of a servo motor with a metal shaft and a bearing on the other side to support the weight of the horizontally-hanging shaft. On the shaft is a box that has pictues of artists from different genres on different faces. When the servo rotates, different genres are show. The code here is meant to detect which genre/artist I am listening to on my Spotify account, and then move the servo accordingly to display the right part of the "poster".

Spotify API: https://developer.spotify.com/documentation/web-api
