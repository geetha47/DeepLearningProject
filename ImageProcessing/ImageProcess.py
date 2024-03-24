import cv2
import os
import numpy as np

#cube details
cube_info = {
    1: {'x': 267, 'y': 1324, 'w': 61, 'h': 61},
    2: {'x': 372, 'y': 1314, 'w': 59, 'h': 57},
    3: {'x': 489, 'y': 1311, 'w': 56, 'h': 60},
    4: {'x': 425, 'y': 1209, 'w': 57, 'h': 60},
    5: {'x': 221, 'y': 1209, 'w': 58, 'h': 59},
    6: {'x': 528, 'y': 1159, 'w': 57, 'h': 61},
    9: {'x': 477, 'y': 1026, 'w': 56, 'h': 62},
    10: {'x': 220, 'y': 1013, 'w': 58, 'h': 59},
    11: {'x': 100, 'y': 965, 'w': 63, 'h': 61},
    13: {'x': 543, 'y': 890, 'w': 59, 'h': 62},
    15: {'x': 441, 'y': 833, 'w': 59, 'h': 62},
    16: {'x': 136, 'y': 820, 'w': 55, 'h': 61},
    17: {'x': 234, 'y': 771, 'w': 60, 'h': 60},
    18: {'x': 527, 'y': 753, 'w': 64, 'h': 62},
    20: {'x': 381, 'y': 664, 'w': 59, 'h': 63},
    24: {'x': 310, 'y': 548, 'w': 64, 'h': 63},
    34: {'x': 96, 'y': 293, 'w': 56, 'h': 61},
    35: {'x': 212, 'y': 281, 'w': 60, 'h': 64},
    36: {'x': 558, 'y': 242, 'w': 59, 'h': 59},
    37: {'x': 416, 'y': 228, 'w': 59, 'h': 61},


    7: {'x': 352, 'y': 1130, 'w': 40, 'h': 60},
    8: {'x': 141, 'y': 1103, 'w': 58, 'h': 63},
    12: {'x': 356, 'y': 962, 'w': 61, 'h': 64},
    14: {'x': 340, 'y': 836, 'w': 57, 'h': 59},
    19: {'x': 92, 'y': 718, 'w': 61, 'h': 60},
    21: {'x': 251, 'y': 639, 'w': 57, 'h': 64},
    22: {'x': 502, 'y': 607, 'w': 66, 'h': 63},
    23: {'x': 149, 'y': 600, 'w': 55, 'h': 62},
    25: {'x': 105, 'y': 511, 'w': 62, 'h': 62},
    26: {'x': 469, 'y': 486, 'w': 60, 'h': 63},
    27: {'x': 219, 'y': 482, 'w': 64, 'h': 64},
    28: {'x': 567, 'y': 458, 'w': 64, 'h': 65},
    29: {'x': 79, 'y': 408, 'w': 61, 'h': 61},
    30: {'x': 395, 'y': 398, 'w': 64, 'h': 61},
    31: {'x': 179, 'y': 381, 'w': 65, 'h': 64},
    32: {'x': 503, 'y': 350, 'w': 58, 'h': 62},
    33: {'x': 315, 'y': 332, 'w': 59, 'h': 61},
    38: {'x': 163, 'y': 146, 'w': 58, 'h': 59},
    39: {'x': 297, 'y': 141, 'w': 62, 'h': 55},
    40: {'x': 478, 'y': 136, 'w': 63, 'h': 66},
    41: {'x': 537, 'y': 49, 'w': 70, 'h': 63},
    42: {'x': 391, 'y': 37, 'w': 66, 'h': 61}
}


mean_intensity_values = {}
margin = 5
folder_path = 'Images/'
n=0
# Get a list of all files in the folder
file_list = os.listdir(folder_path)
print(file_list)
# Iterate over each file in the folder
for file_name in file_list:
    # Check if the file is an image (you can add more image extensions if needed)
    if file_name.endswith('.JPG'):
        # Construct the full path to the image file
        image_path = os.path.join(folder_path, file_name)
        image = cv2.imread(image_path)
        img_copy = image.copy()

        n=n+1
        #print(n)
        for cube_id, info in cube_info.items():
            x, y, w, h = info['x'], info['y'], info['w'], info['h']

            x -= margin
            y -= margin
            w += 2 * margin
            h += 2 * margin

            x = max(0, x)
            y = max(0, y)
            w = min(w, image.shape[1] - x)
            h = min(h, image.shape[0] - y)

            # extract the cube
            cube = image[y:y + h, x:x + w]
            mean_intensity = np.mean(cube)
            min_intensity = np.min(cube)
            max_intensity = np.max(cube)

            # Normalize the intensities
            # normalized_intensity = (mean_intensity - min_intensity) / (max_intensity - min_intensity)

            mean_intensity_values[cube_id] = {'mean': mean_intensity, 'min': min_intensity, 'max': max_intensity}

            gray = cv2.cvtColor(cube, cv2.COLOR_BGR2GRAY)

            # Apply the logarithm transformation
            log_transformed_image = np.log1p(gray.astype(np.float32))

            # Normalize the transformed image to the range [0, 255]
            log_transformed_image = cv2.normalize(log_transformed_image, None, 0, 255, cv2.NORM_MINMAX)

            # Convert the transformed image back to uint8 data type
            log_transformed_image = np.uint8(log_transformed_image)
            blurred = cv2.GaussianBlur(log_transformed_image, (5, 5), 0)
            unsharp_mask = cv2.addWeighted(log_transformed_image, 1.5, blurred, -0.5, 0)

            pores=[1,2,3,4,5,6,9,10,11,13,15,16,17,18,20,24,34,35,36,37]
            if cube_id in pores:
                output_dir = 'Defective_cubes_01/histEqu'
            else:
                output_dir = 'Quality_cubes_01/HistEqu'
            os.makedirs(output_dir, exist_ok=True)

            cv2.imwrite(os.path.join(output_dir, f'{n}_B{cube_id}.jpg'), gray)

            cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)
cv2.imshow("Cubes", img_copy)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''    
# Find min and max intensity values across all cubes
min_intensity = min(mean_intensity_values[cube_id]['min'] for cube_id in mean_intensity_values)
max_intensity = max(mean_intensity_values[cube_id]['max'] for cube_id in mean_intensity_values)

# Normalize mean intensity values for all cubes
normalized_intensity_values = {}
for cube_id, intensity in mean_intensity_values.items():
    mean_intensity = intensity['mean']
    normalized_intensity = (mean_intensity - min_intensity) / (max_intensity - min_intensity)
    normalized_intensity_values[cube_id] = normalized_intensity

# Print normalized intensity values for all cubes
for cube_id, normalized_intensity in normalized_intensity_values.items():
    print(f'B{cube_id}: Normalized Intensity = {round(normalized_intensity,2)}')


'''
# display image
