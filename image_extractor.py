import os
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
            if (not os.path.isdir(self.input_folder)):
                FileService.create_folder(self.input_folder)

        # Find all videos from the input folder
        for file in os.listdir(self.input_folder):
            # First check if the file is supported
            if (not FileService.has_extension(file, ".mp4")):
                print(f"{file} is not a supported type for the extraction, ignoring")
                continue

            # We use the name of the file to create the folder
            destination_folder = os.path.join(self.output_folder, file)

            # If the folder already exists, ignore this video (already processed)
            if (os.path.isdir(destination_folder)):
                print(f"{file} has already been processed, skipping")
                continue

            # The folder is created
            FileService.create_folder(self.output_folder, file)
            # Then the video is processed
            ImageExtractor.Extract(file, destination_folder)

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

class ImageExtractor:

    @staticmethod
    def Extract(video_name, folder):
        """
        Extract the frames from the given video and store them in the given folder
        """
        pass

if __name__ == "__main__":
    Program(INPUT_FOLDER, OUTPUT_FOLDER).main()
