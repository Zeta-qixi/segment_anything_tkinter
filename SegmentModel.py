from typing import List
from segment_anything import sam_model_registry, SamPredictor
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
from pathlib import Path

checkpoint = Path("./assets/sam_vit_h_4b8939.pth")
model_type = "vit_h"
print(checkpoint)

class Sam:

    def __init__(self):

        self.sam = sam_model_registry[model_type](checkpoint=checkpoint)
        self.sam.to(device='cuda')
        self.predictor = SamPredictor(self.sam)
       
        self.input_points = []
        self.input_points_label = []
        self.points_masks = []


    def set_image(self, image_path):
        self.image = cv2.imread(image_path)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.predictor.set_image(self.image)


    def set_point(self,x,y):
        self.input_points.append(np.array([[x,y]]))
        self.input_points_label = np.array([1])
        print(self.input_points)

    def clean_point(self):
        self.points_masks = []
        self.input_points = []

    def set_box(self, box: List):
        self.input_box = np.array(box)


    def segment_item(self):
        

        for input_point in self.input_points:

            points_mask, scores, logits = self.predictor.predict(
            point_coords=input_point,
            point_labels=self.input_points_label,
            multimask_output=True,
            )
            self.points_masks.append(points_mask[0])

    def segment_box(self):
       
        self.box_masks, _, _ = self.predictor.predict(
            point_coords=None,
            point_labels=None,
            box=self.input_box[None, :],
            multimask_output=False,
        )



    def show(self):

        def show_anns( gray_image, brightness_increase, mask):
         
            for m in mask:
         
                gray_image = np.where(m, np.clip( brightness_increase, 0 , 255), gray_image)
            return gray_image

        gray_image = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY) 
        gray_image[~(self.box_masks[0])] = 20
        gray_image[(self.box_masks[0])] = 40
        new_gray = show_anns(gray_image, 100, self.points_masks)
        plt.figure(figsize=(10,10))

        plt.imshow(new_gray, cmap='gray')
        plt.axis('off')
        plt.show() 

sam = Sam()