import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_KEY = 'a2586e246ee25f666528091862b8fa8a'


def get_forecast_by_city(city_name):
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid=a2586e246ee25f666528091862b8fa8a&units=metric'
    response = requests.get(url)

    if response.status_code != 200:
        return None, [], response.json().get('message', 'Terjadi kesalahan.')

    data = response.json()
    forecast_by_date = {}
    bencana = []

    for item in data['list']:
        if "12:00:00" in item['dt_txt']:
            date = item['dt_txt'].split()[0]
            temp = item['main']['temp']
            desc = item['weather'][0]['description']
            wind = item['wind']['speed']

            ekstrem = temp > 35 or temp < 20 or "storm" in desc or "heavy rain" in desc or "thunderstorm" in desc or "fog" in desc or wind > 10

            forecast_by_date[date] = {
                "text": f"{date} - {temp:.1f}°C - {desc} - Angin {wind} m/s",
                "ekstrem": ekstrem
            }

            if ekstrem:
                bencana.append(f"{date}: {desc}, {temp:.1f}°C, Angin {wind} m/s")

    return forecast_by_date, bencana, None

def update_date_options():
    kota = selected_city.get()
    if not kota:
        return

    forecast_data, _, error = get_forecast_by_city(kota)
    if error:
        messagebox.showerror("Gagal", f"Error: {error}")
        return

    available_dates = list(forecast_data.keys())
    if available_dates:
        start_date_combo['values'] = available_dates
        end_date_combo['values'] = available_dates
        start_date_combo.set(available_dates[0])
        end_date_combo.set(available_dates[-1])

def show_filtered_forecast():
    kota = selected_city.get()
    start = start_date.get()
    end = end_date.get()
    filter_ekstrem = var_ekstrem.get()

    if not kota:
        messagebox.showwarning("Peringatan", "Masukkan nama kota terlebih dahulu.")
        return

    forecast_data, bencana_list, error = get_forecast_by_city(kota)
    if error:
        messagebox.showerror("Gagal", f"Error: {error}")
        return

    if not start or not end:
        messagebox.showwarning("Peringatan", "Lu mau gua prediksi sampe hari kiamat?")
        return

    filtered = []
    for date, data in forecast_data.items():
        if start <= date <= end:
            if filter_ekstrem:
                if data["ekstrem"]:
                    filtered.append(data["text"])
            else:
                filtered.append(data["text"])

    if filtered:
        result = f"Prakiraan cuaca untuk {kota} dari {start} sampai {end}:\n\n" + "\n".join(filtered)
    else:
        result = "Kondisinya aman aman aja kok, yang penting stay healthy ajaa..."

    if not filter_ekstrem and bencana_list:
        result += "\n\n⚠️ Peringatan: Cuaca buruk terdeteksi harap mempersiapkan diri jika terjadi cuaca yang lebih buruk."

    messagebox.showinfo("Hasil Cuaca", result)


# --- GUI ---
root = tk.Tk()
root.title("Prakiraan Cuaca Global")

tk.Label(root, text="Masukkan Nama Kota:", font=("Arial", 12)).pack(pady=5)
selected_city = tk.StringVar()
city_entry = tk.Entry(root, textvariable=selected_city, width=35)
city_entry.pack(pady=5)

search_btn = tk.Button(root, text="Ambil Tanggal Prakiraan", command=update_date_options)
search_btn.pack(pady=5)

tk.Label(root, text="Tanggal Mulai Preiksi:", font=("Arial", 10)).pack()
start_date = tk.StringVar()
start_date_combo = ttk.Combobox(root, textvariable=start_date, state="readonly", width=20)
start_date_combo.pack(pady=2)

tk.Label(root, text="Tanggal Akhir Prediksi:", font=("Arial", 10)).pack()
end_date = tk.StringVar()
end_date_combo = ttk.Combobox(root, textvariable=end_date, state="readonly", width=20)
end_date_combo.pack(pady=2)

var_ekstrem = tk.BooleanVar()
checkbox = tk.Checkbutton(root, text="Tampilkan hanya cuaca ekstrem", variable=var_ekstrem)
checkbox.pack(pady=5)

btn = tk.Button(root, text="Lihat Prakiraan", command=show_filtered_forecast, bg="#4CAF50", fg="white", padx=10, pady=5)
btn.pack(pady=15)

root.mainloop()
