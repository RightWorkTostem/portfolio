import json
import folium
from folium.plugins import GroupedLayerControl

# Load JSON
with open("locations.json") as f:
    locations = json.load(f)
with open("selected.json") as f:
    selected_projects = json.load(f)

# Build fast lookup
selected_map = {
    f"{float(p['lat'])},{float(p['lon'])}": p 
    for p in selected_projects
}

# Create base map WITHOUT automatic tiles control
m = folium.Map(
    location=[12.9086641, 77.6341012],
    zoom_start=12,
    tiles=None  
)

# Add only one TileLayer, hidden from control
folium.TileLayer(
    tiles="CartoDB Voyager",
    name="CartoDB Voyager",
    overlay=False,
    control=False,
    show=True
).add_to(m)

# Define layer groups
all_markers = folium.FeatureGroup(
    name="All Projects", overlay=True, control=True, show=True
).add_to(m)

selected_markers = folium.FeatureGroup(
    name="Special Clients", overlay=True, control=True, show=False
).add_to(m)

# Populate 'All Projects'
for lat_raw, lon_raw in locations:
    lat, lon = float(lat_raw), float(lon_raw)
    tooltip = (
        "Tostem STUDIO, <br>Right Work Decor"
        if lat == 12.9086641 else None
    )
    icon = folium.CustomIcon(
        icon_image='images/tostem.png' if lat == 12.9086641 else 'images/we.png',
        icon_size=(80, 50) if lat == 12.9086641 else (20, 30)
    )
    folium.Marker(
        [lat, lon], tooltip=tooltip, icon=icon
    ).add_to(all_markers)

# Populate 'Selected Projects'
for key, data in selected_map.items():
    lat, lon = map(float, key.split(","))
    popup_html = f"""
    <div style="text-align:center; padding:10px; font-family:Georgia, serif">
      <img src="{data['image']}" style="width:250px; border-radius:8px;
           box-shadow:0 2px 6px rgba(0,0,0,0.3)"><br>
      <strong style="font-size:16px; color:#1d4b7f">
        {data['name']}
      </strong><br>
      <span style="font-size:14px; color:#555">
        {data['position']}
      </span>
    </div>
    """
    icon = folium.CustomIcon(
        icon_image=data['image'] if lat == 12.9086641 else 'images/we.png',
        icon_size=(80, 50) if lat == 12.9086641 else (20, 30)
    )
    folium.Marker(
        [lat, lon], tooltip=data['name'],
        popup=folium.Popup(popup_html, max_width=250),
        icon=icon
    ).add_to(selected_markers)

# Add grouped control for exclusivity: mimics radio_buttons
GroupedLayerControl(
    groups={
        'Right Work Projects': [all_markers, selected_markers]
    },
    exclusive_groups=True,
    collapsed=False
).add_to(m)

# Save
m.save("portfolio.html")
