import cv2
import mediapipe as mp
import math
import os
import psutil  # To check running processes
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import screen_brightness_control as sbc

# Initialize MediaPipe Hands and drawing utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Pycaw setup for volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# Set default volume and brightness levels
current_volume = 0
volume.SetMasterVolumeLevelScalar(current_volume / 100, None)
current_brightness = 0
sbc.set_brightness(current_brightness)

# Application list
applications = [
    "Notepad", "Calculator", "Paint", "WordPad", "Snipping Tool"
]

# Commands to open applications
app_commands = {
    "Notepad": "notepad.exe",
    "Calculator": "calc.exe",
    "Paint": "mspaint.exe",
    "WordPad": "write.exe",
    "Snipping Tool": "snippingtool.exe"
}

selected_app_index = None
apps_displayed = False
left_hand_in_use = False
right_hand_in_use = False
opened_applications = {}  # To track opened applications and their PIDs

def calculate_distance(p1, p2):
    """Calculate the Euclidean distance between two points."""
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

def draw_bar(frame, level, max_level, bar_pos, color, label):
    """Draw a bar to display the current level of volume or brightness."""
    cv2.rectangle(frame, (bar_pos[0], bar_pos[1]), (bar_pos[0] + 30, bar_pos[1] + 300), (50, 50, 50), -1)
    fill_height = int((level / max_level) * 300)
    cv2.rectangle(frame, (bar_pos[0], bar_pos[1] + 300 - fill_height), (bar_pos[0] + 30, bar_pos[1] + 300), color, -1)
    cv2.putText(frame, f"{int(level)}%", (bar_pos[0] - 20, bar_pos[1] + 320), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    cv2.putText(frame, label, (bar_pos[0] - 20, bar_pos[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

def draw_applications(frame, apps, selected_app):
    """Draw the list of applications on the screen."""
    for i, app in enumerate(apps):
        x = 100
        y = 100 + i * 50
        color = (0, 255, 0) if i == selected_app else (255, 255, 255)
        cv2.rectangle(frame, (x - 10, y - 30), (x + 200, y + 10), (50, 50, 50), -1)  # Background box
        cv2.putText(frame, app, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

def is_fist(hand_landmarks):
    """Check if the hand is in a fist gesture."""
    fingers = [hand_landmarks.landmark[i].y for i in [
        mp_hands.HandLandmark.THUMB_TIP,
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]]
    return all(finger < hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y for finger in fingers)

def is_index_pointing(hand_landmarks, frame_width, frame_height):
    """Check if the index finger is pointing to the application."""
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    x, y = index_tip.x * frame_width, index_tip.y * frame_height
    return x > 100 and x < 300 and y > 100 and y < 300  # Assuming application area is within these coordinates

def is_application_running(app_name):
    """Check if the application is already running."""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == app_name:
            return True
    return False

# Start webcam feed
cap = cv2.VideoCapture(0)

previous_distance_volume = None  # To track changes in distance for volume
previous_distance_brightness = None  # To track changes in distance for brightness

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Flip and process the frame
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        fist_count = 0  # Count fists detected
        left_hand_landmarks = None
        right_hand_landmarks = None

        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Identify left and right hands
            handedness = results.multi_handedness[results.multi_hand_landmarks.index(hand_landmarks)].classification[0].label

            # Get index finger and thumb tip positions
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            if handedness == "Left":
                left_hand_landmarks = hand_landmarks
                # Handle volume control
                if left_hand_in_use == False:
                    distance = calculate_distance(index_tip, thumb_tip)
                    if previous_distance_volume is not None:
                        delta_distance = distance - previous_distance_volume
                        current_volume = max(0, min(100, current_volume + delta_distance * 1000))
                        volume.SetMasterVolumeLevelScalar(current_volume / 100, None)
                    previous_distance_volume = distance
                    left_hand_in_use = True  # Mark the left hand as in use

            elif handedness == "Right":
                right_hand_landmarks = hand_landmarks
                # Handle brightness control
                if right_hand_in_use == False:
                    distance = calculate_distance(index_tip, thumb_tip)
                    if previous_distance_brightness is not None:
                        delta_distance = distance - previous_distance_brightness
                        current_brightness = max(0, min(100, current_brightness + delta_distance * 1000))
                        sbc.set_brightness(current_brightness)
                    previous_distance_brightness = distance
                    right_hand_in_use = True  # Mark the right hand as in use

            # Count the number of fists detected
            if is_fist(hand_landmarks):
                fist_count += 1

        # If both hands are in fist gestures, display applications
        if fist_count == 2 and not apps_displayed:
            apps_displayed = True

        # If not both hands are fists, hide the applications
        if fist_count < 2:
            apps_displayed = False
            left_hand_in_use = False
            right_hand_in_use = False

        if apps_displayed:
            draw_applications(frame, applications, selected_app_index)
            for i, app in enumerate(applications):
                x = 100
                y = 100 + i * 50
                if x - 10 < index_tip.x * frame.shape[1] < x + 200 and y - 30 < index_tip.y * frame.shape[0] < y + 10:
                    selected_app_index = i

                    # Check if left hand is a fist and right hand is pointing at the application
                    if left_hand_in_use and left_hand_landmarks is not None and is_fist(left_hand_landmarks) and right_hand_landmarks is not None and is_index_pointing(right_hand_landmarks, frame.shape[1], frame.shape[0]):
                        app_name = app_commands[applications[selected_app_index]]
                        if not is_application_running(app_name):
                            os.system(app_name)  # Open the selected application
                        apps_displayed = False  # Hide the applications after selection

    # Draw volume and brightness bars only if applications are not displayed
    if not apps_displayed:
        draw_bar(frame, current_volume, 100, (50, 150), (255, 0, 0), "Volume")  # Volume bar
        draw_bar(frame, current_brightness, 100, (frame.shape[1] - 80, 150), (0, 255, 255), "Brightness")  # Brightness bar

    # Display the frame
    cv2.imshow("Gesture-Based Control System", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
hands.close()
