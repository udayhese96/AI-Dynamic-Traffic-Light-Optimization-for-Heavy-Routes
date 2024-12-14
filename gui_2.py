import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
from ultralytics import YOLO

# Initialize YOLO model
model = YOLO('yolov10l.pt')  # Replace with yolov10 when available

# Define the class ID for vehicle detection (typically, class 2 corresponds to "car" in YOLO)
VEHICLE_CLASSES = [2, 3, 5, 7]  # Class IDs for car, bus, truck, and motorcycle in YOLOv8

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")
        self.image_paths = []
        self.processed_images = []
        self.num_vehicles_per_image = []  # To store the number of vehicles per image

        # Layout
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=10)
        self.grid_frame = tk.Frame(root)
        self.grid_frame.pack(pady=10)
        self.process_button = tk.Button(
            root, text="Process", command=self.process_images, state=tk.DISABLED
        )
        self.process_button.pack(pady=10)

        # Buttons for image input
        for i in range(4):
            btn = tk.Button(
                self.input_frame, text=f"Upload Image {i+1}", command=lambda i=i: self.upload_image(i)
            )
            btn.grid(row=0, column=i, padx=5)

        # Canvas placeholders for images
        self.canvas_size = (300, 300)  # 1.5x of the original size
        self.canvases = [
            tk.Canvas(self.grid_frame, width=self.canvas_size[0], height=self.canvas_size[1], bg="gray")
            for _ in range(4)
        ]
        for i, canvas in enumerate(self.canvases):
            canvas.grid(row=i // 2, column=i % 2, padx=10, pady=10)

    def upload_image(self, index):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        if file_path:
            self.image_paths.append(file_path)
            self.display_image(file_path, self.canvases[index])

        if len(self.image_paths) == 4:
            self.process_button.config(state=tk.NORMAL)

    def display_image(self, path, canvas):
        img = Image.open(path)
        img.thumbnail(self.canvas_size)
        tk_img = ImageTk.PhotoImage(img)
        canvas.image = tk_img
        canvas.create_image(self.canvas_size[0] // 2, self.canvas_size[1] // 2, image=tk_img)

    def process_images(self):
        total_vehicles = 0
        self.num_vehicles_per_image.clear()  # Clear the list before processing

        # First, count the total number of vehicles across all images
        for img_path in self.image_paths:
            num_vehicles, _ = self.detect_vehicles(img_path)  # Get the number of vehicles
            self.num_vehicles_per_image.append(num_vehicles)
            total_vehicles += num_vehicles  # Summing the total number of vehicles

        # Now, calculate the green signal time for each image and display the vehicle count
        for i, num_vehicles in enumerate(self.num_vehicles_per_image):
            print(f"Image {i+1} - Vehicle count: {num_vehicles}")
            green_signal_time = (num_vehicles / total_vehicles) * 60
            print(f"Green signal time for Image {i+1}: {green_signal_time:.2f} seconds")

            # Process and display the image with bounding boxes
            _, processed_img = self.detect_vehicles(self.image_paths[i])
            self.display_image_with_bounding_boxes(processed_img, self.canvases[i])

    def detect_vehicles(self, img_path):
        img = cv2.imread(img_path)
        results = model.predict(img, conf=0.5)
        boxes = results[0].boxes
        class_ids = results[0].boxes.cls  # Get the class IDs for detected objects

        # Filter for vehicle classes (car, bus, truck, motorcycle)
        vehicle_boxes = []
        for box, class_id in zip(boxes, class_ids):
            if class_id.item() in VEHICLE_CLASSES:  # Check if it's a vehicle
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                vehicle_boxes.append((x1, y1, x2, y2))  # Collect bounding box for vehicles

        # Count the number of vehicles detected
        num_vehicles = len(vehicle_boxes)

        # Draw bounding boxes for vehicles only
        for x1, y1, x2, y2 in vehicle_boxes:
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green bounding box for vehicles

        output_path = f"processed_{img_path.split('/')[-1]}"
        cv2.imwrite(output_path, img)  # Save the processed image
        return num_vehicles, img  # Return the number of vehicles and the image with bounding boxes

    def display_image_with_bounding_boxes(self, img, canvas):
        # Convert the processed OpenCV image (BGR) to RGB for display
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_pil.thumbnail(self.canvas_size)
        tk_img = ImageTk.PhotoImage(img_pil)
        canvas.image = tk_img
        canvas.create_image(self.canvas_size[0] // 2, self.canvas_size[1] // 2, image=tk_img)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
