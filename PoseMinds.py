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



def draw_keypoints(frame,results,file_path):
        if results.pose_landmarks:
           #num_axis = len(results.pose_world_landmarks)

            #cv2.putText(frame, f'Numero de pontos: {num_axis}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)


            # Desenhar as landmarks das mãos detectadas
            #if(num_axis != 2):
             #       new_file_name = os.path.splitext(file_path)[0] + "_INVALIDO" + os.path.splitext(file_path)[1]
              #      cv2.putText(frame, f'Numero de maos: {num_hands}, INVALIDO', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            #else:
             #       new_file_name = os.path.splitext(file_path)[0] + "_VALIDO" + os.path.splitext(file_path)[1]
              #      cv2.putText(frame,"Duas maos detectadas, VALIDO", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            #if not (new_file_name == file_path or "_VALIDO" in os.path.splitext(file_path)[0] or "_INVALIDO" in os.path.splitext(file_path)[0]):
             #   os.rename(file_path, new_file_name)
                mpDraw.draw_landmarks(frame, results.pose_landmarks , mpPose.POSE_CONNECTIONS)




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
        draw_keypoints(frame, results, file_path)
            
        cv2.imshow("MediaPipe Hand", frame)
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()




main("/home/britis/Minds/Sinalizador03/Frames/Medo_frames/16MedoSinalizador03-1")