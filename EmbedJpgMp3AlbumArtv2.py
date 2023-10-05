import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import eyed3

def embed_album_art():
    root.withdraw()  # Hide the main window

    # Prompt user for image path
    image_path = filedialog.askopenfilename(title="Select an image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not image_path:
        return
    
    # Dynamically detect MIME type
    mime_type = 'image/jpeg' if image_path.lower().endswith(('.jpg', '.jpeg')) else 'image/png'
    
    # Prompt user for audio file paths
    audio_files = filedialog.askopenfilenames(title="Select audio files", filetypes=[("MP3 Files", "*.mp3")])
    if not audio_files:
        return

    try:
        # Add image to audio file(s) as album art
        for audio_file in audio_files:
            audio = eyed3.load(audio_file)
            if audio.tag is None:
                audio.initTag()

            with open(image_path, "rb") as img_file:
                audio.tag.images.set(3, img_file.read(), mime_type)  # 3 means front cover

            audio.tag.save()
        messagebox.showinfo("Success", "Album art embedded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

root = tk.Tk()
embed_album_art()
