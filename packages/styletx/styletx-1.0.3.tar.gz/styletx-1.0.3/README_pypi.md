# styletx
**styletx** is a python package that applies effects of an image to another image using machine learning.

## Installation
You can install the styletx package using the command given below

`pip install styletx`

## Requirements
Python3

**styletx** depends on the following python packages
```
torch==1.5.0
torchvision==0.6.0
numpy==1.19.0
pillow==7.1.2
tqdm==4.46.1
```
All the requirements stated above are used in creating the project, lower versions of the requirements may or may not work.\
Also, using GPU will significantly reduce the run time of the script. Make sure to get `torch` and `torchvision` version that supports GPU.

## Implementation

```
# import necessary packages
from styletx import StyleTransfer
from PIL import Image
import matlibplot.pyplot as plt

# import the images
content_image = Image.open('path/filename')
style_image = Image.open('path/filename')

# implement StyleTransfer
output_image = StyleTransfer(content_image, style_image, alpha=1, beta=10, epochs=500)

# plot the results
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
ax1.imshow(content_image)
ax2.imshow(output_image)
plt.show()
```
The above code will apply the effects of the `style_image` to `content_image`.

## Inputs
`content_image` - a PIL object\
`style_image` - a PIL object\
`alpha` - a positive integer\
`beta` - a positive integer\
`epochs` - a positive integer

By default `alpha` = 1, `beta` = 10 and `epochs` = 500.
You can play around these values to get desired output image.

## Example
![](https://raw.githubusercontent.com/dinesh-GDK/StyleTx/master/images/Result.png)

## References
The complete theory behind the **StyleTransfer** can be found in this [link](https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Gatys_Image_Style_Transfer_CVPR_2016_paper.pdf).
