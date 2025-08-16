import cv2
import pyautogui

from HandTrackingModule import HandDetector
from utils import cornerRectangle

# Initialize the hand detector with 1 hand max and high confidence threshold
hand_detector = HandDetector(max_num_hands=1, min_detection_confidence=0.85)

# Open webcam feed and configure resolution & FPS
webcam = cv2.VideoCapture(0)
webcam.set(propId=3, value=1280)  # Width
webcam.set(propId=4, value=720)  # Height
webcam.set(propId=cv2.CAP_PROP_FPS, value=60)  # Frames per second


# --- Button Class ---
class Button:
    """
    Represents a virtual keyboard button.

    Attributes:
        position (tuple): Top-left (x, y) coordinates of the button.
        text (str): Character or symbol displayed on the button.
        size (tuple): Width and height of the button (default = 85x85).
    """

    def __init__(self, position, text, size=(85, 85)):
        self.position = position
        self.text = text
        self.size = size


# --- Utility Function to Draw Buttons ---
def drawAll(buttons_list):
    """
    Draws all virtual buttons on the current frame.

    Args:
        buttons_list (list): List of Button objects.
    """
    for button in buttons_list:
        x1, y1 = button.position
        width, height = button.size

        # Button background
        cv2.rectangle(
            img=frame,
            pt1=(x1, y1),
            pt2=(x1 + width, y1 + height),
            color=(255, 0, 255),
            thickness=cv2.FILLED,
        )

        # Button label
        cv2.putText(
            img=frame,
            text=button.text,
            org=(x1 + 20, y1 + 65),
            fontFace=cv2.FONT_HERSHEY_PLAIN,
            fontScale=4,
            color=(255, 255, 255),
            thickness=4,
        )

        # Stylized corners around the button
        cornerRectangle(
            img=frame,
            pt1=(x1, y1),
            pt2=(x1 + width, y1 + height),
            color=(0, 255, 255),
            corner_length=15,
            corner_thickness=2,
            line_thickness=0,
        )


# --- Virtual Keyboard Layout ---
key_rows = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
]

# Create button objects for each key
buttons_list = []
for y, row in enumerate(key_rows):
    for x, key in enumerate(row):
        button = Button(position=(x * 100 + 150, y * 120 + 20), text=key)
        buttons_list.append(button)

# --- Main Loop ---
while True:
    is_successful, frame = webcam.read()
    if not is_successful:
        break

    # Detect hands in the current frame
    hands = hand_detector.findHands(frame)

    # Draw keyboard buttons
    drawAll(buttons_list)

    if len(hands) > 0:
        hand = hands[0]

        # Measure distance between index fingertip (id=8) and middle fingertip (id=12)
        distance_data = hand_detector.findDistance(
            frame=frame, hand_no1=0, hand_no2=0, id1=8, id2=12, draw=True
        )
        distance = distance_data["distance"]

        # Check if finger hover is within a button area
        for button in buttons_list:
            x1, y1 = button.position
            x2, y2 = x1 + button.size[0], y1 + button.size[1]

            if (
                x1 < distance_data["center x"] < x2
                and y1 < distance_data["center y"] < y2
            ):
                # Highlight hovered button (purple)
                cv2.rectangle(
                    img=frame,
                    pt1=(x1, y1),
                    pt2=(x2, y2),
                    color=(150, 0, 150),
                    thickness=cv2.FILLED,
                )
                cv2.putText(
                    img=frame,
                    text=button.text,
                    org=(x1 + 20, y1 + 65),
                    fontFace=cv2.FONT_HERSHEY_PLAIN,
                    fontScale=4,
                    color=(255, 255, 255),
                    thickness=4,
                )
                cornerRectangle(
                    img=frame,
                    pt1=(x1, y1),
                    pt2=(x2, y2),
                    color=(0, 230, 230),
                    corner_length=15,
                    corner_thickness=2,
                    line_thickness=0,
                )

                # Simulate key press if pinch gesture detected (fingers close)
                if distance < 55:
                    cv2.rectangle(
                        img=frame,
                        pt1=(x1, y1),
                        pt2=(x2, y2),
                        color=(0, 255, 0),
                        thickness=cv2.FILLED,
                    )
                    cv2.putText(
                        img=frame,
                        text=button.text,
                        org=(x1 + 20, y1 + 65),
                        fontFace=cv2.FONT_HERSHEY_PLAIN,
                        fontScale=4,
                        color=(255, 255, 255),
                        thickness=4,
                    )
                    pyautogui.press(keys=button.text, interval=0.2)

    # Display frame
    cv2.imshow(winname="frame", mat=frame)

    # Exit on ESC key
    key = cv2.waitKey(delay=1)
    if key == 27:
        break

# Release resources
webcam.release()
cv2.destroyAllWindows()
