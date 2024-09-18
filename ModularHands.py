import cv2
import os
import mediapipe as mp
import numpy as np






class HandsMind():
    def __init__(self,mode=False, min_conf=0.5,min_track=0.5):
         self.mode = mode
         self.min_conf = min_conf
         self.min_track = min_track
         self.mp_hands = mp.solutions.hands
         self.hands = self.mp_hands.Hands(min_detection_confidence = self.min_conf,min_tracking_confidence = self.min_track)
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



    def process_frames(self,frame):
            if frame is None:
                raise ValueError("O frame está vazio ou não foi carregado corretamente.")
            
            if len(frame.shape) != 3 or frame.shape[2] != 3:
                raise ValueError("O frame não possui 3 canais. Verifique o formato da imagem.")
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            

            return results


    def draw_keypoints(self,frame,results,file_path):
            if results.multi_hand_landmarks:
                num_hands = len(results.multi_hand_landmarks)
                # Desenhar as landmarks das mãos detectadas
                if(num_hands != 2):
                        new_file_name = os.path.splitext(file_path)[0] + "_INVALIDO" + os.path.splitext(file_path)[1]
                        cv2.putText(frame, f'Numero de maos: {num_hands}, INVALIDO', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                else:
                        new_file_name = os.path.splitext(file_path)[0] + "_VALIDO" + os.path.splitext(file_path)[1]
                        cv2.putText(frame,"Duas maos detectadas, VALIDO", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                if not (new_file_name == file_path or "_VALIDO" in os.path.splitext(file_path)[0] or "_INVALIDO" in os.path.splitext(file_path)[0]):
                    os.rename(file_path, new_file_name)

                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)


    def clean_file(self,folder_path):
            frames = self.load_frames(folder_path)
            for frame, file_path in frames:
                if "_INVALIDO" in os.path.splitext(file_path)[0]:
                    os.remove(file_path)
                        
                
                    


            
    def run(self,folder_path):
        frames = self.load_frames(folder_path)
        for frame, file_path in frames:
            results = self.process_frames(frame)
            self.draw_keypoints(frame, results, file_path)
                
            cv2.imshow("MediaPipe Hand", frame)
                
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
    







import time

if __name__ == "__main__":
        path = "/home/britis/Minds/Sinalizador03/Frames/Medo_frames/16MedoSinalizador03-4"
        apk = HandsMind()
        apk.run(path)
        apk.clean_file(path)