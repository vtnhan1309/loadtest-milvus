import glob
import random
import base64
import cv2



class ImageLoader:
    def __init__(self, src_dir):
        self.src_dir = src_dir
        pt = self.src_dir + '/*'
        self.img_paths = glob.glob(pt)
        
    
    def get_image_base64(self,):
        path = random.choice(self.img_paths)
        img = cv2.imread(path)
        noised_img = img
        _, im_arr = cv2.imencode('.jpg', noised_img)
        img_bytes = im_arr.tobytes()
        return base64.b64encode(img_bytes).decode()
