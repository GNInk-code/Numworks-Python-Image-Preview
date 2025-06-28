from skimage import io, transform
import numpy as np

# CHANGE THESE OPTIONS TO GET SMALLER DATA
quality = 100 #percentage
different_colors = 6 #powers of 2

sample_img = io.imread("./Media/Flower_p.jpg") #np array with rbg pixels of image

#---------------------------------------------------------------

#Decreasing quality

sample_img = transform.resize(sample_img, (len(sample_img)//(100/quality), len(sample_img[0])//(100/quality)), anti_aliasing=True)
sample_img = (sample_img * 255).astype(np.uint8) # values are stored as floating points betwenn 0-1

#---------------------------------------------------------------

#Colors - Median cut algorithm from https://muthu.co/reducing-the-number-of-colors-of-an-image-using-median-cut-algorithm/
#This algorithm finds the 2^x different common colors in the image

def median_cut_quantize(img, img_arr):
    # when it reaches the end, color quantize
    r_average = np.mean(img_arr[:,0])
    g_average = np.mean(img_arr[:,1])
    b_average = np.mean(img_arr[:,2])
    
    for data in img_arr:
        sample_img[data[3]][data[4]] = [r_average, g_average, b_average] #Change data
    
def split_into_buckets(img, img_arr, depth):
    
    if len(img_arr) == 0:
        return 
        
    if depth == 0:
        median_cut_quantize(img, img_arr)
        return
    
    r_range = np.max(img_arr[:,0]) - np.min(img_arr[:,0])
    g_range = np.max(img_arr[:,1]) - np.min(img_arr[:,1])
    b_range = np.max(img_arr[:,2]) - np.min(img_arr[:,2])
    
    space_with_highest_range = 0

    if g_range >= r_range and g_range >= b_range:
        space_with_highest_range = 1
    elif b_range >= r_range and b_range >= g_range:
        space_with_highest_range = 2
    elif r_range >= b_range and r_range >= g_range:
        space_with_highest_range = 0


    # sort the image pixels by color space with highest range 
    # and find the median and divide the array.
    img_arr = img_arr[img_arr[:,space_with_highest_range].argsort()]
    median_index = int((len(img_arr)+1)/2)
    
    #split the array into two buckets along the median
    split_into_buckets(img, img_arr[0:median_index], depth-1)
    split_into_buckets(img, img_arr[median_index:], depth-1)
    
flattened_img_array = []
for rindex, rows in enumerate(sample_img):
    for cindex, color in enumerate(rows):
        flattened_img_array.append([color[0],color[1],color[2],rindex, cindex]) 
        
flattened_img_array = np.array(flattened_img_array)

# the 3rd parameter represents how many colors are needed in the power of 2. If the parameter 
# passed is 4 its means 2^4 = 16 colors ==> max 2^6 = 64
split_into_buckets(sample_img, flattened_img_array, different_colors)

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ&|@#?!$%/*=+" #64 different chars used for colors
chars = list(chars) #Easier when it is a list
colors = []

flattened_img_array = [] #Another array with new values
for rindex, rows in enumerate(sample_img):
    for cindex, color in enumerate(rows):
        flattened_img_array.append([color[0], color[1], color[2], rindex, cindex]) 
        

for pixel in flattened_img_array: #To put every different color in colors
    
    for color in colors:
        if pixel[0] == color[0] and pixel[1] == color[1] and pixel[2] == color[2]:
            break
    else:
        colors.append([pixel[0], pixel[1], pixel[2]])
        


#---------------------------------------------------------------
#Encode

image_data = []

result = ''
count = 0
index = 0

for pixel in flattened_img_array:
    
    color = pixel[:3] # Only taking rgb values
    
    try:
        if pixel[4] == len(sample_img[0])-1: # Throws an error to pass to the next line
            raise Exception("Next line")

        if flattened_img_array[index][:3] == flattened_img_array[index+1][:3]: # If the color is the same for the next pixel...
            count += 1
            color = pixel[:3]
        else:
            result += (str(count + 1) if count else "") + chars[colors.index(color)] # Otherwise it puts the number of same-color pixels next to the color code
            count = 0
    except:
        result += (str(count + 1) if count else "") + chars[colors.index(color)] # When it finishes the line it puts the result in the image_data list
        image_data.append(result)
        result = ""
        count = 0
    
    index += 1

#---------------------------------------------------------------
#Save

with open("image_data.py", "w") as file:
    file.write("image_data=")
    file.write(str(image_data))
    file.write("\ncolor_map={")
    index = 0
    for color in colors:
        char = chars[index]
        tup = (color[0], color[1], color[2])
        file.write(f'\'{char}\':{str(tup)},')
        index += 1
    file.write("}")
