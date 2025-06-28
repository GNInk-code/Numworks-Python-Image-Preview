import math
import kandinsky

import image_data

width = 320
height = 222

line = 0

def rgb_to_hex(rgb:tuple[int, int, int]) -> str:
    return str('#'+('%02x%02x%02x' % rgb))

def decompress_line(line:str) -> str:
    count = ""
    result = ""
    for char in line:
        if char.isdigit():
            count += char
        else:
            result += char * (int(count) if count else 1)
            count = ""
    
    return result

for line in range(len(image_data.image_data)):
    
    if height/len(image_data.image_data) <= width/len(decompress_line(image_data.image_data[0])): #If the scale should be made according to height or width
        scale = math.floor(height/len(image_data.image_data))
    else:
        scale = math.floor(width/len(decompress_line(image_data.image_data[0])))
        
    y = image_data.image_data[line]
    ix = 0
    for x in decompress_line(y):
        color = rgb_to_hex(image_data.color_map.get(x, (0,0,0)))
        kandinsky.fill_rect(ix * scale, line * scale, scale, scale, color)
        ix+=1
        
