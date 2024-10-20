from pydub import AudioSegment
from pydub.utils import which
AudioSegment.converter = r"C:\ML\project\ffmpeg\bin\ffmpeg.exe"  

import subprocess
import sys
import os
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from yt_dlp import YoutubeDL
import streamlit as st
import imageio

ffmpeg_path = imageio.plugins.ffmpeg.get_exe()
AudioSegment.converter = ffmpeg_path

def install_package(package_name):
    try:
        __import__(package_name)
    except ImportError:
        print(f"Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

def install_ffmpeg():
    try:
        subprocess.check_call(["ffmpeg", "-version"])
        print("FFmpeg is already installed.")
    except FileNotFoundError:
        print("FFmpeg not found. Please install it manually.")

def download_and_convert_videos(search_query, num_videos):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noprogress': False,
            'verbose': True,
        }

        downloaded_files = []
        with YoutubeDL(ydl_opts) as ydl:
            search_results = ydl.extract_info(f"ytsearch{num_videos}:{search_query}", download=False)

            for video in search_results['entries']:
                try:
                    print(f"Downloading: {video['title']}")
                    ydl.download([video['webpage_url']])
                    mp3_file = f"{video['title']}.mp3"
                    downloaded_files.append(mp3_file)
                    if not os.path.exists(mp3_file):
                        print(f"Error: {mp3_file} was not created.")
                    else:
                        print(f"Downloaded and converted {mp3_file}")
                except Exception as download_error:
                    print(f"Failed to download {video['title']}: {download_error}")

        return downloaded_files

    except Exception as e:
        print(f"An error occurred during the video download or conversion: {e}")
        return []

def create_mashup_with_pydub(directory=".", output_file="mashup.mp3", snippet_duration=30 * 1000):
    try:
        audio_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".mp3")]

        if not audio_files:
            print("No .mp3 audio files found in the directory.")
            return

        mashup = AudioSegment.silent(duration=0) 

        for audio_file in audio_files:
            try:
                audio = AudioSegment.from_file(audio_file)
                snippet = audio[:snippet_duration] 
                mashup += snippet
                print(f"Added first {snippet_duration / 1000} seconds of {audio_file} to mashup")
            except Exception as e:
                print(f"Failed to process {audio_file}: {e}")

        if len(mashup) > 0:
            mashup.export(output_file, format="mp3")
            print(f"Mashup created as {output_file}")
        else:
            print("No valid audio clips to create a mashup.")

    except Exception as e:
        print(f"An error occurred during the mashup creation: {e}")

def zip_mashup_file(output_file, zip_filename="mashup.zip"):
    try:
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            zipf.write(output_file)
        print(f"Zipped {output_file} as {zip_filename}")
        return zip_filename
    except Exception as e:
        print(f"Error while zipping the file: {e}")
        return None

def send_email_with_attachment(receiver_email, zip_file):
    try:
        sender_email = "akritiikapoor@gmail.com"  
        sender_password = "ukehlzsfujlmxfgk"      

        subject = "Your Mashup Audio"
        body = "Please find the mashup audio attached."

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEBase('application', 'octet-stream'))

        with open(zip_file, 'rb') as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(zip_file)}')
            msg.attach(part)

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        print(f"Email sent to {receiver_email} with {zip_file} attached.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    st.title("🎶 Audio Mashup Creator")
    col1, col2 = st.columns(2)
    
    with col1:
        search_query = st.text_input("Search videos by name/topic:")
        num_videos = st.number_input("Number of videos to download:", min_value=1, value=1)

    with col2:
        cut_duration = st.number_input("Clip duration to cut (in seconds):", min_value=1, value=30)
        receiver_email = st.text_input("Recipient email address:")

    if st.button("Create Mashup 🎧"):
        if not search_query.strip():
            st.error("Search query cannot be empty!")
            return

        audio_files = download_and_convert_videos(search_query, num_videos)

        if audio_files:
            mashup_file = "mashup.mp3"
            create_mashup_with_pydub(directory=".", output_file=mashup_file, snippet_duration=cut_duration * 1000)
            if not receiver_email or '@' not in receiver_email:
                st.error("Invalid email address!")
                return

            zip_file = zip_mashup_file(mashup_file)

            if zip_file:
                send_email_with_attachment(receiver_email, zip_file)
                st.success(f"Mashup created and sent to {receiver_email}!")
            else:
                st.error("Failed to create the zip file.")
        else:
            st.error("No audio files were downloaded. Please check the search query.")

if __name__ == "__main__":
    install_ffmpeg()  
    main()
