import os
import cv2

def generate_txt(img_path, filename, coor_init_list, coor_end_list):
    file = open(os.path.join(img_path, filename.split('.')[0]+'.txt'), "a+")
    content = []
    for coor_init, coor_rls in zip(coor_init_list, coor_end_list):
        xmin = int(coor_init[0])
        ymin = int(coor_init[1])
        xmax = int(coor_rls[0])
        ymax = int(coor_rls[1])
        coords = convert(img_path, filename, [xmin, ymin, xmax, ymax])
        combine_coor = "0" + ' ' + str(coords[0]) + ' ' + str(coords[1]) + ' ' + str(coords[2]) + ' ' + str(coords[3])
        content.append(combine_coor)
        file.write(content[0] + '\n')
        content = []

    file.close()

def convert(img_path, filename_str, coords):
    image = cv2.imread(os.path.join(img_path,filename_str))
    coords[2] -= coords[0]
    coords[3] -= coords[1]
    x_diff = int(coords[2] / 2)
    y_diff = int(coords[3] / 2)
    coords[0] = coords[0] + x_diff
    coords[1] = coords[1] + y_diff
    coords[0] /= int(image.shape[1])
    coords[1] /= int(image.shape[0])
    coords[2] /= int(image.shape[1])
    coords[3] /= int(image.shape[0])
    return coords
