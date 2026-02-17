import json

import base64

print('Type json file name (without format .json):')
img_name=input()

print('Preferable image format: j - jpeg, p - png')
img_type=input()


with open(img_name+'.json','r') as f:
    in_data=json.load(f)
#dict_keys(['label', 'level', 'image', 'id', 'visible', 'topleft', 'topright', 'bottomleft', 'bottomright', 'origWidth', 'origHeight', 'selected', 'opacity'])

lat=in_data[0]['topleft']['lat']
lng=in_data[0]['topleft']['lng']
lat_2=in_data[0]['bottomright']['lat']
lng_2=in_data[0]['bottomright']['lng']
w=in_data[0]['origWidth']
h=in_data[0]['origHeight']
A=(lng_2-lng)/w
D=0
B=0
E=(lat_2-lat)/h
C=lng
F=lat
in_64=in_data[0]['image'].replace('data:image/jpeg;base64,','')

if img_type=='j':
    out=img_name+'.jpg'
    out_world=img_name+'.jpw'
elif img_type=='p':
    out=img_name+'.png'
    out_world=img_name+'pgw'

def base64_to_img(base64_string:str,output_path:str):
    try:
        # If starting with a string, encode it back to bytes
        if isinstance(base64_string, str):
            base64_bytes_to_decode = base64_string.encode('utf-8')
        else: # Assuming input is already bytes
            base64_bytes_to_decode = base64_bytes # Use the bytes variable directly

        # Decode the Base64 bytes to get the original image bytes
        # Use decodebytes for modern Python (handles potential whitespace/newlines)
        image_data = base64.decodebytes(base64_bytes_to_decode)

        # Alternatively, b64decode can be used if input is strictly Base64 encoded bytes
        # image_data = base64.b64decode(base64_bytes_to_decode)

        # Open the output file in binary write mode
        with open(output_path, 'wb') as output_file:
            # Write the decoded image data
            output_file.write(image_data)

        print(f"Image successfully decoded and saved to {output_path}")

    except base64.binascii.Error as e:
        print(f"Base64 Decoding Error: {e}. Check if the input string is valid Base64.")
    except Exception as e:
        print(f"An error occurred during decoding/saving: {e}")

base64_to_img(in_64,out)

with open(out_world,'w') as f:
    f.write(str(A)+'\n'+
            str(D)+'\n'+
            str(B)+'\n'+
            str(E)+'\n'+
            str(C)+'\n'+
            str(F))

#    Line 1: A: pixel size in the x-direction in map units/pixel
#    Line 2: D: rotation about y-axis
#    Line 3: B: rotation about x-axis
#    Line 4: E: pixel size in the y-direction in map units, almost always negative[b]
#    Line 5: C: x-coordinate of the center of the upper left pixel
#    Line 6: F: y-coordinate of the center of the upper left pixel

