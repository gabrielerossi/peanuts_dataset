import os
from frameExtractor import FrameExtractor

full_images = "../../data/stripes/"
splitted_images = "../../data/frame/"

def create_dir(dir_name):
    if(not os.path.exists(dir_name)):
        os.makedirs(dir_name)

def main():
    # extract frame from each full illustration
    full_images_paths = [os.path.join(full_images, file) for file in os.listdir(full_images)]
    create_dir(splitted_images)
    splitted_images_directory = splitted_images
    frame_extractor = FrameExtractor()
    splitted_images_paths = frame_extractor.extract_and_save_panels(full_images_paths, splitted_images_directory)

if __name__ == "__main__":
    main()
