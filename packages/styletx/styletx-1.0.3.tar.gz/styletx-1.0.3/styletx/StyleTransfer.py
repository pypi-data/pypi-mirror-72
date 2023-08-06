import torch
import numpy as np
from torchvision import models
from PIL import Image
from .process import *
import tqdm

def StyleTransfer(content_img, style_img, alpha=1, beta=10, epochs=500):
    ''' Transfers the style of the image given by the user
    INPUT:
        content_img - the image for which the style transfer is to be applied (type: PIL)
        style_img - the image whose style is to be transfered to content_img (type: PIL)
        alpha - weight of the content info used in the error function (type: positive int)
        beta -  weigth of the style info used in the error function (type: positive int)
        epochs - number of iterations to be done (type: positive int)
        checkpoint - display the intermediate result for every checkpoint (type: positive int)
    OUTPUT:
        target_img - style transfered image (type: PIL)
    '''

    # set device to train
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print('Training in', device, '...')

    # load the network from the models folder
    model = models.vgg19(pretrained=True).features
    # freeze all VGG parameters
    for param in model.parameters():
        param.requires_grad_(False)

    # change the images to torch tensor and move to the device
    content_tensor, _, _ = pre_process(content_img)
    style_tensor, style_mean, style_var = pre_process(style_img, shape=content_tensor.shape[2:])

    content_tensor = content_tensor.to(device)
    style_tensor = style_tensor.to(device)

    # layers used in the model with weights to transfer the style
    style_layer_weights = {'conv1_1': 1.,
                           'conv2_1': 0.75,
                           'conv3_1': 0.2,
                           'conv4_1': 0.2,
                           'conv5_1': 0.2}
    content_layer_weights = {'conv4_2': 1}

    # create target tensor from content tensor, set the gradient on and move it to the device
    target_tensor = content_tensor.clone().requires_grad_(True).to(device)

    # extracting the layers from the network for the content and style tensor
    content_layers = layer_extract(model, content_tensor)
    style_layers = layer_extract(model, style_tensor)
    # gram maatrix for the style layers
    style_layers = {layer: gram_matrix(style_layers[layer]) for layer in style_layers} 

    # set the optimizer
    optimizer = torch.optim.Adam([target_tensor], lr=0.01)

    for i in tqdm.tqdm(range(1, epochs+1), desc='Progress'):

        # extract the layers from the network for the target tensor
        target_layers = layer_extract(model, target_tensor)

        # calculate the individual loss for content and style
        content_layer_loss = calculate_layer_loss(target_layers, content_layers, content_layer_weights)
        style_layer_loss = calculate_layer_loss(target_layers, style_layers,style_layer_weights, style=True)
    
        # total loss of the system
        total_loss = alpha * content_layer_loss + beta * style_layer_loss
    
        optimizer.zero_grad()
        total_loss.backward()
        optimizer.step()

    # get the output image from the output(target) tensor
    target_img = denorm_tensor(target_tensor, style_mean, style_var)

    # convert the image type from numpy to PIL object
    target_img = Image.fromarray(np.uint8(target_img * 255))
    
    return target_img
