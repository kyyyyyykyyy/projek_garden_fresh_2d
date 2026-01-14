<div align="center">

# 🌱 GARDEN FRESH: FARMING SIMULATOR

<img src="assets/image/background_menu.png" alt="Garden Fresh Banner" width="100%" style="border-radius: 10px; box-shadow: 0px 0px 20px rgba(100,255,100,0.3);">

<br><br>

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Engine-Pygame-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Genre](https://img.shields.io/badge/Genre-Simulation_Strategy-green?style=for-the-badge)

<br>
   
**"Tanam, Rawat, Panen, Cuan!"**
<br>
Simulasi pertanian santai dengan siklus pertumbuhan tanaman *real-time* dan sistem ekonomi sederhana.

[View Features](#-key-features) • [Technical Review](#-technical-retrospective) • [Installation](#-installation)

</div>

---

## 🌻 About The Game

**Garden Fresh** adalah game simulasi pertanian yang menekankan pada manajemen waktu dan *resource*. Pemain mengelola lahan pertanian luas yang melebihi ukuran layar, memaksa pemain untuk melakukan navigasi (*panning*) untuk memantau seluruh tanaman.

Berbeda dengan game sebelumnya, proyek ini fokus pada **State Management** dimana setiap tanaman memiliki timer dan status pertumbuhannya sendiri secara independen.

---

## ✨ Key Features

### 🌾 Real-time Growth System (3 Tahap)
Tanaman memiliki siklus hidup yang berjalan berdasarkan waktu nyata:
1.  **Bibit (Seed):** Tahap awal (0 - 15 detik).
2.  **Medium:** Setengah matang (15 - 30 detik).
3.  **Full Harvest:** Siap panen (30+ detik).

### 📷 Dynamic Camera System
Dunia game lebih besar dari layar monitor. Menggunakan sistem kamera **Drag & Drop** (Mouse Motion) untuk menggeser pandangan ke seluruh kebun.

### 💰 Economy & Logic
* **Harvest Logic:** Tanaman hanya bisa dipanen saat statusnya "Full". Panen saat masih bibit tidak akan menghasilkan uang.
* **Auto-Replant:** Setelah panen, tanah otomatis ditanami kembali untuk memulai siklus investasi baru.

### 🎨 Mathematical Animations
* **Wavy Text:** Judul game bergerak bergelombang menggunakan fungsi Trigonometri (`math.sin`).
* **Pulsing UI:** Tombol dan border berdenyut halus untuk menarik perhatian pemain.

---

## 🧐 Technical Retrospective

*Bagian ini menjelaskan analisis teknis terhadap kode yang dibangun (Kelebihan & Kekurangan).*

### ✅ Kelebihan (Strengths)
1.  **Independent Object States:** Menggunakan *List of Dictionaries* untuk menyimpan data 100+ tanaman. Setiap tanaman punya "otak" sendiri untuk tahu kapan dia harus tumbuh.
2.  **World vs Screen Coordinates:** Implementasi logika kamera yang memisahkan posisi asli objek di dunia (*World Position*) dengan posisi gambarnya di layar (*Screen Position*).
3.  **Asset Safety:** Dilengkapi dengan `try-except` block yang kuat. Game tidak akan crash total jika ada gambar yang hilang, melainkan memberikan pesan error yang jelas.

### ⚠️ Kekurangan (Areas for Improvement)
1.  **Hardcoded Timers:** Waktu tumbuh tanaman (15s & 30s) masih ditulis statis di dalam kode. *Next update: Pindahkan ke file konfigurasi JSON agar mudah di-balancing.*
2.  **Rendering Optimization:** Saat ini game me-render (menggambar) seluruh tanaman meskipun tanaman tersebut berada di luar layar kamera. *Next update: Implementasi "Culling" agar hanya menggambar objek yang terlihat kamera untuk performa lebih ringan.*
3.  **Monolithic Script:** Seluruh logika (Aset, Game Loop, UI) masih dalam satu file `main.py`. *Next update: Pecah menjadi modul terpisah (MVC Pattern).*

---

## 🛠️ Tools Used

* **Language:** Python 3.10+
* **Game Engine:** Pygame (SDL Wrapper)
* **Asset Creation:** Photoshop / Canva (for sprites)
* **Version Control:** Git & GitHub

---

## 🕹 Controls

| Input | Aksi |
| :---: | :--- |
| **Mouse Drag (Tahan Klik Kiri)** | Menggeser Kamera (Panning) |
| **Mouse Click (Klik Kiri)** | Memanen Tanaman (Saat Siap) |
| **Mouse Hover** | Interaksi UI Tombol |

---

## 💻 Installation

1.  **Clone Repository**
    ```bash
    git clone [https://github.com/kyyyyykyyy/garden-fresh.git](https://github.com/kyyyyykyyy/garden-fresh.git)
    ```

2.  **Masuk ke Folder**
    ```bash
    cd garden-fresh
    ```

3.  **Install Pygame**
    ```bash
    pip install pygame
    ```

4.  **Jalankan Petani Virtual**
    ```bash
    python main.py
    ```

---

<div align="center">
  
  ### 👨‍💻 Developed by **Muhamad Adzky Maulana**
  
  <a href="https://github.com/kyyyyykyyy">
    <img src="https://img.shields.io/badge/GitHub-kyyyyykyyy-181717?style=for-the-badge&logo=github" alt="GitHub">
  </a>
  
  <p>Aceh, Indonesia</p>
  
</div>
