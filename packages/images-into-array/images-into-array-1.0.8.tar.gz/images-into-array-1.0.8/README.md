# Convert-Images-Into-Array:
---------------------------
Convert Multiple images into a array and saved it into .npy file and letter user it for various task :
------------------------------------------------------------------------------------------------------
This package fuction requres two argument one is path of the images folder and another is image size.

# How to import the module:
---------------------------

from images_into_array.images_into_array import images

images_path = ('')


image_size = set the value [32, 64, 128] [(32*32), (64*64), (128*128)]

array = images(images_path, image_size)

print(array.shape)



 Required package’s:
---------------------

• conda install -c conda-forge opencv=4.2.0

• pip install shuffle

• pip install numpy

• pip install tqdm

License:
--------
MIT Licensed

Author:
-------
Sujit Mandal

LinkedIn : https://www.linkedin.com/in/sujit-mandal-91215013a/

Facebook : https://www.facebook.com/sujit.mandal.33671748

Twitter : https://twitter.com/mandalsujit37