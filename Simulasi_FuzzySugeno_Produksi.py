import streamlit as st

st.set_page_config(page_title="Dashboard Produksi", layout="centered")
st.title("Estimasi Jumlah Produksi")
st.markdown("Simulasi Fuzzy Sugeno estimasi jumlah produki berdasarkan suhu, pencahayaan, dan kebisingan.")

#suhu = 20
#pencahayaan = 400
#kebisingan = 55

#Input
suhu = st.slider("Suhu (°C)", 18, 38, 25)
pencahayaan = st.slider("Pencahayaan (lux)", 0, 700, 350)
kebisingan = st.slider("Kebisingan (dB)", 35, 105, 65)

def data_suhu(x):
    # Rendah
    if 18 <= x <= 22: rendah = (x - 18.0) / 4.0
    elif 22< x <= 26: rendah = (26.0 - x) / 4.0
    else: rendah = 0

    # Normal
    if 22 <= x <= 26: normal = (x - 22.0) / 4.0 
    elif 26 < x <= 32: normal = (32.0 - x) / 6.0
    else: normal = 0 

    # Tinggi
    if 26 <= x <= 32: tinggi = (x - 26.0) / 6.0
    elif 32 < x <= 38: tinggi = (38.0 - x) / 6.0 
    else: tinggi = 0 

    return {'Rendah': rendah, 'Normal': normal, 'Tinggi': tinggi}

def data_kebisingan(x):
    # Tenang
    if 35 <= x <= 55: tenang = (x - 35.0) / 20.0    
    elif 55 < x <= 75: tenang = (75.0 - x) / 20.0
    else: tenang = 0

    # Agak Bising
    if 55 <= x <= 75: agak_bising = (x - 55.0) / 20.0
    elif 75 < x <= 90: agak_bising = (90.0 - x) / 15.0
    else: agak_bising = 0

    # Bising
    if 75 <= x <= 90: bising = (x - 75.0) / 15.0
    elif 90 < x <= 105: bising = (105.0 - x) / 15.0
    else: bising = 0

    return {'Tenang': tenang, 'Agak Bising': agak_bising, 'Bising': bising}

def data_pencahayaan(x):
    # Redup
    if 0 <= x <= 150: redup = x / 150.0
    elif 150 < x <= 300: redup = (300 - x) / 150.0
    else: redup = 0

    # Agak Terang
    if 150 <= x <= 350: agak_terang = (x - 150.0) / 150.0
    elif 350 < x <= 500: agak_terang = (500.0 - x) / 200.0
    else: agak_terang = 0 

    # Terang
    if 300 <= x <= 500: terang = (x - 300.0) / 200.0
    elif 500 < x <= 700: terang = (700.0 - x) / 200.0
    else: terang = 0 

    return {'Redup': redup, 'Agak Terang': agak_terang, 'Terang': terang}
    
nilai_suhu = data_suhu(suhu)
nilai_pencahayaan = data_pencahayaan(pencahayaan)
nilai_kebisingan = data_kebisingan(kebisingan)

from itertools import product
produksi_rules = {
    ('Rendah', 'Redup', 'Tenang'): 148.0,
    ('Rendah', 'Agak Terang', 'Tenang'): 150.9,
    ('Rendah', 'Terang', 'Tenang'): 146.5,
    ('Rendah', 'Redup', 'Agak Bising'): 143.1,
    ('Rendah', 'Agak Terang', 'Agak Bising'): 146.53,
    ('Rendah', 'Terang', 'Agak Bising'): 142.73,
    ('Rendah', 'Redup', 'Bising'): 136.73,
    ('Rendah', 'Agak Terang', 'Bising'): 140.77,
    ('Rendah', 'Terang', 'Bising'): 135.97,
    ('Normal', 'Redup', 'Tenang'): 149.73,
    ('Normal', 'Agak Terang', 'Tenang'): 153.27,
    ('Normal', 'Terang', 'Tenang'): 152.13,
    ('Normal', 'Redup', 'Agak Bising'): 148,
    ('Normal', 'Agak Terang', 'Agak Bising'): 150.63,
    ('Normal', 'Terang', 'Agak Bising'): 147.63,
    ('Normal', 'Redup', 'Bising'): 141.47,
    ('Normal', 'Agak Terang', 'Bising'): 145.67,
    ('Normal', 'Terang', 'Bising'): 140.2,
    ('Tinggi', 'Redup', 'Tenang'): 142.10,
    ('Tinggi', 'Agak Terang', 'Tenang'): 146.53,
    ('Tinggi', 'Terang', 'Tenang'): 142.17,
    ('Tinggi', 'Redup', 'Agak Bising'): 138.7,
    ('Tinggi', 'Agak Terang', 'Agak Bising'): 141.4,
    ('Tinggi', 'Terang', 'Agak Bising'): 138.3,
    ('Tinggi', 'Redup', 'Bising'): 133.33,
    ('Tinggi', 'Agak Terang', 'Bising'): 138.33,
    ('Tinggi', 'Terang', 'Bising'): 133.77,
}

def compute_output():
    temp1 = 0
    temp2 = 0
    for s, p, k in product(nilai_suhu.keys(), nilai_pencahayaan.keys(), nilai_kebisingan.keys()):
        hasil = nilai_suhu[s] * nilai_pencahayaan[p] * nilai_kebisingan[k]
        jumlah = produksi_rules.get((s, p, k), 140)  #default skor
        temp1 += hasil * jumlah
        temp2 += hasil
    return temp1 / temp2 if temp2 != 0 else 0

produksi = round(compute_output(), 2)

kenyamanan_rules = {
    # Format: ('Suhu', 'Pencahayaan', 'Kebisingan'): Skor kenyamanan 0-100
    ('Rendah', 'Redup', 'Tenang'): 65,
    ('Rendah', 'Redup', 'Agak Bising'): 60,
    ('Rendah', 'Redup', 'Bising'): 35,
    ('Rendah', 'Agak Terang', 'Tenang'): 70,
    ('Rendah', 'Agak Terang', 'Agak Bising'): 65,
    ('Rendah', 'Agak Terang', 'Bising'): 40,
    ('Rendah', 'Terang', 'Tenang'): 68,
    ('Rendah', 'Terang', 'Agak Bising'): 60,
    ('Rendah', 'Terang', 'Bising'): 38,
    ('Normal', 'Redup', 'Tenang'): 75,
    ('Normal', 'Redup', 'Agak Bising'): 65,
    ('Normal', 'Redup', 'Bising'): 40,
    ('Normal', 'Agak Terang', 'Tenang'): 85,
    ('Normal', 'Agak Terang', 'Agak Bising'): 80,
    ('Normal', 'Agak Terang', 'Bising'): 45,
    ('Normal', 'Terang', 'Tenang'): 88,
    ('Normal', 'Terang', 'Agak Bising'): 80,
    ('Normal', 'Terang', 'Bising'): 50,
    ('Tinggi', 'Redup', 'Tenang'): 40,
    ('Tinggi', 'Redup', 'Agak Bising'): 35,
    ('Tinggi', 'Redup', 'Bising'): 30,
    ('Tinggi', 'Agak Terang', 'Tenang'): 45,
    ('Tinggi', 'Agak Terang', 'Agak Bising'): 40,
    ('Tinggi', 'Agak Terang', 'Bising'): 30,
    ('Tinggi', 'Terang', 'Tenang'): 50,
    ('Tinggi', 'Terang', 'Agak Bising'): 45,
    ('Tinggi', 'Terang', 'Bising'): 30,
}

def compute_kenyamanan():
    temp1 = 0
    temp2 = 0
    for s, p, k in product(nilai_suhu.keys(), nilai_pencahayaan.keys(), nilai_kebisingan.keys()):
        derajat = nilai_suhu[s] * nilai_pencahayaan[p] * nilai_kebisingan[k]
        score = kenyamanan_rules.get((s, p, k), 50)  # default skor 50
        temp1 += derajat * score
        temp2 += derajat
    return temp1 / temp2 if temp2 != 0 else 0
    
kenyamanan = round(compute_kenyamanan(), 2)

hasil_suhu = max(nilai_suhu, key=nilai_suhu.get)
hasil_pencahayaan = max(nilai_pencahayaan, key=nilai_pencahayaan.get)
hasil_kebisingan = max(nilai_kebisingan, key=nilai_kebisingan.get)

#Show output

st.markdown("---")
st.subheader("Hasil Produksi")
st.metric(label="Jumlah Estimasi", value=f"{produksi} unit")

st.markdown("---")
st.subheader("Hasil Parameter")
st.write(f"**Suhu ({suhu}°C):** {hasil_suhu}")
st.write(f"**Pencahayaan ({pencahayaan} lux):** {hasil_pencahayaan}")
st.write(f"**Kebisingan ({kebisingan} dB):** {hasil_kebisingan}")

st.markdown("---")
st.subheader("Simulasi Kenyamanan Ruangan")
st.metric(label="Skor Kenyamanan", value=f"{kenyamanan}")

if kenyamanan >= 80:
    st.success("Kondisi sangat nyaman 😊")
elif kenyamanan >= 60:
    st.info("Kondisi cukup nyaman 😌")
elif kenyamanan >= 40:
    st.warning("Kondisi kurang nyaman 😕")
else:
    st.error("Kondisi tidak nyaman 😢")

st.markdown("---")
st.subheader("Perhitungan Nilai")
st.write(f"**Suhu ({suhu}°C):** {nilai_suhu}")
st.write(f"**Pencahayaan ({pencahayaan} lux):** {nilai_pencahayaan}")
st.write(f"**Kebisingan ({kebisingan} dB):** {nilai_kebisingan}")

st.markdown("---")
st.markdown("P31.2024.02644 - Muhammad Budi Hartanto")
