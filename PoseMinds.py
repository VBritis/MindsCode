import cv2
import os
import mediapipe as mp



def load_frames(folder_path):
        frames = []
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                img_path = os.path.join(folder_path,filename)
                img = cv2.imread(img_path)
                if img is not None:
                    frames.append((img,img_path))
        
        if frames:
            print(f"Total frames loaded: {len(frames)}")
        else:
            print("No frames loaded.")
        return frames





mpPose = mp.solutions.pose
pose = mpPose.Pose(static_image_mode = True)
mpDraw = mp.solutions.drawing_utils



def draw_keypoints(frame,results):
        if results.pose_landmarks:
                mpDraw.draw_landmarks(frame, results.pose_landmarks , mpPose.POSE_CONNECTIONS)
                for id, lm in enumerate(results.pose_landmarks.landmark):
                    print(id, lm)




def process_frames(frame):
        if len(frame.shape) != 3 or frame.shape[2] != 3:
            raise ValueError("O frame não possui 3 canais. Verifique o formato da imagem.")
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        return results





def main(folder_path):
    frames = load_frames(folder_path)
    for frame, file_path in frames:
        results = process_frames(frame)
        draw_keypoints(frame, results)
            
        cv2.imshow("MediaPipe Hand", frame)
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()




main("/home/britis/Minds/Sinalizador03/Frames/Sapo_frames/18SapoSinalizador03-4")