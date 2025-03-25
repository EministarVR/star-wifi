import subprocess
import re
import customtkinter
from tkinter import messagebox
import webbrowser
from tkinter import HORIZONTAL

# Funktion zum Abrufen der gespeicherten WLAN-Passwörter
def get_wifi_passwords():
    try:
        # Führe den netsh-Befehl aus
        result = subprocess.check_output('netsh wlan show profiles', stderr=subprocess.STDOUT, shell=True).decode('utf-8', errors="ignore")
        profiles = re.findall(r"Profil für alle Benutzer\s*:\s(.*)", result)
        wifi_list = []

        # Gehe durch jedes Profil und versuche, das Passwort zu extrahieren
        for profile in profiles:
            try:
                # Hole die Details für jedes Profil
                profile_details = subprocess.check_output(f'netsh wlan show profile "{profile.strip()}" key=clear', stderr=subprocess.STDOUT, shell=True).decode('utf-8', errors="ignore")
                password = re.search(r"Schlüsselinhalt\s*:\s(.*)", profile_details)
                
                # Füge das Profil und Passwort der Liste hinzu
                wifi_list.append({
                    "SSID": profile.strip(),
                    "Password": password.group(1).strip() if password else "Kein Passwort gespeichert"
                })
            except subprocess.CalledProcessError as e:
                pass
        return wifi_list
    except subprocess.CalledProcessError as e:
        return []

# Funktion zum Anzeigen der gespeicherten WLAN-Passwörter
def show_passwords():
    wifi_data = get_wifi_passwords()
    textbox.delete("0.0", "end")
    if not wifi_data:
        textbox.insert("0.0", "❌ Keine gespeicherten WLANs gefunden.")
    for wifi in wifi_data:
        textbox.insert("end", f"📶 SSID: {wifi['SSID']}\n🔑 Passwort: {wifi['Password']}\n{'-'*40}\n")

# Über uns
def show_about():
    about_window = customtkinter.CTkToplevel(app)
    about_window.title("Über StarWiFi")
    about_window.geometry("800x600")
    about_window.resizable(False, False)
    
    main_frame = customtkinter.CTkFrame(about_window)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Titel
    title = customtkinter.CTkLabel(
        main_frame,
        text="🌟 StarWiFi - WLAN Passwort Viewer",
        font=("Segoe UI", 20, "bold")
    )
    title.pack(pady=10)

    # Info-Text
    info_text = """Version 1.0.2 (Beta)
Entwickelt von EministarVR
Veröffentlichungsdatum: 25.03.2025

🚀 Funktionen:
- Anzeige aller gespeicherten WLAN-Passwörter
- Einfache Bedienung mit modernem UI
- Direkte Export-Funktion (geplant)
- Multi-OS Support (in Entwicklung)

📅 Changelog:
v1.0.0 (25.03.2025)
- Erstveröffentlichung
- Grundlegende Funktionen implementiert

v1.0.1 (25.03.2025)
- UI-Verbesserungen
- Performance-Optimierungen

v1.0.2 (25.03.2025)
- Responsive Design
- Erweitertes About-Menü

🔮 Geplante Features:
- Android App (Google Play)
- iCloud Sync (experimentell)
- Netzwerkanalyse-Tools
"""
    textbox = customtkinter.CTkTextbox(
        main_frame,
        width=700,
        height=300,
        wrap="word",
        font=("Segoe UI", 14)
    )
    textbox.insert("0.0", info_text)
    textbox.configure(state="disabled")
    textbox.pack(pady=10)

    # Social Media Links
    links_frame = customtkinter.CTkFrame(main_frame)
    links_frame.pack(pady=10)

    def open_discord():
        webbrowser.open("https://discord.gg/PuZNvVNw")

    discord_btn = customtkinter.CTkButton(
        links_frame,
        text="💬 Discord Server",
        command=open_discord,
        fg_color="#5865F2",
        hover_color="#4752C4",
        width=200
    )
    discord_btn.pack(side="left", padx=10)

    social_text = customtkinter.CTkLabel(
        links_frame,
        text="TikTok: @EministarVR\nGitHub: EministarVR",
        font=("Segoe UI", 14, "italic")
    )
    social_text.pack(side="left", padx=10)

    # Trennlinie
    customtkinter.CTkLabel(main_frame, text="─"*100).pack(pady=5)

    # Footer
    footer = customtkinter.CTkLabel(
        main_frame,
        text="🔒 Alle Rechte vorbehalten | © 2025 EministarVR\n📧 Kontakt: benounnaelemin@gmail.com",
        font=("Segoe UI", 12),
        text_color=("gray70", "gray30")
    )
    footer.pack(pady=10)

    about_window.transient(app)
    about_window.grab_set()
# --- UI SETUP ---
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.title("🌟 StarWiFi - WLAN Passwort Viewer")
app.geometry("850x600")
app.minsize(800, 550)
app.resizable(True, True)

# Hauptcontainer mit Grid-Layout
main_frame = customtkinter.CTkFrame(app)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Grid-Konfiguration für responsives Layout
main_frame.grid_rowconfigure(1, weight=1)  # Textbox erhält expandierbaren Bereich
main_frame.grid_columnconfigure(0, weight=1)

# Titel
title = customtkinter.CTkLabel(
    main_frame, 
    text="🌟 StarWiFi", 
    font=("Segoe UI", 32, "bold")
)
title.grid(row=0, column=0, pady=20, sticky="n")

# Textbox mit Scrollbar
textbox = customtkinter.CTkTextbox(
    main_frame,
    corner_radius=15,
    font=("Segoe UI", 16),
    wrap="word"
)
textbox.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

# Button-Container
btn_frame = customtkinter.CTkFrame(main_frame)
btn_frame.grid(row=2, column=0, sticky="sew", padx=20, pady=20)

# Button-Grid für gleichmäßige Verteilung
btn_frame.grid_columnconfigure((0, 1), weight=1)
btn_frame.grid_rowconfigure(0, weight=1)

# Scan-Button
scan_btn = customtkinter.CTkButton(
    btn_frame,
    text="🔍 Scannen",
    command=show_passwords,
    height=50,
    font=("Segoe UI", 16)
)
scan_btn.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

# Über-Button
about_btn = customtkinter.CTkButton(
    btn_frame,
    text="ℹ Über",
    command=show_about,
    height=50,
    font=("Segoe UI", 16)
)
about_btn.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

app.mainloop()