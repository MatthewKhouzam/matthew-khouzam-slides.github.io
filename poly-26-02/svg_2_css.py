import xml.etree.ElementTree as ET

def extract_fill_colors(svg_file):
    """Extracts unique fill colors from an SVG file."""
    fill_colors = set()
    try:
        tree = ET.parse(svg_file)
        root = tree.getroot()

        for element in root.iter():
            if 'fill' in element.attrib:
                fill_colors.add(element.attrib['fill'])
    except FileNotFoundError:
        print(f"Error: SVG file '{svg_file}' not found.")
        return None
    except ET.ParseError:
        print(f"Error: Could not parse SVG file '{svg_file}'.")
        return None
    return fill_colors

def generate_css(fill_colors, css_file="fills.css"):
    """Generates a CSS file with fill color classes."""
    if not fill_colors:
        print("No fill colors to generate CSS from.")
        return

    with open(css_file, "w") as f:
        for i, color in enumerate(fill_colors):
            class_name = f"fill-color-{i+1}"
            f.write(f".{class_name} {{\n")
            f.write(f"  fill: {color};\n")
            f.write("}\n\n")
    print(f"CSS file '{css_file}' created successfully.")

if __name__ == "__main__":
    svg_file = "theiacon.svg"  # Replace with your SVG file
    fill_colors = extract_fill_colors(svg_file)

    if fill_colors:
        generate_css(fill_colors)