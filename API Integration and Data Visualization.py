import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

API_KEY = "Replace Your API Key here"
CITY = "Bengaluru,IN"
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.titlepad'] = 15

def fetch_weather_data():
    """Fetch 5-day weather forecast data"""
    params = {'q': CITY, 'appid': API_KEY, 'units': 'metric'}
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()['list']
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def process_weather_data(weather_data):
    """Process raw weather data into DataFrame"""
    processed = []
    for entry in weather_data:
        dt = datetime.fromtimestamp(entry['dt'])
        processed.append({
            'datetime': dt,
            'date': dt.strftime('%Y-%m-%d'),
            'hour': dt.hour,
            'temperature': entry['main']['temp'],
            'humidity': entry['main']['humidity'],
            'pressure': entry['main']['pressure'],
            'wind_speed': entry['wind']['speed'],
            'weather': entry['weather'][0]['main'],
            'description': entry['weather'][0]['description']
        })
    return pd.DataFrame(processed)

def create_visualizations(df):
    """Create optimized weather visualizations"""
    fig = plt.figure(figsize=(18, 14), constrained_layout=True)
    
    fig.suptitle('Bengaluru 5-Day Weather Forecast', 
                fontsize=18, fontweight='bold', y=0.04) 
    
    gs = fig.add_gridspec(3, 2)
    
    # Plot 1: Temperature Trend
    ax1 = fig.add_subplot(gs[0, :])
    sns.lineplot(data=df, x='datetime', y='temperature', marker='o', ax=ax1)
    ax1.set_title('Temperature Trend (°C)', pad=20)
    ax1.set_xlabel('')
    ax1.tick_params(axis='x', rotation=45)
    
    # Plot 2: Humidity and Pressure 
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.plot(df['datetime'], df['humidity'], color='blue', marker='o')
    ax2.set_title('\nHumidity (%)(Blue) / Pressure (hPa)(Red)', pad=15)  
    ax2.tick_params(axis='x', rotation=45)
    
    ax2b = ax2.twinx()
    ax2b.plot(df['datetime'], df['pressure'], color='red', marker='o')
    ax2b.set_title('\n', pad=15) 
    
    # Plot 3: Wind Speed
    ax3 = fig.add_subplot(gs[1, 1])
    sns.barplot(data=df, x='date', y='wind_speed', hue='hour', 
               palette='coolwarm', ax=ax3)
    ax3.set_title('Wind Speed by Date/Hour (m/s)', pad=15)
    ax3.legend(title='Hour', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Plot 4: Weather Conditions
    ax4 = fig.add_subplot(gs[2, :])
    weather_counts = df['weather'].value_counts()
    wedges, texts, autotexts = ax4.pie(
        weather_counts, 
        labels=weather_counts.index, 
        autopct='%1.1f%%',
        startangle=90,
        colors=sns.color_palette("pastel"),
        textprops={'fontsize': 12}
    )
    ax4.set_title('Weather Conditions Distribution', pad=20)
    
    # Adjust label positions
    plt.setp(autotexts, size=12, weight='bold')
    plt.setp(texts, size=12)
    
    plt.savefig('bengaluru_weather_dashboard.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """Main execution"""
    print("Fetching weather data...")
    data = fetch_weather_data()
    
    if data:
        df = process_weather_data(data)
        print("Creating visualizations...")
        create_visualizations(df)
        df.to_csv('bengaluru_weather_data.csv', index=False)
        print("Dashboard saved successfully")
    else:
        print("Failed to fetch data")

if __name__ == "__main__":
    main()
