import climage
import os
import time
from pathlib import Path


# ffmpeg -i ngyu.mp4 -r 12 -f image2 nggyu/image-%3d.jpeg



def convert_images(folder, width):
    files = [file for file in Path(folder).iterdir() if file.is_file()]
    
    for file in sorted(files):
        # os.mkdir(file.parent / Path("txt_convert"))
        animation_name = file.parent.name
        animations_folder = file.parent.parent.parent
        new_fp_folder = animations_folder / animation_name
        new_fp_folder.mkdir(exist_ok=True)
        new_fp = new_fp_folder / Path(file.name).with_suffix(".txt")
        climage.to_file(file, new_fp, width=width, is_unicode=True)

        new_fp_folder = animations_folder / Path("windows") / animation_name

        new_fp_folder.mkdir(exist_ok=True)
        new_fp = new_fp_folder / Path(file.name).with_suffix(".txt")
        climage.to_file(file, new_fp, width=width, is_unicode=False)
        print(f"Converted {file.name} to {new_fp.name}")



def pad_image(image, height_term):
    image = image.split("\n")
    width_image = len(image[0])
    height_to_add = height_term - len(image)
    height_above = height_to_add // 2
    height_below = height_to_add - height_above
    new_image = [" "*2 for _ in range(height_above)]
    new_image.extend(image)
    new_image.extend([" "*2 for _ in range(height_below)])
    return "\n".join(new_image)


def play_video(folder, fps=12, with_padding=True):

    height_term = os.get_terminal_size().lines


    files = list(Path(folder).iterdir())
    for file in sorted(files):
        image = open(file, "r").read()
        image_padded = image 
        print(image_padded)
        time.sleep(1/fps)


if __name__ == "__main__":
    
    # convert_images("animations/pngs/exit/", 100)
    # convert_images("animations/pngs/big_eyes/", 100)
    # convert_images("animations/pngs/exclamation/", 100)
    # convert_images("animations/pngs/idle/", 100)
    # convert_images("animations/pngs/point_down/", 100)
    # convert_images("animations/pngs/point_left/", 100)
    # convert_images("animations/pngs/read/", 100)
    # convert_images("animations/pngs/sleepy/", 100)
    # convert_images("animations/pngs/scratches/", 100)


    # play_video("clippy_gifs/images/arrival/txt_convert", fps=12)
    