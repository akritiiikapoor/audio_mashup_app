# audio_mashup_app

A Streamlit-based web app that downloads YouTube videos based on a search query, extracts the audio, trims snippets from each audio file, and combines them into a single mashup. The final mashup is zipped and sent via email. This tool is perfect for creating short audio mashups from multiple sources quickly and efficiently


REQUIREMENTS:

Python: Core programming language.

Streamlit: Framework for creating the web interface.

pydub: Used for audio processing (cutting and merging).

yt-dlp: For downloading YouTube videos and extracting audio.

smtplib: Used for sending the email with the mashup.

FFmpeg: Required for audio conversion and manipulation.

![Screenshot 2024-10-21 044454](https://github.com/user-attachments/assets/9abb624f-7af3-46c2-9e20-7f3cfdb64244)

Features
Search & Download Videos: Enter a search query, and the app downloads the audio from the top YouTube search results.

Create Mashups: Cuts and merges the first few seconds of each downloaded audio file into a single mashup.

Email Integration: Zips the final mashup file and sends it directly to the recipient's email.


![Screenshot 2024-10-21 044441](https://github.com/user-attachments/assets/57089f43-13fd-4a7b-b888-e242b805e8d8)

Download & Convert: The app uses yt-dlp to download the audio from YouTube videos based on the search query. The audio is converted to .mp3 format.

Create Mashup: It then trims the first few seconds (based on user input) from each audio file and merges them into one mashup.

Send Email: The mashup is zipped and sent as an email attachment to the provided email address.

![Screenshot 2024-10-21 044427](https://github.com/user-attachments/assets/e02021c8-2ad6-4d4f-91ab-56a7c86f8695)

![Screenshot 2024-10-21 044524](https://github.com/user-attachments/assets/48f7e86a-f0ea-45aa-bf23-67735fee065c)
