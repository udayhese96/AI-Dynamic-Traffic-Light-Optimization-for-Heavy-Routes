# AI-Dynamic-Traffic-Light-Optimization-for-Heavy-Routes

A smart AI-based solution for traffic management on routes with heavy traffic from different directions, featuring **real-time monitoring** and **adaptive traffic light timing** using deep learning and computer vision techniques.

---

## 🚦 Project Overview

This system leverages artificial intelligence to **dynamically optimize traffic light control** at high-traffic intersections. The goal is to reduce congestion, improve traffic flow, and ensure the prioritization of emergency vehicles when detected.

While the full solution includes multiple components, this repository currently **focuses on**:
- Vehicle detection in real-time video
- Retrieving vehicle count and estimating traffic density
- Emergency vehicle detection
- Displaying detection results and vehicle count-based timing

---

## 🎯 Key Features

- ✅ Real-time vehicle detection using **YOLOv10**
- ✅ Classification of emergency vehicles (e.g., ambulance, fire truck)
- ✅ Adaptive signal timing estimation based on vehicle count
- ✅ Support for **manual override by traffic authorities**
- ✅ Real-time processing using **OpenCV** and **FFmpeg**
- ✅ Video processing and analysis with **Scikit-Video**
- ✅ Deep learning integration with **PyTorch/TensorFlow**
- ✅ Flow diagram showing the complete pipeline
- ✅ Sample outputs: images & videos

---

## 🧪 Processed Output Images

<p align="center">
  <img src="processed_cars.png" width="200">
  <img src="processed_test1.jpg" width="200">
  <img src="processed_test2.png" width="200">
  <img src="processed_test3.png" width="200">
  <img src="processed_test4.png" width="200">
</p>

---

## 🎥 Sample Output Videos

- 🔵 Vehicle Detection  
  [![Watch the video](https://img.youtube.com/vi/VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=VIDEO_ID)

- 🔴 Emergency Vehicle Detection  
  <iframe width="934" height="526" src="https://www.youtube.com/embed/_KL2drrePso" title="Emergency" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>(https://youtu.be/_KL2drrePso)

