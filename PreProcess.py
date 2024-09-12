import cv2
import os



#Process videos function
def process_videos(input_folder, output_folder): 

    #Input_folder and output are the directories that the archives are storaged and the directory that will be storaged


    # Verifica se o diretório de saída existe, cria se não existir no caminho especificado
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)




    video_files = [f for f in os.listdir(input_folder) ]


    # os.listdir(input_folder) lista todos os arquivos e diretórios dentro do diretório especificado por input_folder.

 

    for video_file in video_files:
        video_path = os.path.join(input_folder,video_file)
        video_output_folder =  os.path.join(output_folder,os.path.splitext(video_file)[0])

        if not os.path.exists(video_output_folder):
            os.makedirs(video_output_folder)

        print(f"Processando video: {video_file}")
        extract_frames(video_path, video_output_folder)


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






process_videos("/home/britis/Minds/Sapo","/home/britis/Minds/Sapo_frames")


