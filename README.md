# SmartWave

**Project Overview: SmartWave - Gesture-Based Control System**

**Introduction:**
SmartWave is an innovative gesture-based control system that enables users to interact with their devices without physical touch. By leveraging hand gestures captured through a webcam, the system allows control of essential features like volume, brightness, and the launching of applications. The system utilizes advanced computer vision techniques to detect and interpret hand movements, making it a cutting-edge, hands-free solution for managing digital environments.

**Key Features:**

1. **Gesture Recognition:**
   - The system uses **MediaPipe Hands** to detect and track hand landmarks in real-time.
   - Hand gestures are mapped to control actions, such as volume adjustment, brightness control, and launching applications.

2. **Volume Control:**
   - Users can control the system's volume by performing a specific gesture with their left hand. The system measures the distance between the index finger and thumb to adjust the volume in real-time.
   - The system provides a visual representation of the volume level on the screen, allowing users to see changes as they make adjustments.
![Screenshot 2025-01-03 193330](https://github.com/user-attachments/assets/b1df4c2f-6807-4e5f-8f86-69e6e828b070)

3. **Brightness Control:**
   - Similarly, the system uses the right hand's gestures to adjust the screen's brightness.
   - The same distance-based gesture mechanism is applied to the right hand for seamless control of screen brightness.
![Screenshot 2025-01-03 193249](https://github.com/user-attachments/assets/9482fc90-1d5d-41a4-ba3c-c4f7a17fad96)

4. **Application Launching:**
   - The system can detect when the user is pointing at an application (like Notepad, Calculator, or Paint) using their index finger.
   - When the user performs a "fist" gesture with the left hand and points to an application with the right hand, the corresponding application is launched automatically.
   - A list of applications is displayed on the screen, and the user can select an application by pointing at it, followed by a gesture to open it.
![Screenshot 2025-01-03 193522](https://github.com/user-attachments/assets/cd87712d-b255-4d5c-9f1e-1d1af6683d9c)

5. **Dynamic Interface:**
   - The system provides a dynamic user interface that updates in real-time based on user gestures.
   - Volume and brightness levels are visually represented by bars on the screen, with changes reflected immediately as the user adjusts them.

6. **Multi-Hand Support:**
   - The system supports multi-hand detection, enabling the user to control different functions simultaneously using both hands.
   - The left hand controls volume, while the right hand handles brightness adjustments, with both hands being used to select and launch applications.

7. **Application Management:**
   - The system keeps track of running applications, ensuring that applications are only launched if they are not already open, preventing duplicates.
   - The process of opening and closing applications is handled through the **os.system** function, which launches applications by executing their respective executable files.

8. **Real-Time Feedback:**
   - The system provides real-time feedback by updating the user interface with the current volume and brightness levels.
   - The application list is shown dynamically based on hand gestures, making it intuitive and easy to interact with the system.

**Technology Stack:**

- **Computer Vision:** 
   - **MediaPipe Hands** for hand tracking and gesture recognition.
   - **OpenCV** for video processing and display.
   
- **Audio Control:**
   - **Pycaw** for controlling system volume via the `IAudioEndpointVolume` interface.
   
- **Screen Brightness Control:**
   - **screen_brightness_control** for adjusting the screen brightness programmatically.

- **Operating System Integration:**
   - **psutil** to check running processes and avoid opening duplicate applications.
   - **os.system** to launch applications.

**User Experience:**

SmartWave provides a user-friendly, intuitive interface where gestures are the primary means of interaction. The system responds instantly to hand movements, providing a seamless experience for controlling system functions like volume, brightness, and application management. The inclusion of real-time feedback and the ability to manage multiple functions simultaneously makes it a powerful tool for hands-free device control.

**Conclusion:**

SmartWave is a versatile, hands-free control system that leverages advanced computer vision and gesture recognition technologies to offer an intuitive, user-friendly experience. Whether for accessibility, convenience, or innovation, SmartWave transforms the way users interact with their devices, making it an exciting addition to the realm of gesture-based interfaces.
