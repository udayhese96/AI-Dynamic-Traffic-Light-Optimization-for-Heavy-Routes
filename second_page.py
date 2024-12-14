import tkinter as tk
from PIL import Image, ImageTk
import cv2
from ultralytics import YOLO
import time

# Load YOLOv10n model
model = YOLO('yolov10n.pt')

# Vehicle class names for filtering
vehicle_classes = ["car", "bus", "truck", "motorcycle"]

def detect_vehicles_yolov10n(frame):
    results = model(frame, conf=0.5)  # Perform detection with confidence threshold
    detections = results[0]

    # Count vehicles based on vehicle classes
    vehicle_count = 0
    for box in detections.boxes:
        cls_id = int(box.cls)
        if model.names[cls_id] in vehicle_classes:
            vehicle_count += 1

    return vehicle_count

def calculate_green_signal_time(vehicle_count, total_vehicles):
    return min((vehicle_count / total_vehicles) * 12, vehicle_count * 2)

def play_video_segment(cap, label, green_signal_time, paused_frame=None):
    """
    Play a segment of the video for the specified green_signal_time in seconds.
    Resumes from paused_frame if provided.
    """
    # If there was a pause, start from the last paused frame
    if paused_frame is not None:
        cap.set(cv2.CAP_PROP_POS_FRAMES, paused_frame)

    fps = cap.get(cv2.CAP_PROP_FPS)
    frames_to_play = int(green_signal_time * fps)  # Calculate frames for green_signal_time seconds
    frame_count = 0

    # Ensure the first frame is fetched and displayed correctly
    ret, frame = cap.read()
    if not ret:
        return None  # Video has ended, cannot play

    # Convert and resize the first frame to RGB for display
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (500, 300))  # Resize for display
    img = ImageTk.PhotoImage(Image.fromarray(frame))

    # Set the label with the first frame
    label.imgtk = img
    label.configure(image=img)
    label.update()  # Ensure the frame is displayed immediately

    # Start the countdown timer
    start_time = time.time()

    while frame_count < frames_to_play:
        ret, frame = cap.read()
        if not ret:
            return None  # Video has ended

        # Calculate remaining green signal time
        remaining_time = max(0, green_signal_time - (time.time() - start_time))
        overlay_text = f"Green Signal: {int(remaining_time)} seconds"
        cv2.putText(frame, overlay_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0, 255, 0), 2, cv2.LINE_AA)

        # Convert BGR to RGB for display
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (500, 300))  # Resize for display

        # Update image for label
        img = ImageTk.PhotoImage(Image.fromarray(frame))

        # Update label with the new image
        label.imgtk = img
        label.configure(image=img)
        label.update()  # Ensure the frame is updated immediately

        frame_count += 1
        time.sleep(1 / fps)  # Wait for the duration of one frame

    # Return the last frame to pause on
    return cap.get(cv2.CAP_PROP_POS_FRAMES)



def display_videos(video_paths):
    second_root = tk.Tk()
    second_root.title("Smart Traffic Management - Simulation")
    second_root.geometry("1100x800")
    second_root.resizable(False, False)

    heading_label = tk.Label(second_root, text="Simulation: Traffic Videos",
                             font=("Arial", 20, "bold"), fg="blue")
    heading_label.pack(pady=20)

    video_frame = tk.Frame(second_root)
    video_frame.pack(pady=10)

    video_labels = []
    caps = []
    last_frames = [0, 0, 0, 0]  # Last frame for each video to start the next loop
    total_vehicles = 0  # Total vehicle count placeholder; adjust if needed

    # Initialize video captures and labels
    for i, video_path in enumerate(video_paths):
        video_label = tk.Label(video_frame, width=500, height=300, bg="black")
        video_label.grid(row=i // 2, column=i % 2, padx=20, pady=20)
        video_labels.append(video_label)

        cap = cv2.VideoCapture(video_path)
        caps.append(cap)

        # Detect vehicles in the first frame of each video
        ret, frame = cap.read()
        if ret:
            vehicle_count = detect_vehicles_yolov10n(frame)
            total_vehicles += vehicle_count  # Sum of detected vehicles across all videos
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset to the start

    # Loop until all videos have ended
    while any(cap.isOpened() for cap in caps):
        green_signal_times = []  # Store green signal times for this loop
        for i, cap in enumerate(caps):
            if not cap.isOpened():
                green_signal_times.append(0)  # Skip ended videos
                continue

            # Start from last paused frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, last_frames[i])
            ret, frame = cap.read()
            if not ret:
                cap.release()
                green_signal_times.append(0)
                continue

            # Calculate green signal time based on the detected vehicles
            vehicle_count = detect_vehicles_yolov10n(frame)
            green_signal_time = calculate_green_signal_time(vehicle_count, total_vehicles)
            green_signal_times.append(green_signal_time)

            print(f"Video {i+1}: Vehicle Count = {vehicle_count}, Green Signal Time = {green_signal_time} seconds")

        # Play each video for its green signal time
        for i, (cap, green_signal_time) in enumerate(zip(caps, green_signal_times)):
            if cap.isOpened() and green_signal_time > 0:
                last_frames[i] = play_video_segment(cap, video_labels[i], green_signal_time, last_frames[i])
                if last_frames[i] is None:
                    cap.release()  # Close video if it has ended

    # Exit button to close the Tkinter window
    exit_button = tk.Button(second_root, text="Exit", font=("Arial", 14, "bold"),
                            bg="red", fg="white", command=second_root.destroy)
    exit_button.pack(pady=20)

    second_root.mainloop()
