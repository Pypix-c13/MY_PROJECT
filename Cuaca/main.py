import asyncio
import aiohttp

WMO_CODES = {
    0: "Cerah",
    1: "Cerah Berawan",
    2: "Berawan Sebagian",
    3: "Mendung / Berawan",
    45: "Kabut",
    48: "Kabut Tebal / Rime Fog",
    51: "Gerimis Ringan",
    53: "Gerimis Sedang",
    55: "Gerimis Lebat",
    56: "Gerimis Dingin Ringan",
    57: "Gerimis Dingin Lebat",
    61: "Hujan Ringan",
    63: "Hujan Sedang",
    65: "Hujan Lebat",
    66: "Hujan Es Ringan",
    67: "Hujan Es Lebat",
    71: "Salju Ringan",
    73: "Salju Sedang",
    75: "Salju Lebat",
    77: "Butiran Salju",
    80: "Hujan Lokal Ringan",
    81: "Hujan Lokal Sedang",
    82: "Hujan Lokal Lebat / Deras",
    85: "Hujan Salju Ringan",
    86: "Hujan Salju Lebat",
    95: "Badai Petir / Badai Guruh",
    96: "Badai Petir + Hujan Es Ringan",
    99: "Badai Petir + Hujan Es Lebat",
}

def get_weather_desc(code):
    return WMO_CODES.get(code, f"Tidak Diketahui ({code})")

lat = -0.9492
lon = 100.3543

url = (
    f"https://api.open-meteo.com/v1/forecast"
    f"?latitude={lat}&longitude={lon}"
    f"&hourly=temperature_2m,relative_humidity_2m,weather_code"
    f"&timezone=Asia%2FJakarta"
)

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                hourly = data["hourly"]
                
                for i in range(min(25, len(hourly["time"]))):
                    waktu = hourly["time"][i]
                    suhu = hourly["temperature_2m"][i]
                    kelembapan = hourly["relative_humidity_2m"][i]
                    code = hourly["weather_code"][i]
                    
                    kondisi = get_weather_desc(code)
                    
                    print(f"Waktu     : {waktu}")
                    print(f"Kondisi   : {kondisi}")
                    print(f"Suhu      : {suhu}°C")
                    print(f"Kelembapan: {kelembapan}%")
                    print("-" * 30)
            else:
                print(f"Failed to get data. Status: {response.status}")

asyncio.run(main())