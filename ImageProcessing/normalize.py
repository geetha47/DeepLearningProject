def normalize(value, min_val, max_val):
    scaled= (value - min_val) / (max_val - min_val)
    return scaled

# Defect area % values
defect_area_values = [
    0.237, 0.263, 0.137, 0.106, 0.164, 0.141, 3.879, 0.721, 0.223, 0.054,
    0.270, 2.076, 0.067, 1.151, 0.124, 0.096, 0.097, 0.361, 0.51, 0.25,
    1.14, 0.78, 1.84, 0.19, 1.20, 2.95, 1.73, 2.33, 3.18, 0.70, 0.72,
    1.95, 2.84, 0.03, 0.04, 0.08, 0.19, 0.75, 1.55, 0.35, 0.94, 0.86
]

# Find min and max values
min_value = min(defect_area_values)
max_value = max(defect_area_values)


# Normalize values
normalized_values = [normalize(value, min_value, max_value) for value in defect_area_values]

print(normalized_values)
