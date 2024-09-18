import cv2
import os
import mediapipe as mp

class PoseMindsd():
    def __init__(self,mode= True,  smooth=True,min_detect=0.5,min_track=0.5):
        self.mode = mode
        self.smooth = smooth
        self.min_detect = min_detect
        self.min_track = min_track
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(self.mode,self.smooth, min_detection_confidence = self.min_detect, min_tracking_confidence = self.min_track)
        self.mp_drawing = mp.solutions.drawing_utils


    def findPose(self, frame, draw=True):
        if len(frame.shape) != 3 or frame.shape[2] != 3:
            raise ValueError("O frame não possui 3 canais. Verifique o formato da imagem.")
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)
        if results.pose_landmarks:
                self.mp_drawing.draw_landmarks(frame, results.pose_landmarks , self.mpPose.POSE_CONNECTIONS)
                for id, lm in enumerate(results.pose_landmarks.landmark):
                    print(id, lm)



        return results
        