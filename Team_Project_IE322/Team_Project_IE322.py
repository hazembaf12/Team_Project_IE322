import tkinter as tk
from tkinter import messagebox
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from datetime import datetime
import pytz

def confirm_location(address, label):
    return messagebox.askyesno("Confirm Location", f"{label}:\n{address}\n\nIs this the correct location?")

def calculate_price():
    start_input = entry_start.get()
    end_input = entry_end.get()

    geolocator = Nominatim(user_agent="dynamic_pricing_gui")

    try:
        loc1 = geolocator.geocode(start_input)
        if not loc1:
            messagebox.showerror("Error", "Starting location not found.")
            return

        if not confirm_location(loc1.address, "Starting location"):
            return

        loc2 = geolocator.geocode(end_input)
        if not loc2:
            messagebox.showerror("Error", "Destination location not found.")
            return

        if not confirm_location(loc2.address, "Destination location"):
            return

        coord1 = (loc1.latitude, loc1.longitude)
        coord2 = (loc2.latitude, loc2.longitude)

        distance_km = geodesic(coord1, coord2).kilometers
        base_price = round(distance_km * 2.0, 2)  # 2 SAR per km

        sa_time = datetime.now(pytz.timezone("Asia/Riyadh"))
        hour = sa_time.hour

        if 6 <= hour < 12:
            multiplier = 1.1
        elif 12 <= hour < 18:
            multiplier = 1.2
        elif 18 <= hour < 23:
            multiplier = 1.3
        else:
            multiplier = 1.05

        final_price = round(base_price * multiplier, 2)
        increase_percent = int((multiplier - 1.0) * 100)  # Example: 1.3 -> 30%

        result_label.config(
            text=f"From: {start_input}\n"
                 f"To: {end_input}\n"
                 f"Distance: {round(distance_km, 2)} km\n"
                 f"Saudi Time: {sa_time.strftime('%H:%M')}\n\n"
                 f"Base Price: {base_price} SAR\n"
                 f"Time-based Increase: {increase_percent}%\n"
                 f"Final Price: {final_price} SAR"
        )

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# GUI setup
window = tk.Tk()
window.title("Trip Price")
window.geometry("520x450")
window.config(bg="#f7f7f7")

tk.Label(window, text="Your trip price", font=("Arial", 18, "bold"), bg="#f7f7f7", fg="#333").pack(pady=10)

entry_start = tk.Entry(window, width=50)
entry_start.insert(0, "Enter Location, City")
entry_start.pack(pady=5)

entry_end = tk.Entry(window, width=50)
entry_end.insert(0, "Enter destination, City")
entry_end.pack(pady=5)

tk.Button(window, text="Calculate Price", command=calculate_price, bg="#4CAF50", fg="white", width=20).pack(pady=10)

result_label = tk.Label(window, text="", font=("Arial", 11), bg="#f7f7f7", fg="#333", justify="left")
result_label.pack(pady=10)

tk.Button(window, text="Exit", command=window.quit, bg="#d9534f", fg="white", width=10).pack(pady=5)

window.mainloop()

