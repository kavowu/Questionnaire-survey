from PIL import Image
import math
import os

def remove_bg_smooth(input_path, output_path, tolerance=60):
    try:
        print(f"Processing: {input_path}")
        img = Image.open(input_path).convert("RGBA")
        datas = img.getdata()
        
        newData = []
        bg_color = (255, 255, 255) # Assuming white background
        
        for item in datas:
            # Calculate Euclidean distance from white
            # White is (255, 255, 255)
            # Distance ranges from 0 (white) to ~441 (black)
            
            r, g, b, a = item
            
            # Simple distance calc
            dist = math.sqrt((255-r)**2 + (255-g)**2 + (255-b)**2)
            
            if dist < tolerance:
                # If it's very close to white, make it transparent
                # But instead of hard 0, let's fade it out based on how white it is
                # This creates a smoother "anti-aliased" look
                
                # If dist is 0 (pure white) -> alpha 0
                # If dist is tolerance (edge) -> alpha 255
                
                # Make the fade curve steeper to avoid semi-transparent grey ghosting
                ratio = (dist / tolerance)
                
                # Power curve to make near-whites invisible faster
                alpha = int((ratio ** 2) * 255) 
                
                newData.append((r, g, b, alpha))
            else:
                newData.append(item)

        img.putdata(newData)
        img.save(output_path, "PNG")
        print(f"Saved optimized image to: {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")

input_file = os.path.join("image", "WETOPLOGO.png")
output_file = os.path.join("image", "WETOPLOGO_transparent.png") # Overwrite the old one

if os.path.exists(input_file):
    remove_bg_smooth(input_file, output_file)
else:
    print("Source image not found.")
