import json
import folium
from folium.plugins import GroupedLayerControl
from folium import Element

# Load JSON data
with open("locations.json") as f:
    locations = json.load(f)
with open("selected.json") as f:
    selected_projects = json.load(f)

# Fast lookup
selected_map = {
    f"{float(p['lat'])},{float(p['lon'])}": p 
    for p in selected_projects
}

# Base map
m = folium.Map(
    location=[12.9086641, 77.6341012],
    zoom_start=12,
    tiles=None
)

# Tiles
folium.TileLayer(
    tiles="CartoDB Voyager",
    name="CartoDB Voyager",
    overlay=False,
    control=False,
    show=True
).add_to(m)

# Layers
all_markers = folium.FeatureGroup(name="All Projects").add_to(m)
selected_markers = folium.FeatureGroup(name="Special Clients").add_to(m)

# All Projects
for lat_raw, lon_raw in locations:
    lat, lon = float(lat_raw), float(lon_raw)
    tooltip = "Tostem STUDIO, <br>Right Work Decor" if lat == 12.9086641 else None
    icon = folium.CustomIcon(
        icon_image='images/tostem.png' if lat == 12.9086641 else 'images/we.png',
        icon_size=(80, 50) if lat == 12.9086641 else (20, 30)
    )
    folium.Marker(
        [lat, lon], tooltip=tooltip, icon=icon
    ).add_to(all_markers)

# Selected Projects
for key, data in selected_map.items():
    lat, lon = map(float, key.split(","))

    # Carousel HTML inside popup (thumbnail view)
    image_carousel = "".join([
        f'<img src="{img}" style="width:250px; display:inline-block; margin-right:10px; border-radius:8px;">'
        for img in data['image']
    ])
    carousel_html = f"""
    <div style="overflow-x:auto; white-space:nowrap; padding-bottom:10px;">
    {image_carousel}
    </div>
    """

    # Fullscreen button
    button_html = f"""
    <button onclick='openPopupModal({json.dumps(data["name"])}, {json.dumps(data["position"])}, {json.dumps(data["image"])})'
        style="margin-top:10px; padding:6px 12px; font-size:14px;
        background:#1d4b7f; color:white; border:none; border-radius:4px; cursor:pointer;">
    View Full Screen
    </button>
    """

    # Combine popup HTML
    popup_html = f"""
    <div style="text-align:center; font-family:Georgia, serif">
    {carousel_html}
    <strong style="font-size:16px; color:#1d4b7f">{data['name']}</strong><br>
    <span style="font-size:14px; color:#555">{data['position']}</span><br>
    {button_html}
    </div>
    """

    icon = folium.CustomIcon(
        icon_image=data['image'][0] if lat == 12.9086641 else 'images/we.png',
        icon_size=(80, 50) if lat == 12.9086641 else (20, 30)
    )

    folium.Marker(
        [lat, lon], tooltip=data['name'],
        popup=folium.Popup(popup_html, max_width=300),
        icon=icon
    ).add_to(selected_markers)

# Layer control
GroupedLayerControl(
    groups={'Right Work Projects': [all_markers, selected_markers]},
    exclusive_groups=True,
    collapsed=False
).add_to(m)

# Modal HTML (single image carousel)
modal_html = """
<div id="customModal" style="display:none; position:fixed; top:0; left:0; width:100vw; height:100vh;
     background:rgba(0,0,0,0.7); z-index:9999; display:flex; justify-content:center; align-items:center; padding:20px; box-sizing:border-box;">
  <div style="background:white; padding:30px; border-radius:12px; width:100%; max-width:1000px;
       max-height:90vh; overflow:auto; position:relative; box-sizing:border-box;">
    
    <span onclick="document.getElementById('customModal').style.display='none'"
          style="position:absolute; top:15px; right:25px; font-size:28px; font-weight:bold; color:#333; cursor:pointer;">
      &times;
    </span>

    <div id="modalContent" style="text-align:center;"></div>

    <div style="text-align:center; margin-top:20px;">
      <button id="prevBtn" style="background:#1d4b7f; color:white; border:none; font-family:Georgia, serif; font-size:24px; 
        padding:10px 20px; border-radius:50%; margin-right:10px; cursor:pointer;">&#8249;</button>
      <button id="nextBtn" style="background:#1d4b7f; color:white; border:none; font-family:Georgia, serif; font-size:24px; 
        padding:10px 20px; border-radius:50%; margin-left:10px; cursor:pointer;">&#8250;</button>
    </div>
  </div>
</div>
"""


# Modal JS (single image with navigation)
modal_js = """
<script>
  let currentIndex = 0;
  let modalImages = [];

  function openPopupModal(name, position, images) {
    modalImages = images;
    currentIndex = 0;
    updateModalContent(name, position);
    document.getElementById('customModal').style.display = 'flex';
  }

  function updateModalContent(name, position) {
    let content = `
      <h2 style='margin:0 0 5px 0; color:#1d4b7f; font-family:Georgia, serif; font-size:28px;'>${name}</h2>
      <p style='margin:0 0 20px 0; color:#666; font-family:Georgia, serif; font-size:16px;'>${position}</p>
      <div style='display:flex; justify-content:center; align-items:center;'>
        <img src="${modalImages[currentIndex]}" style="max-width:90%; max-height:500px; border-radius:10px;" />
      </div>
    `;
    document.getElementById('modalContent').innerHTML = content;
  }

  document.getElementById("prevBtn").onclick = function() {
    if (modalImages.length > 0) {
      currentIndex = (currentIndex - 1 + modalImages.length) % modalImages.length;
      updateModalContent(currentName, currentPosition);
    }
  };

  document.getElementById("nextBtn").onclick = function() {
    if (modalImages.length > 0) {
      currentIndex = (currentIndex + 1) % modalImages.length;
      updateModalContent(currentName, currentPosition);
    }
  };

  // Maintain state across navigation
  let currentName = "";
  let currentPosition = "";
  function openPopupModal(name, position, images) {
    currentName = name;
    currentPosition = position;
    modalImages = images;
    currentIndex = 0;
    updateModalContent(name, position);
    document.getElementById('customModal').style.display = 'flex';
  }
</script>
"""

# Inject HTML and JS
m.get_root().html.add_child(Element(modal_html))
m.get_root().html.add_child(Element(modal_js))

# Save map
m.save("index.html")
