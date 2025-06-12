import pandas as pd
import ast
import folium
from folium.plugins import HeatMap
from scipy.stats import gaussian_kde
import numpy as np

# Memuat dataset
file_path = r"C:\Users\Asus\OneDrive\Documents\Skripsi_Megi\kuliner_makassar.csv"
data = pd.read_csv(file_path)

# Ekstrak latitude dan longitude dari kolom 'Lokasi'
data['Lat'] = data['Lokasi'].apply(lambda x: ast.literal_eval(x)['lat'])
data['Lng'] = data['Lokasi'].apply(lambda x: ast.literal_eval(x)['lng'])

# Siapkan koordinat
coordinates = data[['Lat', 'Lng']].values

# Buat model KDE untuk estimasi kepadatan
kde = gaussian_kde(coordinates.T, bw_method=0.03)

# Buat grid untuk estimasi kepadatan
lat_min, lat_max = data['Lat'].min(), data['Lat'].max()
lng_min, lng_max = data['Lng'].min(), data['Lng'].max()

lat_values = np.linspace(lat_min, lat_max, 100)
lng_values = np.linspace(lng_min, lng_max, 100)
lat_grid, lng_grid = np.meshgrid(lat_values, lng_values)

# Evaluasi KDE pada grid
density = kde(np.vstack([lat_grid.ravel(), lng_grid.ravel()]))
density = density.reshape(lat_grid.shape)

# Normalisasi kepadatan untuk visualisasi yang lebih baik
density_normalized = (density - density.min()) / (density.max() - density.min())

# Buat peta Folium yang terpusat pada lokasi rata-rata
map_center = [data['Lat'].mean(), data['Lng'].mean()]
m = folium.Map(location=map_center, zoom_start=13)

# Buat FeatureGroup untuk HeatMap
heatmap_layer = folium.FeatureGroup(name='Heatmap')
heat_data = []

for lat, lng, d in zip(lat_grid.ravel(), lng_grid.ravel(), density_normalized.ravel()):
    if d > 0.01:   # Saring area dengan kepadatan sangat rendah
        heat_data.append([lat, lng, d])

HeatMap(heat_data, radius=20, blur=30, max_zoom=1, max_val=1.0).add_to(heatmap_layer)

# Buat FeatureGroup terpisah untuk kategori rating
rating_below_4_layer = folium.FeatureGroup(name='Rating < 4')
rating_4_to_5_layer = folium.FeatureGroup(name='Rating 4-5')

# Iterasi data dan tambahkan titik ke layer yang sesuai
for _, row in data.iterrows():
    popup_content = f"""
    <b>Nama:</b> {row['Nama']}<br>
    <b>Alamat:</b> {row['Alamat']}<br>
    <b>Rating:</b> {row['Rating']}<br>
    <b>Place ID:</b> {row['Place ID']}<br>
    <b>Lokasi:</b> {row['Lat']}, {row['Lng']}
    """
    marker = folium.Marker(
        location=[row['Lat'], row['Lng']],
        popup=folium.Popup(popup_content, max_width=300),
        tooltip=row['Nama']
    )
    if row['Rating'] < 4:
        marker.add_to(rating_below_4_layer)
    elif 4 <= row['Rating'] <= 5:
        marker.add_to(rating_4_to_5_layer)

# Tambahkan semua layer ke dalam peta
heatmap_layer.add_to(m)
rating_below_4_layer.add_to(m)
rating_4_to_5_layer.add_to(m)

# Tambahkan kontrol layer untuk mengatur tampilan layer
folium.LayerControl(collapsed=False).add_to(m)

# Simpan peta ke dalam file HTML
m.save("interactive_hotspot_map_with_ratings_combined_1.html")

print("Map saved as 'interactive_hotspot_map_with_ratings_combined_1.html'. Open this file in your browser to view the result.")
