import matplotlib.pyplot as plt # single use of plt is commented out
import os.path  
import PIL.ImageDraw            

def frame(original_image, color, frame_width):
    """ Put frame around a PIL.Image
    
    original_image must be a PIL.Image
    Returns a new PIL.Image with a frame, where
    0 < frame_width < 1
    is the border as a portion of the shorter dimension of original_image
    """
    #set the radius of the rounded corners
    width, height = original_image.size
    thickness = int(frame_width * min(width, height)) # thickness in pixels
    
    ###
    #create a mask
    ###
    
    #start with transparent mask
    if height < 500:
        r, g, b = color
    else:
        r, g, b = (255, 255, 255)
    frame_mask = PIL.Image.new('RGBA', (width, height), (0,0,0,0))
    drawing_layer = PIL.ImageDraw.Draw(frame_mask)
    drawing_layer.rectangle((0,0,width,thickness), fill=(r, g, b, 255))
    drawing_layer.rectangle((0,height,thickness,0), fill=(r, g, b, 255))
    drawing_layer.rectangle((width,height,0,height-thickness), fill=(r, g, b, 255))
    drawing_layer.rectangle((width,height,width-thickness,0), fill=(r, g, b, 255))

    drawing_layer.polygon((3*thickness,0,0,3*thickness,0,0), fill=(73, 31, 3, 255))
    drawing_layer.polygon((width,0,width-3*thickness,0,width,3*thickness), fill=(73, 31, 3, 255))
    drawing_layer.polygon((0,height,0,height-3*thickness,3*thickness,height), fill=(73, 31, 3, 255))
    drawing_layer.polygon((width,height,width-3*thickness,height,width,height-3*thickness), fill=(73, 31, 3, 255))
    # Make the new image, starting with all transparent
    result = original_image.copy()
    result.paste(frame_mask, (0,0), mask=frame_mask)
    return result
  
def get_images(directory=None):
    """ Returns PIL.Image objects for all the images in directory.
    
    If directory is not specified, uses current directory.
    Returns a 2-tuple containing 
    a list with a  PIL.Image object for each image file in root_directory, and
    a list with a string filename for each image file in root_directory
    """
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    image_list = [] # Initialize aggregaotrs
    file_list = []
    
    directory_list = os.listdir(directory) # Get list of files
    for entry in directory_list:
        absolute_filename = os.path.join(directory, entry)
        try:
            image = PIL.Image.open(absolute_filename)
            file_list += [entry]
            image_list += [image]
        except IOError:
            pass # do nothing with errors tying to open non-images
    return image_list, file_list

def frame_all_images(directory=None, color=(255,0,0), frame_width=.1):
    """ Saves a modfied version of each image in directory.
    
    Uses current directory if no directory is specified. 
    Places images in subdirectory 'modified', creating it if it does not exist.
    New image files are of type PNG and have transparent rounded corners.
    """
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    # Create a new directory 'modified'
    new_directory = os.path.join(directory, 'grayscale')
    try:
        os.mkdir(new_directory)
    except OSError:
        pass # if the directory already exists, proceed  
    
    #load all the images
    image_list, file_list = get_images(directory)  

    #go through the images and save modified versions
    for n in range(len(image_list)):
        # Parse the filename
        filename, filetype = (file_list[n]).split('.')
        
        # Round the corners with radius = 30% of short side
        gray_image = grayscale(file_list[n])
        #save the altered image, suing PNG to retain transparency
        gray_image_filename = os.path.join(new_directory, filename + '.png')
        gray_image.save(gray_image_filename) 
    gray_directory = os.path.join(new_directory, 'framed')
    image_list, file_list = get_images(new_directory)  

    # Go through the images and save modified versions
    for n in range(len(image_list)):
        # Parse the filename

        filename, filetype = file_list[n].split('.') 
        
        # Round the corners with default percent of radius
        new_image = frame(image_list[n],color,frame_width) 
     
        # Save the altered image, suing PNG to retain transparency
        new_image_filename = os.path.join(gray_directory, filename + '.png')
        new_image.save(new_image_filename)    
    
         
def grayscale(filename):
    directory = os.path.dirname(os.path.abspath(__file__))
    input_image_path = os.path.join(directory, filename)

    color_image = PIL.Image.open(input_image_path)
    bw = color_image.convert('L')
    return bw