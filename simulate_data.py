import pandas as pd
import random

crop_types = ['Wheat', 'Corn', 'Rice', 'Soybean']
seasons = ['Spring', 'Summer', 'Autumn', 'Winter']

def generate_data(samples=1000):
    data = []
    for _ in range(samples):
        temp = round(random.uniform(20, 40), 1)
        humidity = round(random.uniform(30, 80), 1)
        soil = round(random.uniform(10, 60), 1)
        wind = round(random.uniform(0, 15), 1)  # wind speed km/h
        rainfall = random.choice([0, 0.5, 2.0])  # mm rainfall forecast
        crop = random.choice(crop_types)
        season = random.choice(seasons)

        # Simple irrigation logic
        irrigate = 1 if (soil < 30 and rainfall < 1) else 0

        data.append([temp, humidity, soil, wind, rainfall, crop, season, irrigate])

    df = pd.DataFrame(data, columns=["Temp", "Humidity", "Soil", "Wind", "Rainfall", "Crop", "Season", "Irrigation"])
    df.to_csv("simulated_data_extended.csv", index=False)

if __name__ == "__main__":
    generate_data()
    print("Simulated data generated and saved to simulated_data_extended.csv")
