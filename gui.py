import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import second_page  # Import the second page module

# Global variable to store video paths
video_paths = ["", "", "", ""]

# Function to handle file selection
def select_video(index, video_label):
    file_path = filedialog.askopenfilename(
        filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")]
    )
    if file_path:
        video_paths[index] = file_path
        video_label.config(text=f"Selected: {file_path}")

# Function to navigate to the second page
def open_second_page():
    if all(video_paths):
        root.destroy()  # Close the main page
        second_page.display_videos(video_paths)  # Open the second page
    else:
        messagebox.showwarning("Missing Videos", "Please select all four videos.")

# Initialize main window
root = tk.Tk()
root.title("Smart Traffic Management - Home")
root.geometry("600x500")
root.resizable(False, False)

# Styling options
bg_color = "#f0f8ff"  # Light blue background
btn_color = "#4682b4"  # Steel blue buttons
btn_text_color = "white"
heading_font = ("Helvetica", 18, "bold")
label_font = ("Arial", 12)
button_font = ("Arial", 10, "bold")

# Set background color
root.configure(bg=bg_color)

# Heading
heading_label = tk.Label(root, text="Welcome to Smart Traffic Management",
                         font=heading_font, fg="#2e8b57", bg=bg_color)  # Sea green heading
heading_label.pack(pady=20)

# Instruction label
instruction_label = tk.Label(root, text="Please select 4 video files for simulation:",
                             font=label_font, bg=bg_color, fg="black")
instruction_label.pack(pady=10)

# Video selection section
video_frame = tk.Frame(root, bg=bg_color)
video_frame.pack(pady=20)

# Video Input Elements
video_labels = []
for i in range(4):
    # Video label
    video_label = tk.Label(video_frame, text="No video selected", width=40, anchor="w", bg=bg_color)
    video_label.grid(row=i, column=0, padx=10, pady=10)
    # Select button
    video_button = tk.Button(video_frame, text=f"Select Video {i+1}",
                             font=button_font, bg=btn_color, fg=btn_text_color,
                             command=lambda i=i, video_label=video_label: select_video(i, video_label))
    video_button.grid(row=i, column=1, padx=10, pady=10)
    video_labels.append(video_label)

# Next Button
start_button = tk.Button(root, text="Next", font=button_font,
                         bg="green", fg="white", width=15,
                         command=open_second_page)
start_button.pack(pady=30)

# Footer
footer_label = tk.Label(root, text="© 2024 Smart Traffic Management", 
                        font=("Arial", 10), bg=bg_color, fg="gray")
footer_label.pack(side="bottom", pady=10)

# Run the main application
root.mainloop()
