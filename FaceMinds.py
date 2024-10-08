import cv2
import mediapipe as mp
import os


mpFaceDetection = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils
faceDetection = mpFaceDetection.FaceDetection()

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










def process_frames(frame,file_path):
    if len(frame.shape) != 3 or frame.shape[2] != 3:
        raise ValueError("O frame não possui 3 canais. Verifique o formato da imagem.")
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = faceDetection.process(rgb_frame)

    if results.detections:
        for detection in results.detections:
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = frame.shape
            bbox = (int(bboxC.xmin * iw), int(bboxC.ymin * ih),
                    int(bboxC.width * iw), int(bboxC.height * ih))
            cv2.rectangle(frame, bbox, (255, 0, 255), 2)
    else:
        
        new_file_name = os.path.splitext(file_path)[0] + "_INVALIDO" + os.path.splitext(file_path)[1]
        if not (new_file_name == file_path or "_INVALIDO" in os.path.splitext(file_path)[0]):
            os.rename(file_path, new_file_name)


    return frame  # Retorna o quadro processado






def main(folder_path):
    frames = load_frames(folder_path)
    for frame, file_path in frames:
        processed = process_frames(frame,file_path)
            
        cv2.imshow("MediaPipe Hand", processed)
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()




main("/home/britis/Minds/Sinalizador03/Frames/Medo_frames/16MedoSinalizador03-2")

