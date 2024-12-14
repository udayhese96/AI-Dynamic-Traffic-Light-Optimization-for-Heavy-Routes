import tkinter as tk
from tkinter import filedialog
import cv2
from ultralytics import YOLO
import numpy as np
from PIL import Image, ImageTk
import threading

# Load YOLOv8 model
model = YOLO("yolov8n.pt")  # Replace with your custom model if needed

# Vehicle classes for car, motorcycle, bus, truck
vehicle_classes = [2, 3, 5, 7]

# Function to count vehicles in a frame
def count_vehicles(frame):
    results = model(frame, conf=0.5)  # Run YOLO on the frame
    vehicle_count = 0
    for result in results:
        boxes = result.boxes  # Bounding boxes
        for box in boxes:
            cls = int(box.cls[0])  # Class index
            if cls in vehicle_classes:
                vehicle_count += 1
    return vehicle_count

# Class to manage video inputs and simulation
class TrafficSimulation:
    def __init__(self, root):
        self.root = root
        self.videos = []
        self.cap = []
        self.gst = []  # Green signal times for each road
        self.video_labels = []
        self.video_threads = []
        self.lock = threading.Lock()

        # Set up the GUI
        self.setup_gui()

    def setup_gui(self):
        self.root.title("Smart Traffic Management System")

        # Header
        label = tk.Label(self.root, text="Welcome to Smart Traffic Management System", font=("Arial", 16))
        label.grid(row=0, column=0, columnspan=2)

        # Button to select 4 videos
        button = tk.Button(self.root, text="Select 4 Videos", command=self.select_videos)
        button.grid(row=1, column=0, columnspan=2)

        # Start simulation button
        start_button = tk.Button(self.root, text="Start Simulation", command=self.start_simulation)
        start_button.grid(row=2, column=0, columnspan=2)

    def select_videos(self):
        """Allows the user to select 4 videos."""
        file_paths = filedialog.askopenfilenames(title="Select 4 Videos", filetypes=[("MP4 Files", "*.mp4")])
        if len(file_paths) == 4:
            self.videos = list(file_paths)
            print("Videos selected:", self.videos)
        else:
            print("Please select exactly 4 videos.")

    def start_simulation(self):
        """Start the traffic simulation after video selection."""
        if len(self.videos) != 4:
            print("Error: Please select 4 videos first.")
            return

        # Initialize video capture for each road
        self.cap = [cv2.VideoCapture(video) for video in self.videos]
        self.gst = [0] * 4  # Placeholder for green signal times

        # Create a window to display the videos in 2x2 grid
        self.video_window = tk.Toplevel(self.root)
        self.video_window.title("Simulation")

        # Create 2x2 grid of labels to display videos
        for i in range(4):
            label = tk.Label(self.video_window)
            label.grid(row=i // 2, column=i % 2)
            self.video_labels.append(label)

        # Start the first loop of the simulation
        self.run_simulation()

    def run_simulation(self):
        """Run the simulation loop."""
        # Get the initial vehicle count at frame 0 for all roads
        vehicle_counts = []
        for i in range(4):
            ret, frame = self.cap[i].read()
            if ret:
                count = count_vehicles(frame)
                vehicle_counts.append(count)
                print(f"Road {i+1} vehicle count at 0th second: {count}")

        # Calculate green signal time for each road
        total_vehicles = sum(vehicle_counts)
        self.gst = [(count / total_vehicles) * 60 for count in vehicle_counts]
        print(f"Green Signal Times: {self.gst}")

        # Sort roads based on GST in descending order
        road_order = sorted(range(4), key=lambda x: self.gst[x], reverse=True)

        # Start playing videos in order of GST
        self.play_videos(road_order)

    def play_videos(self, road_order):
        """Play the videos in the order of green signal times."""
        threads = []
        for i in road_order:
            t = threading.Thread(target=self.play_video, args=(i,))
            t.start()
            threads.append(t)

        # Wait for all threads to finish
        for t in threads:
            t.join()

        # Repeat the process after the loop
        self.run_simulation()

    def play_video(self, i):
        """Play video for a specific road (video) in the 2x2 grid."""
        while True:
            ret, frame = self.cap[i].read()
            if not ret:
                print(f"Road {i+1} video has ended.")
                break

            # Show video and display remaining GST on the video
            gst_text = f"Green Signal: {self.gst[i]:.2f} sec"
            cv2.putText(frame, gst_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Display video in the appropriate window of 2x2 grid
            self.show_video_in_window(frame, i)

            # Wait for the video's GST time to pass
            cv2.imshow(f"Road {i+1}", frame)
            cv2.waitKey(int(self.gst[i] * 1000))  # Wait for GST duration

    def show_video_in_window(self, frame, road_index):
        """Display the video in the appropriate window of 2x2 grid."""
        # Convert the OpenCV frame to a format Tkinter can display
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        img_tk = ImageTk.PhotoImage(img)
        
        # Update the label in the 2x2 grid with the current frame
        self.video_labels[road_index].config(image=img_tk)
        self.video_labels[road_index].image = img_tk  # Keep a reference to the image

if __name__ == "__main__":
    root = tk.Tk()
    sim = TrafficSimulation(root)
    root.mainloop()
