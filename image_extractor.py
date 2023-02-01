import os
import shutil
import time
import cv2

INPUT_FOLDER = "Inputs"
OUTPUT_FOLDER = "Outputs"

class Program:

    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder

    def main(self):

        start_time = time.time()
        processed = 0
        skipped = 0

        # Create the folders if they don't already exists
        for folder in (self.input_folder, self.output_folder):
            if (not os.path.isdir(folder)):
                # Create the folder inside the current working directory
                FileService.create_folder(os.getcwd(), folder)

        # Find all videos from the input folder
        for file in os.listdir(self.input_folder):
            filename, extension = os.path.splitext(file)

            # First check if the file is supported
            if (not extension in (".mp4")):
                print(f"{file} is not a supported type for the extraction, ignoring")
                continue

            # We use the name of the file to create the folder
            destination_folder = os.path.join(self.output_folder, filename)

            # If the folder already exists, ignore this video (already processed)
            if (os.path.isdir(destination_folder)):
                skipped += 1
                print(f"{file} has already been processed, skipping")
                continue

            # The folder is created
            FileService.create_folder(self.output_folder, filename)
            # Then the video is processed
            try:
                ImageExtractor.Extract(os.path.join(self.input_folder, file), filename, destination_folder)
            except Exception as excpetion:
                # Couldn't extract the video
                print(f"{filename}: {excpetion}, skipping")
                FileService.delete_folder(os.path.join(self.output_folder, filename))
                skipped += 1
            else:
                # Extraction went well
                processed += 1

        # End of the program
        print(f"Program exited successfully: {processed} processed, {skipped} skipped in {time.time() - start_time}s")

class FileService:

    @staticmethod
    def has_extension(file, *extensions):
        for extension in extensions:
            if (file.endswith(extension)):
                return True
        return False

    @staticmethod
    def create_folder(folder_path, folder_name):
        os.mkdir(f"{folder_path}\{folder_name}")

    @staticmethod
    def delete_folder(folder_path):
        shutil.rmtree(folder_path, ignore_errors=True)

class ImageExtractor:

    @staticmethod
    def Extract(video_path, video_name, output_folder):
        """
        Extract the frames from the given video and store them in the given folder
        """
        # Open the video
        video = cv2.VideoCapture(video_path)
        # Check if the video has been opened correctly
        if not video.isOpened():
            raise Exception("An error as occured when trying to open the video")
        # Get the number of frames and the framerate of the video
        frame_number = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = video.get(cv2.CAP_PROP_FPS)
        # Convert all frames into an image
        for i in range(frame_number):
            success, frame = video.read()
            cv2.imwrite(os.path.join(output_folder, f"{video_name}_{i:0<5}.jpg"), frame)

if __name__ == "__main__":
    Program(INPUT_FOLDER, OUTPUT_FOLDER).main()
