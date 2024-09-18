import cv2
import os
import mediapipe as mp







class HandsMind():
    def __init__(self,mode=True, min_conf=0.5,min_track=0.5):
         self.mode = mode
         self.min_conf = min_conf
         self.min_track = min_track
         self.mp_hands = mp.solutions.hands
         self.hands = self.mp_hands.Hands(self.mode,min_detection_confidence = self.min_conf,min_tracking_confidence = self.min_track)
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



    def findHands(self,frame,file_path, hands, draw = True,):
                if frame is None:
                    raise ValueError("O frame está vazio ou não foi carregado corretamente.")
                
                if len(frame.shape) != 3 or frame.shape[2] != 3:
                    raise ValueError("O frame não possui 3 canais. Verifique o formato da imagem.")
                
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(rgb_frame)

                if results.multi_hand_landmarks:
                    if draw:
                        num_hands = len(results.multi_hand_landmarks)
                        # Desenhar as landmarks das mãos detectadas
                        if(num_hands < hands or num_hands > 2 ):
                                new_file_name = os.path.splitext(file_path)[0] + "_INVALIDO" + os.path.splitext(file_path)[1]
                                cv2.putText(frame, f'Numero de maos{new_file_name}: {num_hands}, INVALIDO', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                        else:
                                new_file_name = os.path.splitext(file_path)[0] + "_VALIDO" + os.path.splitext(file_path)[1]
                                cv2.putText(frame, f'Numero de maos: {num_hands}, VALIDO', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                        if not (new_file_name == file_path or "_VALIDO" in os.path.splitext(file_path)[0] or "_INVALIDO" in os.path.splitext(file_path)[0]):
                            os.rename(file_path, new_file_name)

                        for hand_landmarks in results.multi_hand_landmarks:
                            self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                else:
                        new_file_name = os.path.splitext(file_path)[0] + "_INVALIDO" + os.path.splitext(file_path)[1]
                        if not (new_file_name == file_path or "_VALIDO" in os.path.splitext(file_path)[0] or "_INVALIDO" in os.path.splitext(file_path)[0]):
                            os.rename(file_path, new_file_name)


                    

                return results


            
    def run(self,folder_path, clean = True, hands=2):
        frames = self.load_frames(folder_path)
        for frame, file_path in frames:
            self.findHands(frame,file_path,hands)
            if clean:
                if "_INVALIDO" in os.path.splitext(file_path)[0]:
                    os.remove(file_path)
                
            cv2.imshow("MediaPipe Hand", frame)
                
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
    







import time

if __name__ == "__main__":
        path = "/home/britis/Minds/Sinalizador03/Frames/Sapo_frames/18SapoSinalizador03-4"
        apk = HandsMind()
        apk.run(path,clean=True,hands=2)