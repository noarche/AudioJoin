import os
from pydub import AudioSegment
import eyed3
import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox

def select_audio_files():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(title="Select audio files to join",
                                             filetypes=[('Audio Files', '*.mp3;*.m4a')])
    return file_paths

def confirm_files_order(file_paths):
    file_names = [os.path.basename(path) for path in file_paths]
    message = "Files will be joined in the following order:\n\n"
    message += "\n".join(file_names)
    return messagebox.askyesno("Confirm Order", message)

def gather_metadata():
    root = tk.Tk()
    root.title("Enter Metadata")

    tk.Label(root, text="Artist:").grid(row=0, column=0, sticky='w', padx=10, pady=5)
    artist_entry = tk.Entry(root)
    artist_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Album:").grid(row=1, column=0, sticky='w', padx=10, pady=5)
    album_entry = tk.Entry(root)
    album_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Track Number:").grid(row=2, column=0, sticky='w', padx=10, pady=5)
    track_num_entry = tk.Entry(root)
    track_num_entry.grid(row=2, column=1, padx=10, pady=5)


    metadata = {}

    def on_ok():
        metadata["artist"] = artist_entry.get()
        metadata["album"] = album_entry.get()
        metadata["track_num"] = track_num_entry.get()
        root.quit()  # This line breaks out of the tkinter main loop

    ok_button = tk.Button(root, text="OK", command=on_ok)
    ok_button.grid(row=4, column=0, columnspan=2, pady=10)

    root.mainloop()
    root.destroy()  # Now we destroy the root window after the main loop
    
    return metadata


def join_audio_files(file_paths, output_file_name, bitrate, metadata):
    combined_audio = None

    for audio_file in file_paths:
        if audio_file.endswith('.mp3'):
            audio = AudioSegment.from_mp3(audio_file)
        elif audio_file.endswith('.m4a'):
            audio = AudioSegment.from_file(audio_file, format="m4a")

        if combined_audio is None:
            combined_audio = audio
        else:
            combined_audio += audio
    
    combined_audio.export(output_file_name, format="mp3", bitrate=bitrate)

    audio_file = eyed3.load(output_file_name)
    audio_file.tag.artist = metadata["artist"]
    audio_file.tag.album = metadata["album"]
    audio_file.tag.track_num = int(metadata["track_num"])

    audio_file.tag.save()

if __name__ == "__main__":
    file_paths = select_audio_files()

    if not file_paths:
        print("No files selected. Exiting.")
        exit()

    if not confirm_files_order(file_paths):
        print("Order not confirmed. Exiting.")
        exit()

    metadata = gather_metadata()
    

initial_file_name = f"{metadata['album']} by {metadata['artist']}.mp3"
output_file_name = simpledialog.askstring("Input", "Name your output file:", initialvalue=initial_file_name)
if not output_file_name.endswith('.mp3'):
    output_file_name += ".mp3"


    bitrate = "64k"  # Default to 64kbps

    join_audio_files(file_paths, output_file_name, bitrate, metadata)
    print(f"Combined audio saved to {output_file_name}")
