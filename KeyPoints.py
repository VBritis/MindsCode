import cv2
import os
import mediapipe as mp
import numpy as np

def load_frames(folder_path):
    frames = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            img_path = os.path.join(folder_path,filename)
            img = cv2.imread(img_path)
            if img is not None:
                frames.append(img)
    
    if frames:
        print(f"Total frames loaded: {len(frames)}")
    else:
        print("No frames loaded.")
    return frames





mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence = 0.7, min_tracking_confidence = 0.5)
mp_drawing = mp.solutions.drawing_utils






def process_frames(frame):
    if frame is None:
        raise ValueError("O frame está vazio ou não foi carregado corretamente.")
    
    if len(frame.shape) != 3 or frame.shape[2] != 3:
        raise ValueError("O frame não possui 3 canais. Verifique o formato da imagem.")
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    return results


def draw_keypoints(frame,results):
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS)





frames = load_frames("/home/britis/Minds/Sinalizador03/Frames/Sapo_frames/18SapoSinalizador03-1")
for frame in frames:
    results = process_frames(frame)
    draw_keypoints(frame,results)

    cv2.imshow("MediaPipe hand", frame)

    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()






