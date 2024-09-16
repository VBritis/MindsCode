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
                frames.append((img,img_path))
    
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


def draw_keypoints(frame,results,file_path):
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
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)


def clean_file(folder_path):
    frames = load_frames(folder_path)
    for frame, file_path in frames:
        if "_INVALIDO" in os.path.splitext(file_path)[0]:
            os.remove(file_path)
                
           
            


        
def main(folder_path):
    frames = load_frames(folder_path)
    for frame, file_path in frames:
        results = process_frames(frame)
        draw_keypoints(frame, results, file_path)
            
        cv2.imshow("MediaPipe Hand", frame)
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
  







if __name__ == "__main__":    
    x_input = input("Processar frames: 1 \n Limpar pastas: 2")
    if x_input == "1":
        main("/home/britis/Minds/Sinalizador03/Frames/Sapo_frames/18SapoSinalizador03-2")
    if x_input == "2":    
        clean_file("/home/britis/Minds/Sinalizador03/Frames/Sapo_frames/18SapoSinalizador03-2")




