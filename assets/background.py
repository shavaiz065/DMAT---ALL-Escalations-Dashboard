import base64

# Base64 encoded background image with data analytics elements
# This is a lightweight SVG pattern with data analytics elements
background_image = """
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
  <defs>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#f0f0f0" stroke-width="1"/>
    </pattern>
    
    <!-- Data visualization elements -->
    <g id="chart-element">
      <rect x="0" y="15" width="5" height="10" fill="#4285F4" opacity="0.7"/>
      <rect x="7" y="10" width="5" height="15" fill="#4285F4" opacity="0.8"/>
      <rect x="14" y="5" width="5" height="20" fill="#4285F4" opacity="0.9"/>
      <rect x="21" y="12" width="5" height="13" fill="#4285F4" opacity="0.7"/>
      <rect x="28" y="8" width="5" height="17" fill="#4285F4" opacity="0.8"/>
    </g>
    
    <g id="pie-chart">
      <circle cx="15" cy="15" r="15" fill="#FFFFFF" stroke="#EEEEEE" stroke-width="1"/>
      <path d="M 15 15 L 15 0 A 15 15 0 0 1 30 15 Z" fill="#EA4335" opacity="0.7"/>
      <path d="M 15 15 L 30 15 A 15 15 0 0 1 15 30 Z" fill="#FBBC05" opacity="0.7"/>
      <path d="M 15 15 L 15 30 A 15 15 0 0 1 0 15 Z" fill="#34A853" opacity="0.7"/>
      <path d="M 15 15 L 0 15 A 15 15 0 0 1 15 0 Z" fill="#4285F4" opacity="0.7"/>
    </g>
    
    <g id="line-chart">
      <polyline points="0,15 10,5 20,10 30,2" fill="none" stroke="#34A853" stroke-width="2" opacity="0.7"/>
    </g>
    
    <g id="scatter-plot">
      <circle cx="5" cy="15" r="2" fill="#EA4335" opacity="0.7"/>
      <circle cx="12" cy="8" r="2" fill="#EA4335" opacity="0.7"/>
      <circle cx="18" cy="12" r="2" fill="#EA4335" opacity="0.7"/>
      <circle cx="25" cy="5" r="2" fill="#EA4335" opacity="0.7"/>
    </g>
  </defs>
  
  <!-- Background grid -->
  <rect width="100%" height="100%" fill="url(#grid)"/>
  
  <!-- Data visualization elements scattered around -->
  <use href="#chart-element" x="100" y="100" opacity="0.3"/>
  <use href="#chart-element" x="500" y="300" opacity="0.3"/>
  <use href="#chart-element" x="300" y="500" opacity="0.3"/>
  
  <use href="#pie-chart" x="200" y="200" opacity="0.3"/>
  <use href="#pie-chart" x="600" y="400" opacity="0.3"/>
  
  <use href="#line-chart" x="400" y="150" opacity="0.3"/>
  <use href="#line-chart" x="150" y="350" opacity="0.3"/>
  <use href="#line-chart" x="650" y="250" opacity="0.3"/>
  
  <use href="#scatter-plot" x="300" y="300" opacity="0.3"/>
  <use href="#scatter-plot" x="500" y="150" opacity="0.3"/>
  <use href="#scatter-plot" x="150" y="450" opacity="0.3"/>
</svg>
"""

def get_base64_encoded_image():
    """Convert the SVG to base64 encoding"""
    return base64.b64encode(background_image.encode()).decode()

def get_background_style():
    """Return CSS style with the background image"""
    encoded_image = get_base64_encoded_image()
    background_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/svg+xml;base64,{encoded_image}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    return background_style
