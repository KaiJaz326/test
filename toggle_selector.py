from matplotlib.widgets import RectangleSelector
import matplotlib.pyplot as plt
import numpy
import os
import cv2
from generate_label import generate_txt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--data_path", default = "/home/kaijaz/FYP/dataset", type=str, help = 'path to dataset')

coor_init_list = []
coor_end_list = []
obj_list = []
image_shape = []
filename = None
count = 0
global path

def box_select_callback(click,rls):
    global coor_init_list
    global coor_end_list
    global obj_list
    coor_init_list.append((int(click.xdata),int(click.ydata)))
    coor_end_list.append((int(rls.xdata),int(rls.ydata)))

#keyboard press function
def key_press_event(event):
    global coor_init_list
    global coor_end_list
    global obj_list
    global image_shape
    global filename
    global count
    if event.key == 'q':
        # info of the cropped objects
        if len(coor_end_list) < 1:
            print("Empty file")
            print()
        else:
            index = 0
            for x, y in zip(coor_init_list, coor_end_list):
                print('object {}, x_min:{}, ymin:{}, xmax:{}, ymax:{}'.format(index+1, x[0], y[0], x[1], y[1]))
                index += 1
            print("{} objects".format(len(coor_init_list)))
            # write into xml file
            # generate_xml(path,object,filename,image_shape[0][0],image_shape[0][1],coor_init_list,coor_end_list)
            # write into text file
            generate_txt(path, filename, coor_init_list, coor_end_list)
            print()
            print('close {}'.format(filename))
            print("__________________")
            print()

            # reset everything
            coor_end_list = []
            coor_init_list = []
            obj_list = []
            image_shape = []
            filename = None
            index = 0
            count += 1
            plt.close()

if __name__ == '__main__':
    # return parser content
    args = parser.parse_args()
    path = args.data_path

    for image in os.listdir(path):
        if image.endswith(".txt"):
            continue

        img = cv2.imread(path+'/'+image)
        filename = image
        if img is None:
            continue
        else:
            print("Currently on image {}".format(image))
            print()
            image_shape.append(img.shape)
            RGB_img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            plt.style.use("dark_background")
            # plot image out
            fig, ax = plt.subplots(1, figsize = (14,7))
            ax.imshow(RGB_img)

            # set RS to an instance to perform task
            tog_selector = RectangleSelector(
                ax,
                box_select_callback, # callback function to perform for the selection rectangle selector on ax
                drawtype='box',
                useblit=True, button=[1], # 1 for left key
                spancoords='pixels', interactive=True
            )
            # activate instance
            tog_selector.set_active(True)

            # connect keyboard press event (function)
            plt.connect('key_press_event', key_press_event)
            plt.show()
            count += 1
