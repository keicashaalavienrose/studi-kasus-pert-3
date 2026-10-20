# ==========================================
# STUDI KASUS 3: Otomasi Analisis Aset Spasial Perkotaan
# Berdasarkan Materi Praktisi GIS (Bapak Widi Primadeva - New Zealand)
# ==========================================

import numpy as np
import pandas as pd

print("--- Memulai Analisis Spasial Aset Infrastruktur Kota ---")

# 1. Inisialisasi Data Dummy Titik Aset Publik (Taman, Lampu Jalan, Fasilitas Air)
np.random.seed(42)
n_assets = 150

asset_data = pd.DataFrame({
    'asset_id': [f"AST-{i:03d}" for i in range(1, n_assets + 1)],
    'category': np.random.choice(['Taman Kota', 'Lampu Jalan', 'Fasilitas Air', 'Halte'], size=n_assets),
    'coord_x': np.random.uniform(95.0, 96.5, size=n_assets), # Simulasi koordinat bujur (longitude)
    'coord_y': np.random.uniform(-4.0, -3.0, size=n_assets),  # Simulasi koordinat lintang (latitude)
    'urgency_score': np.random.randint(1, 6, size=n_assets)   # Skala prioritas perbaikan (1-5)
})

# 2. Koordinat Pusat Kendali Operasional (Control Center)
center_x = 95.75
center_y = -3.50

# 3. Fungsi Analisis Jarak Euclidean & Penentuan Zona Prioritas Perbaikan
def analyze_asset_distribution(df):
    # Hitung jarak Euclidean dari pusat kendali
    df['distance_to_center_km'] = np.sqrt(
        (df['coord_x'] - center_x)**2 + (df['coord_y'] - center_y)**2
    ) * 111 # Konversi kasar derajat ke kilometer
    
    # Klasifikasi Status Penanganan Berdasarkan Jarak & Urgensi
    conditions = [
        (df['distance_to_center_km'] <= 30) & (df['urgency_score >= 4']),
        (df['distance_to_center_km'] <= 30),
        (df['distance_to_center_km'] > 30)
    ]
    choices = ['Prioritas Tinggi (Zona 1)', 'Pemeliharaan Rutin (Zona 1)', 'Pemeliharaan Berkala (Zona 2)']
    df['maintenance_status'] = np.select(conditions, choices, default='Evaluasi Lanjutan')
    
    return df

# Jalankan fungsi analisis
processed_assets = analyze_asset_distribution(asset_data)

print("\n--- 5 Data Teratas Hasil Analisis Aset Spasial ---")
print(processed_assets[['asset_id', 'category', 'distance_to_center_km', 'urgency_score', 'maintenance_status']].head())

# 4. Agregasi Ringkasan Laporan untuk Manajemen
print("\n--- Ringkasan Total Aset Berdasarkan Status Pemeliharaan ---")
summary_report = processed_assets.groupby('maintenance_status')['asset_id'].count().reset_index()
summary_report.columns = ['Status Pemeliharaan', 'Jumlah Aset']
print(summary_report)

# 5. Ekspor Hasil Analisis Otomatis untuk Dashboard Cloud
processed_assets.to_csv('urban_asset_report.csv', index=False)
print("\n[SUKSES] Laporan berhasil diekspor ke 'urban_asset_report.csv' untuk sinkronisasi sistem cloud.")