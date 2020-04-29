import numpy as np
from matplotlib import pyplot as plt
from scipy import signal
from scipy.spatial import Delaunay
from tqdm.auto import tqdm

# img = plt.imread('wbsdxpRswQLybPny.jpg')
# img = plt.imread('image.jpg')
# img = plt.imread('Godzill.png')
img = plt.imread('Day9_Picture_Real1.jpg')

scharr = np.array([[ -3-3j, 0-10j,  +3 -3j],
                   [-10+0j, 0+ 0j, +10 +0j],
                   [ -3+3j, 0+10j,  +3 +3j]]) # Gx + j*Gy

grad = np.mean([np.abs(signal.convolve2d(img[:,:,i], scharr, boundary='symm', mode='same')) for i in range(img.shape[2])],axis=0)
grad += np.mean(grad)/10
print(grad.shape,img.shape)
N = 5000
vertices_index = np.random.choice(np.arange(grad.shape[0]*grad.shape[1]),p=grad.flatten()/np.sum(grad),size=N,replace=False)
vertices = np.array(np.unravel_index(vertices_index,grad.shape[::-1])).T
corners = [[0,0],[0,grad.shape[0]],[grad.shape[1],0],grad.shape[::-1]]
vertices = np.concatenate((vertices,corners),axis=0) #N+4 points
tri = Delaunay(vertices) 
# plt.plot(vertices[:,0],vertices[:,1],'.')
# for i1,i2,i3 in tri.simplices:
#     plt.plot(*vertices[[i1,i2,i3,i1]].T,'b')
# plt.show()
x,y = np.arange(img.shape[1],dtype=int), np.arange(img.shape[0],dtype=int)
X,Y = np.meshgrid(x,y)
lis_image_points = np.stack((X,Y),axis=2).reshape(-1,2)

faces = tri.find_simplex(lis_image_points)
new_img = np.zeros_like(img)

#
img_flat = img.reshape(-1,img.shape[-1])
new_img_flat = new_img.reshape(-1,new_img.shape[-1])
for i in tqdm(set(faces)):
    cor_in_face = faces==i
    if np.any(cor_in_face):
        new_img_flat[cor_in_face] = np.mean(img_flat[cor_in_face],axis=0)
new_img = new_img_flat.reshape(*img.shape)


plt.figure(figsize=(16,8))
plt.subplot(1,2,1)
plt.axis('off')
plt.imshow(img)
plt.subplot(1,2,2)
plt.axis('off')
plt.imshow(new_img)
plt.tight_layout()
plt.show()