from pathlib import Path
import numpy as np
import cv2
import sys
import os
import shutil

# data set input info
DATASET_NAME = 'Furniture_set_500'
BACKGROUND_DIR = 'd:/Unity/Furniture_synth/Furniture_data/Backgraunds'
OBJECT_DIR = 'D:/Unity/Furniture_synth/3d_fur_500'
OUTPUT_DIR = 'D:/Unity/Furniture_synth/Data_sets'
OBJECT_NAMES = ['chair', 'sofa', 'table', 'cabinet', 'desk', 'lamp', 'fruits']
NUM_IMAGE = 4500
VAL_PERSENT = 1 # percentage of images selected for validation
TEST_PERSENT = 0 # percentage of images selected for test

backgrounddir = Path(BACKGROUND_DIR)
targetdir = Path(OBJECT_DIR)
if OUTPUT_DIR[-1] != '/': OUTPUT_DIR = OUTPUT_DIR + '/'

#class number and name for incorrect image names
OBJECT_NAMES.append('ghost')

#generate data_set folders
def generate_folders(root_path, folder_list):
    os.chdir(root_path)
    for folder in folder_list:
        try: os.mkdir(folder)
        except: pass
        
        
os.chdir(OUTPUT_DIR)
try: os.mkdir(DATASET_NAME)
except: pass
OUTPUT_DIR = OUTPUT_DIR + DATASET_NAME
print(OUTPUT_DIR)
os.chdir(OUTPUT_DIR)
try: 
    os.makedirs('images/train')
    os.makedirs('labels/train')
except: pass

generate_folders(OUTPUT_DIR + '/images/train', OBJECT_NAMES)
os.chdir(OUTPUT_DIR)
generate_folders(OUTPUT_DIR + '/labels/train', OBJECT_NAMES)
os.chdir(OUTPUT_DIR)
if VAL_PERSENT > 0:
    try:
        os.makedirs('images/val')
        os.makedirs('labels/val')
    except: pass
    generate_folders(OUTPUT_DIR + '/images/val', OBJECT_NAMES)
    os.chdir(OUTPUT_DIR)
    generate_folders(OUTPUT_DIR + '/labels/val', OBJECT_NAMES)
    os.chdir(OUTPUT_DIR)
if TEST_PERSENT > 0:
    try: os.makedirs('images/test')
    except: pass
    generate_folders(OUTPUT_DIR + '/images/test', OBJECT_NAMES)
    os.chdir(OUTPUT_DIR)


b_file_list = [f for f in backgrounddir.glob('**/*.jpg') if f.is_file()]
t_file_list = [f for f in targetdir.glob('**/*.png') if f.is_file()]

num_b = len(b_file_list)
num_t = len(t_file_list)

kernel = np.ones((3, 3), np.uint8)

# validation case detecting
for i in range(0, NUM_IMAGE):
    if VAL_PERSENT > 0 and i % (100//VAL_PERSENT) == 0: val_mode = True
    else: val_mode = False

#test case detecting
    if TEST_PERSENT > 0 and i % (100 // TEST_PERSENT) == 0: test_mode = True
    else: test_mode = False

    bimg = cv2.imread(b_file_list[i % num_b].as_posix())
    timg = cv2.imread(t_file_list[i % num_t].as_posix())
    bimg = cv2.resize(bimg, (timg.shape[1], timg.shape[0]))

    mask1 = timg[:, :, 0] == 123
    mask2 = timg[:, :, 1] == 123
    mask3 = timg[:, :, 2] == 123
    mask = mask1 & mask2 & mask3
    mask = mask.astype(np.uint8) * 255

    _, thresh = cv2.threshold(mask, 100, 255, cv2.THRESH_BINARY_INV)
    thresh = cv2.erode(thresh, kernel, iterations=1)

    mask = thresh != 255
    timg[:, :, 0][mask] = bimg[:, :, 0][mask]
    timg[:, :, 1][mask] = bimg[:, :, 1][mask]
    timg[:, :, 2][mask] = bimg[:, :, 2][mask]

    # class name and number determination
    for obj in OBJECT_NAMES:
        if obj in t_file_list[i % len(t_file_list)].as_posix().lower():
            class_num = OBJECT_NAMES.index(obj)
            class_name = obj
            break
        else:
            class_num = len(OBJECT_NAMES) - 1
            class_name = 'ghost'

    #image file crating
    filename = str(i) + '.jpg'
    image_file = OUTPUT_DIR + "/images/train/" + class_name + "/" + filename
    cv2.imwrite(image_file, cv2.resize(timg, (1024, 768)))
    print(f'train {filename} image added to {class_name}')
    # val image file creating if needed
    if val_mode:
        shutil.copyfile(image_file, image_file.replace("train", "val"))
        print(f'val {filename} image added to {class_name}')
    if test_mode:
        shutil.copyfile(image_file, image_file.replace("train", "test"))
        print(f'test {filename} image added to {class_name}')

    #label file creating
    box = cv2.boundingRect(thresh)
    label_filename = filename.replace('.jpg', '.txt')
    label_file = OUTPUT_DIR + "/labels/train/" + class_name + "/" + label_filename
    with open(label_file, 'w') as f:
        midx = (box[0] + box[2] * 0.5) / timg.shape[1]
        midy = (box[1] + box[3] * 0.5) / timg.shape[0]
        print(class_num, midx, midy, box[2] / float(timg.shape[1]), box[3] / float(timg.shape[0]), file=f)
        f.close()
    print(f'train {label_filename} lable added to {class_name}')
    # val label file creating if needed
    if val_mode:
        shutil.copyfile(label_file, label_file.replace('train', 'val'))
        print(f'val {label_filename} lable added to {class_name}')

#crating yaml file
yaml_file_path = OUTPUT_DIR + '/'+ DATASET_NAME+ '.txt'
with open(yaml_file_path, 'w') as f:
    print("# Train/val/test sets as 1) dir: path/to/imgs, 2) file: path/to/imgs.txt, or 3) list: [path/to/imgs1, path/to/imgs2, ..]", file=f)
    print("path:", OUTPUT_DIR, file=f)
    print("train:", "# train images (relative to 'path')",  NUM_IMAGE, "images", file=f)
    for obj in OBJECT_NAMES:
        print("  -", "images/train/" + obj, file=f)
    if VAL_PERSENT > 0:
        print("val:", file=f)
        for obj in OBJECT_NAMES:
            print("  -", "images/val/" + obj, file=f)

    if TEST_PERSENT > 0:
        print("test:", file=f)
        for obj in OBJECT_NAMES:
            print("  -", "images/test/" + obj, file=f)

    print("\n# Classes", "\nnames:", file=f)
    for obj in OBJECT_NAMES:
        print("  " + str(OBJECT_NAMES.index(obj)) + ":", obj, file=f)
    f.close()
try:
    os.rename(yaml_file_path, yaml_file_path.replace('.txt', '.yaml'))
except FileExistsError:
    os.remove(yaml_file_path.replace('.txt', '.yaml'))
    os.rename(yaml_file_path, yaml_file_path.replace('.txt', '.yaml'))
print (f'Data set {DATASET_NAME} generated.')
