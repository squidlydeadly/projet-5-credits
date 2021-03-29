
import numpy as np
import cv2
import vision

def circle(half_length,radius,max_val=255):
    template = np.zeros((2*half_length +1,2*half_length +1))
    center = vision.get_template_center(2*half_length+1,2*half_length+1)
    for i in range(2*half_length+1):
        for j in range(2*half_length+1):
            dist_center = np.linalg.norm(np.array([i,j]) - center)
            template[i,j] = np.round(max_val*np.sin(min(max(radius + 0.5 - dist_center,0),1)*np.pi/2))
    return template

def ring(radius_e,radius_i,max_val=255):
    template = np.zeros((2*radius_e +1,2*radius_e +1))
    center = vision.get_template_center(2*radius_e+1,2*radius_e+1)
    for i in range(2*radius_e+1):
        for j in range(2*radius_e+1):
            dist_center = np.linalg.norm(np.array([i,j]) - center)
            ring_interior_center = (radius_e + radius_i +1)/2
            ring_half_thikness = (radius_e-radius_i)/2
            template[i,j] = np.round(max_val*np.sin(min(max(ring_half_thikness - abs(dist_center - ring_interior_center),0) ,1)*np.pi/2))
    return template


if __name__ == '__main__':
    img = ring(64,60)
    cv2.imwrite('test.jpg',img.astype(np.uint8))
