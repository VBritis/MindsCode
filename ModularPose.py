import cv2
import os
import mediapipe as mp


class PoseMinds():
    def __init__(self,mode= True,  smooth=True,min_detect=0.5,min_track=0.5):
        self.mode = mode
        self.smooth = smooth
        self.min_detect = min_detect
        self.min_track = min_track
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(self.mode,self.smooth, min_detection_confidence = self.min_detect, min_tracking_confidence = self.min_track)
        self.mp_drawing = mp.solutions.drawing_utils


    def load_frames(self,folder_path):
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


    def findPose(self, frame, draw=True):
        if len(frame.shape) != 3 or frame.shape[2] != 3:
            raise ValueError("O frame não possui 3 canais. Verifique o formato da imagem.")
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)
        if results.pose_landmarks:
                self.mp_drawing.draw_landmarks(frame, results.pose_landmarks , self.mp_pose.POSE_CONNECTIONS)
                for id, lm in enumerate(results.pose_landmarks.landmark):
                    print(id, lm)

        return results
        
    def run(self,folder_path, clean = False):
        frames = self.load_frames(folder_path)
        for frame, file_path in frames:
            self.findPose(frame,file_path)
            if clean:
                if "_INVALIDO" in os.path.splitext(file_path)[0]:
                    os.remove(file_path)
                
            cv2.imshow("MediaPipe Hand", frame)
                
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()


if __name__ == "__main__":
    pose = PoseMinds()
    pose.run("/home/britis/Minds/Sinalizador03/Frames/Sapo_frames/18SapoSinalizador03-2")
