import mediapipe as mp
import cv2
import os




class FaceMinds:
    def __init__(self,max_num_faces):
        self.mpFaceDetect = mp.solutions.face_detection
        self.FaceDetect = self.mpFaceDetect.FaceDetection()
        self.mpFaceMesh = mp.solutions.face_mesh()
        self.FaceMesh = self.mpFaceMesh.FaceMesh(max_num_faces)
        self.mpDraw = mp.solutions.drawing_utils
        



    def process_frames(self,frame,file_path):
        if len(frame.shape) != 3 or frame.shape[2] != 3:
            raise ValueError("O frame não possui 3 canais. Verifique o formato da imagem.")
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.faceMesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for faceFig in results.multi_face_landmarks:
                self.mpDraw.draw_landmarks(frame,faceFig,self.mpFaceMesh.FACEMESH_FACE_OVAL)
        
        else:
            
            new_file_name = os.path.splitext(file_path)[0] + "_INVALIDO" + os.path.splitext(file_path)[1]
            if not (new_file_name == file_path or "_INVALIDO" in os.path.splitext(file_path)[0]):
                os.rename(file_path, new_file_name)


        return frame  # Retorna o quadro processado
