import cv2
import mediapipe as mp
import math

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

def calculate_angle(a, b, c):
    """
    Calculates the angle at point 'b' formed by the lines 'a-b' and 'b-c'.
    a, b, c are landmarks with x and y attributes.
    """
    # calculate vectors
    ab = [a.x - b.x, a.y - b.y]
    bc = [c.x - b.x, c.y - b.y]
    
    dot_product = ab[0] * bc[0] + ab[1] * bc[1]
    magnitude_ab = math.sqrt(ab[0]**2 + ab[1]**2)
    magnitude_bc = math.sqrt(bc[0]**2 + bc[1]**2)
    
    angle_radians = math.acos(dot_product / (magnitude_ab * magnitude_bc))
    
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to RGB for MediaPipe processing
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(frame_rgb)

    if result.pose_landmarks:
        # Draw pose landmarks
        mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        # Get landmarks
        landmarks = result.pose_landmarks.landmark

        # Indices for relevant landmarks
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
        
        # Calculate elbow angle
        elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
        
        # Display the angle on the screen
        cv2.putText(frame, f'Elbow Angle: {int(elbow_angle)}',
                    (int(right_elbow.x * frame.shape[1]), int(right_elbow.y * frame.shape[0] - 20)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the frame
    cv2.imshow('Pose Estimation with Angles', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
