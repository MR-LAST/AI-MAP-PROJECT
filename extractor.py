from svgpathtools import svg2paths

# Load the SVG file
paths, attributes = svg2paths('map.svg')

# Extract coordinates for paths
for i, attr in enumerate(attributes):
    # Check if the element has an 'id' attribute (or another attribute you need)
    label = attr.get('id', None)  # If 'id' attribute exists, use it as the label
    
    # Get only elements that have segments (paths)
    path = paths[i]
    if len(path) > 0:
        x, y = path.point(0).real, path.point(0).imag
        print(f"{label}: ({x}, {y})")
    else:
        print(f"{label} has no path segments")
