import cv2
import os

class load_frames:
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

#Process videos function
def process_videos(input_folder, output_folder): 

    #Input_folder and output are the directories that the archives are storaged and the directory that will be storaged


    # Verify if the output directory exists, create one in input path if not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)



    #Use list comprehension to create a new list for all files of the input_folder
    video_files = [f for f in os.listdir(input_folder) ]


    # os.listdir(input_folder) lista todos os arquivos e diretórios dentro do diretório especificado por input_folder.

 
#Iterate of all files, create the video paths
    for video_file in video_files:
        video_path = os.path.join(input_folder,video_file)
        video_output_folder =  os.path.join(output_folder,os.path.splitext(video_file)[0])

        if not os.path.exists(video_output_folder):
            os.makedirs(video_output_folder)

        print(f"Processando video: {video_file}")
        extract_frames(video_path, video_output_folder)




#Extract the video frames, count is for specify the file name 
def extract_frames(video_path, output_folder):
    cap = cv2.VideoCapture(video_path)

    count = 0

    while True:
        success,frame = cap.read()  

        if not success:
            break

        frame_filename = os.path.join(output_folder, f"frame_{count:04d}.jpg")
        cv2.imwrite(frame_filename, frame)

        count+= 1
    
    cap.release()
    print(f"Total frames extracted from {os.path.basename(video_path)}: {count}")






process_videos("/home/britis/Minds/Sinalizador03/Medo","/home/britis/Minds/Sinalizador03/Frames/Medo_frames")


