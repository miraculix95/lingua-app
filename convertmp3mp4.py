import os
import subprocess

def convert_mp4_to_mp3(folder_path):
    if not os.path.exists(folder_path):
        print("Der angegebene Ordner existiert nicht.")
        return
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp4"):
            mp4_path = os.path.join(folder_path, filename)
            mp3_path = os.path.join(folder_path, filename.replace(".mp4", ".mp3"))
            
            command = ["ffmpeg", "-i", mp4_path, "-q:a", "0", "-map", "a", mp3_path, "-y"]
            subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"Konvertiert: {filename} -> {os.path.basename(mp3_path)}")

if __name__ == "__main__":
    folder = input("Gib den Pfad zum Ordner ein: ")
    convert_mp4_to_mp3(folder)
