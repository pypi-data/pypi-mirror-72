import torch
import numpy as np
from torchvision import transforms

def pre_process(image, max_size=500, shape=None):

    '''Pre Processes the image
    INPUT:
        image - A coloured image (type: PIL)
        max_size - size limit for the image (type: int)
    OUTPUT:
        image - a torch tensor (type: 4D tensor)
        mean - mean value of the original image (type: numpy array of size 3 (R G B))
        var - variance of the original image (type: numpy array of size 3 (R G B))
    '''
    image = image.convert('RGB')
    
    # Sets the size of the image
    if max(image.size) > max_size:
        size = max_size
    else:
        size = max(image.size)
    
    if shape is not None:
        size = shape
        
    mean = np.array(image).mean(axis=(0, 1))/255   # calculate the mean of the image for R, G and B
    var = np.array(image).std(axis=(0, 1))/255     #calculate the variance of the image for R, G and B

    # Resize, convert to tensor and normalize the image    
    transform = transforms.Compose([transforms.Resize(size),
                                    transforms.ToTensor(),
                                    transforms.Normalize(tuple(mean), tuple(var))])
    image = transform(image)[:3,:,:].unsqueeze(0)

    return image, mean, var

def denorm_tensor(tensor_image, mean, var):
    
    '''Converts and return a normalized torch tensor to de-normalized numpy image
    INPUTS:
        tensor_image - a normalized image (type: 4D tensor)
        mean - mean value of the original image (type: numpy array of size 3(R G B))
        var - variance of the original image (type: numpy array of size 3(R G B))
    OUTPUT:
        image - returns the denormalized image (type : numpy array)
    '''
    
    image = tensor_image.to("cpu").clone().detach()    # convert to numpy array
    image = image.numpy().squeeze()
    image = image.transpose(1,2,0)                     # set to correct dimension
    image = image * var + mean                         # de-normalize the image
    image = image.clip(0, 1)                           # change the range to plot in numpy
    
    return image

def gram_matrix(tensor):
    
    """ Calculate the Gram Matrix of a given tensor 
        INPUT:
        tensor - a tensor (type: torch tensor)
        
        OUTPUT:
        gram - Gram Matrix of thr tensor
    """
    
    # get the depth, height, and width of the Tensor
    _, d, h, w = tensor.size()
    
    # reshape - multiplying the features for each channel
    tensor = tensor.view(d, h * w)
    
    # calculate the gram matrix
    gram = torch.mm(tensor, tensor.t())
    
    return gram 

def layer_extract(model, image_tensor, layers=None):
    
    '''Extract the required layers from the CNN model of the image
        INPUTS:
            model - complete CNN model used in the process (type : torch model)
            image_tensor - normalized tensor of the image (type : 4D tensor)
            layers - the info of the layers to be extracted from thr model (type : dictionary)
        
        OUTPUT:
            features - contains the tensors of the specified layers (type : dictionary)
    '''
    
    if layers is None:
        layers = {'0'  : 'conv1_1',
                  '5'  : 'conv2_1',
                  '10' : 'conv3_1',
                  '19' : 'conv4_1',
                  '21' : 'conv4_2',
                  '28' : 'conv5_1'}
    layer_extract= {}
    x = image_tensor
    for label, layer in model._modules.items():
        x = layer(x)
        if label in layers:
            layer_extract[layers[label]] = x
            
    return layer_extract  

def calculate_layer_loss(target_layers, feature_layers, layer_weights, style=False):

    ''' Calculate loss of individual layers
    INPUT:
        target_layers - target tensor layers for which the loss to be calculated (type: dictionary)
        feature_layers - cotent/style tensor layers for which the loss to be calculated (type: dictionary)
        layer weights - weight of the individual layers (type: dictionary)
        style - if True calculate gram matrix of the style layer tensors (type: True/False)
    OUTPUT:
        loss - content/style loss (type: float)
    '''

    loss = 0
    for layer in layer_weights:
        
        target_layer = target_layers[layer]
        feature_layer = feature_layers[layer]
        _, d, h, w = target_layer.shape
        
        # calculate gram matrix of style layers
        if style is True:
            target_layer = gram_matrix(target_layer)
            
        loss += layer_weights[layer] * torch.mean((target_layer - feature_layer) **2) / (d * h * w)
        
    return loss

