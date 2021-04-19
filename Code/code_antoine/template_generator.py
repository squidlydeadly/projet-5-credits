
import numpy as np
import cv2
import vision

def circle(half_length,radius,max_val=255):
    """crée un cercle en nuances de gris

    Parameters
    ----------
    half_length : int
        demi grandeur de l'image
    radius : int
        rayon du cercle
    max_val : int
        valeur maximal par pixel

    Returns
    -------
    array of array of float
        image de cercle

    """
    template = np.zeros((2*half_length +1,2*half_length +1))
    center = vision.get_template_center(2*half_length+1,2*half_length+1)
    for i in range(2*half_length+1):
        for j in range(2*half_length+1):
            dist_center = np.linalg.norm(np.array([i,j]) - center)
            template[i,j] = np.round(max_val*np.sin(min(max(radius + 0.5 - dist_center,0),1)*np.pi/2))
    return template

def ring(radius_e,radius_i,max_val=255):
    """crée une image en nuances de gris d'un anneau

    Parameters
    ----------
    radius_e : int
        rayon externe de l'anneau
    radius_i : int
        rayon interne de l'anneau
    max_val : int
        valeur maximal d'un pixel

    Returns
    -------
    array of array of float
        image de l'anneau

    """
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
