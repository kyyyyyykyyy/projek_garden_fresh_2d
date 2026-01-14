import pygame
import os
import random
import math

# --- 1. Inisialisasi Pygame dan Pengaturan Awal ---
pygame.init()
pygame.font.init()

# Pengaturan ukuran layar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Garden Fresh (3 Tahap Tumbuh Version)")

# Pengaturan FPS
clock = pygame.time.Clock()

# Definisi Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN_TITLE = (20, 150, 20)
BUTTON_BG = (10, 10, 10, 180)
BUTTON_BORDER_START = (100, 255, 100)
BUTTON_BORDER_END = (255, 255, 150)
PLAY_TEXT_COLOR = (255, 255, 220)

# --- 2. Memuat Aset ---
try:
    # Path
    script_dir = os.path.dirname(__file__)
    ASSET_DIR = os.path.join(script_dir, "assets")
    IMAGE_DIR = os.path.join(ASSET_DIR, "image")
    FONT_DIR = os.path.join(ASSET_DIR, "font")

    # Muat Aset Menu
    BG_MENU = pygame.image.load(os.path.join(IMAGE_DIR, "background_menu.png")).convert_alpha()
    BG_MENU = pygame.transform.scale(BG_MENU, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Latar Game (BG_GAME Lama)
    BG_GAME = pygame.image.load(os.path.join(IMAGE_DIR, "background_game.png")).convert_alpha()
    WORLD_WIDTH_PX = BG_GAME.get_width()
    WORLD_HEIGHT_PX = BG_GAME.get_height()
    
    # === ASET BARU: 3 TAHAP TUMBUH ===
    BIBIT_IMG = pygame.image.load(os.path.join(IMAGE_DIR, "bibit.png")).convert_alpha()
    BIBIT_IMG = pygame.transform.scale(BIBIT_IMG, (40, 40))
    
    TANAMAN_MEDIUM_IMG = pygame.image.load(os.path.join(IMAGE_DIR, "tanaman_medium.png")).convert_alpha()
    TANAMAN_MEDIUM_IMG = pygame.transform.scale(TANAMAN_MEDIUM_IMG, (40, 40))
    
    TANAMAN_FULL_IMG = pygame.image.load(os.path.join(IMAGE_DIR, "tanaman_full.png")).convert_alpha()
    TANAMAN_FULL_IMG = pygame.transform.scale(TANAMAN_FULL_IMG, (40, 40))
    
    PLANT_WIDTH = BIBIT_IMG.get_width()
    PLANT_HEIGHT = BIBIT_IMG.get_height()

    # Kupu-kupu (Opsional)
    try:
        BUTTERFLY_IMG = pygame.image.load(os.path.join(IMAGE_DIR, "butterfly.png")).convert_alpha()
        BUTTERFLY_IMG = pygame.transform.scale(BUTTERFLY_IMG, (30, 30))
        HAS_BUTTERFLY = True
    except FileNotFoundError:
        HAS_BUTTERFLY = False

    # Font
    FONT_PATH = os.path.join(FONT_DIR, "custom_font.ttf")
    FONT_TITLE = pygame.font.Font(FONT_PATH, 70)
    FONT_UI = pygame.font.Font(FONT_PATH, 40)
    FONT_PLAY_BASE = pygame.font.Font(FONT_PATH, 50) 

except pygame.error as e:
    print(f"Error: Tidak bisa memuat aset: {e}")
    print("PASTIKAN 'bibit.png', 'tanaman_medium.png', dan 'tanaman_full.png' ADA DI FOLDER 'assets/image/'!")
    pygame.quit()
    exit()

# --- 3. Variabel Game ---
current_screen = "menu"
uang = 0
game_start_time = 0

# Variabel Kamera (Klik & Geser)
camera_x = (WORLD_WIDTH_PX - SCREEN_WIDTH) // 2
camera_y = (WORLD_HEIGHT_PX - SCREEN_HEIGHT) // 2
is_dragging = False
has_dragged_this_click = False
drag_start_pos = (0, 0)
drag_start_camera = (0, 0)

# === LOGIKA BARU: 4 PETAK PERSEGI DI BAWAH ===
plants = [] # Daftar ini akan diisi NANTI saat game dimulai

# Pengaturan Petak
PATCH_ROWS = 5 # 5 baris tanaman per petak
PATCH_COLS = 5 # 5 kolom tanaman per petak
PLANT_SPACING_X = 50 # Jarak antar tanaman
PLANT_SPACING_Y = 50
NUM_PATCHES = 4 # 4 petak
PATCH_SPACING = 300 # Jarak antar petak

# --- 4. Variabel Animasi (Menu & Bintang Jatuh) ---
clickable_play_button_rect = pygame.Rect(0, 0, 0, 0)

# Kupu-kupu Mengelilingi Judul
butterflies = []
if HAS_BUTTERFLY:
    num_butterflies = 3
    for i in range(num_butterflies):
        start_angle = random.uniform(0, 2 * math.pi)
        butterflies.append({
            "angle": start_angle, "radius": 100 + (i * 20),
            "speed": random.uniform(0.005, 0.01),
            "flutter_phase": random.uniform(0, 2 * math.pi),
            "flutter_magnitude": random.uniform(1, 3)
        })

# Bintang Jatuh
stars = []
def get_random_color():
    return (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255))
for _ in range(50):
    stars.append([
        random.randint(0, WORLD_WIDTH_PX), random.randint(0, WORLD_HEIGHT_PX),
        random.uniform(2, 5), random.randint(1, 2), get_random_color()
    ])

# Fungsi 'mencampur' warna
def lerp_color(color1, color2, t):
    r = int(color1[0] + (color2[0] - color1[0]) * t)
    g = int(color1[1] + (color2[1] - color1[1]) * t)
    b = int(color1[2] + (color2[2] - color1[2]) * t)
    return (r, g, b)

# Fungsi Teks Bergelombang
def draw_wavy_text(surface, text_to_draw, font, base_x_center, base_y_center, time, color):
    total_width = 0
    letter_surfaces = []
    for char in text_to_draw:
        letter_surface = font.render(char, True, color)
        letter_surfaces.append(letter_surface)
        total_width += letter_surface.get_width()
    current_x = base_x_center - (total_width / 2)
    
    wave_speed = 0.005; wave_length = 0.8; wave_height = 8
    
    for i, letter_surface in enumerate(letter_surfaces):
        y_offset = math.sin((time * wave_speed) + (i * wave_length)) * wave_height
        surface.blit(letter_surface, (current_x, base_y_center + y_offset))
        current_x += letter_surface.get_width()

# --- 5. Fungsi Game Baru ---
def start_game():
    """Mengatur ulang dan memulai game."""
    global current_screen, game_start_time, plants, uang
    
    current_screen = "game"
    game_start_time = pygame.time.get_ticks()
    uang = 0
    plants = [] 

    # Hitung total lebar & tinggi petak
    patch_width_px = (PATCH_COLS - 1) * PLANT_SPACING_X
    
    # Hitung total lebar semua petak (4 petak + 3 jarak)
    total_patches_width = (NUM_PATCHES * patch_width_px) + ((NUM_PATCHES - 1) * PATCH_SPACING)
    
    # Tentukan posisi X awal untuk petak pertama (biar rata tengah)
    PATCH_START_X = (WORLD_WIDTH_PX - total_patches_width) // 2
    # Tentukan posisi Y (di bagian bawah)
    PATCH_START_Y = WORLD_HEIGHT_PX - (PATCH_ROWS * PLANT_SPACING_Y) - 50 

    # Buat 4 petak persegi
    for patch_index in range(NUM_PATCHES):
        # Hitung X offset untuk petak ini
        patch_offset_x = patch_index * (patch_width_px + PATCH_SPACING)
        
        for row in range(PATCH_ROWS):
            for col in range(PATCH_COLS):
                plant_x = PATCH_START_X + patch_offset_x + (col * PLANT_SPACING_X)
                plant_y = PATCH_START_Y + (row * PLANT_SPACING_Y)
                
                # === LOGIKA BARU: 3 TAHAP TUMBUH (Total 30 detik) ===
                plants.append({
                    "rect": pygame.Rect(plant_x, plant_y, PLANT_WIDTH, PLANT_HEIGHT),
                    "state": "bibit", # Mulai sebagai bibit
                    "grow_time_medium": game_start_time + 15000, # Tumbuh medium 15 detik
                    "grow_time_full": game_start_time + 30000   # Tumbuh full 30 detik
                })


# --- 6. Game Loop Utama ---
running = True
while running:
    
    current_time = pygame.time.get_ticks()
    mouse_pos = pygame.mouse.get_pos()
    
    pulse = (math.sin(current_time * 0.005) + 1) / 2 

    # --- 7. Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if current_screen == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    if clickable_play_button_rect.collidepoint(event.pos):
                        start_game() # Panggil fungsi start_game
        
        elif current_screen == "game":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    is_dragging = True
                    has_dragged_this_click = False 
                    drag_start_pos = mouse_pos
                    drag_start_camera = (camera_x, camera_y)
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: 
                    is_dragging = False
                    
                    if not has_dragged_this_click:
                        # === LOGIKA PANEN (HANYA JIKA SUDAH FULL) ===
                        mouse_pos_dunia = (mouse_pos[0] + camera_x, mouse_pos[1] + camera_y)
                        
                        for plant in reversed(plants):
                            if plant["rect"].collidepoint(mouse_pos_dunia):
                                if plant["state"] == "full":
                                    uang += 10
                                    print(f"Tanaman dipanen! Uang sekarang: ${uang}")
                                    # === KEMBALI JADI BIBIT (SIKLUS BARU) ===
                                    plant["state"] = "bibit"
                                    plant["grow_time_medium"] = current_time + 15000
                                    plant["grow_time_full"] = current_time + 30000
                                elif plant["state"] == "medium":
                                    print("Masih setengah matang!")
                                else:
                                    print("Masih bibit, belum bisa panen!")
                                break 
            
            if event.type == pygame.MOUSEMOTION:
                if is_dragging:
                    has_dragged_this_click = True
                    
                    dx = mouse_pos[0] - drag_start_pos[0]
                    dy = mouse_pos[1] - drag_start_pos[1]
                    
                    camera_x = drag_start_camera[0] - dx
                    camera_y = drag_start_camera[1] - dy

                    if camera_x < 0: camera_x = 0
                    if camera_x > WORLD_WIDTH_PX - SCREEN_WIDTH: camera_x = WORLD_WIDTH_PX - SCREEN_WIDTH
                    if camera_y < 0: camera_y = 0
                    if camera_y > WORLD_HEIGHT_PX - SCREEN_HEIGHT: camera_y = WORLD_HEIGHT_PX - SCREEN_HEIGHT

    # --- 8. Logika Update (Animasi & Tumbuh) ---
    
    if current_screen == "menu":
        # === ANIMASI KUPU-KUPU MENGELILINGI JUDUL ===
        if HAS_BUTTERFLY:
            title_center_x = SCREEN_WIDTH // 2
            title_center_y = SCREEN_HEIGHT // 2 - 100 
            for bf in butterflies:
                bf["angle"] += bf["speed"] 
                
                bf_x = title_center_x + math.cos(bf["angle"]) * bf["radius"]
                bf_y = title_center_y + math.sin(bf["angle"]) * bf["radius"] \
                       + math.sin(current_time * bf["flutter_phase"] * 0.01) * bf["flutter_magnitude"]
                
                bf["pos"] = [bf_x, bf_y]

    elif current_screen == "game":
        # === UPDATE BINTANG JATUH ===
        for star in stars:
            star[1] += star[2]
            if star[1] > camera_y + SCREEN_HEIGHT + 20: 
                star[0] = random.randint(camera_x, camera_x + SCREEN_WIDTH)
                star[1] = camera_y - 20
                star[4] = get_random_color()
        
        # === FULL SISTEM: LOGIKA 3 TAHAP TUMBUH ===
        for plant in plants:
            if plant["state"] == "bibit":
                if current_time > plant["grow_time_medium"]:
                    plant["state"] = "medium" # Tumbuh ke tahap 2
            elif plant["state"] == "medium":
                if current_time > plant["grow_time_full"]:
                    plant["state"] = "full" # Tumbuh ke tahap 3 (Siap Panen)


    # --- 9. Render (Menggambar ke Layar) ---
    
    SCREEN.fill(BLACK)

    if current_screen == "menu":
        SCREEN.blit(BG_MENU, (0, 0))
        
        # Judul Bergelombang
        draw_wavy_text(SCREEN, "GARDEN FRESH", FONT_TITLE, (SCREEN_WIDTH // 2) + 4, (SCREEN_HEIGHT // 2 - 100) + 4, current_time, BLACK)
        draw_wavy_text(SCREEN, "GARDEN FRESH", FONT_TITLE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100, current_time, GREEN_TITLE)

        # Kupu-kupu
        if HAS_BUTTERFLY:
            for bf in butterflies:
                rotation_angle = math.degrees(bf["angle"])
                rotated_butterfly = pygame.transform.rotate(BUTTERFLY_IMG, -rotation_angle - 90)
                rotated_rect = rotated_butterfly.get_rect(center=bf["pos"])
                SCREEN.blit(rotated_butterfly, rotated_rect.topleft)
        
        # Tombol "PLAY" Kustom
        scale = 1.0 + (pulse * 0.1)
        current_font_size = int(50 * scale)
        FONT_PLAY_DYNAMIC = pygame.font.Font(FONT_PATH, current_font_size)
        
        play_text = FONT_PLAY_DYNAMIC.render("PLAY", True, PLAY_TEXT_COLOR)
        play_text_rect = play_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        
        button_container_rect = play_text_rect.inflate(40, 20) 
        pulsing_border_color = lerp_color(BUTTON_BORDER_START, BUTTON_BORDER_END, pulse)
        
        s = pygame.Surface((button_container_rect.width, button_container_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(s, BUTTON_BG, s.get_rect(), border_radius=15)
        SCREEN.blit(s, button_container_rect.topleft)
        
        pygame.draw.rect(SCREEN, pulsing_border_color, button_container_rect, width=4, border_radius=15)
        SCREEN.blit(play_text, play_text_rect)
        
        clickable_play_button_rect = button_container_rect

    elif current_screen == "game":
        # Render BG_GAME
        SCREEN.blit(BG_GAME, (0, 0), (camera_x, camera_y, SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Render Bintang Jatuh
        for star in stars:
            screen_x = star[0] - camera_x
            screen_y = star[1] - camera_y
            if 0 < screen_x < SCREEN_WIDTH and 0 < screen_y < SCREEN_HEIGHT:
                 pygame.draw.circle(SCREEN, star[4], (screen_x, screen_y), star[3])
                 
        # === RENDER 4 PETAK TANAMAN (3 TAHAP) ===
        for plant in plants:
            screen_x = plant["rect"].x - camera_x
            screen_y = plant["rect"].y - camera_y
            
            if -PLANT_WIDTH < screen_x < SCREEN_WIDTH and -PLANT_HEIGHT < screen_y < SCREEN_HEIGHT:
                # Cek status untuk gambar yang benar!
                if plant["state"] == "bibit":
                    SCREEN.blit(BIBIT_IMG, (screen_x, screen_y))
                elif plant["state"] == "medium":
                    SCREEN.blit(TANAMAN_MEDIUM_IMG, (screen_x, screen_y))
                else: # Berarti state == "full"
                    SCREEN.blit(TANAMAN_FULL_IMG, (screen_x, screen_y))

        # Render UI (Uang)
        ui_text = FONT_UI.render(f"UANG: ${uang}", True, GREEN_TITLE)
        ui_bg_rect = pygame.Rect(5, 5, ui_text.get_width() + 10, ui_text.get_height() + 10)
        pygame.draw.rect(SCREEN, (0,0,0, 180), ui_bg_rect)
        SCREEN.blit(ui_text, (10, 10))

    # --- 10. Update Tampilan ---
    pygame.display.flip()
    clock.tick(60)

# --- 11. Keluar ---
pygame.quit()
print("Game ditutup.")