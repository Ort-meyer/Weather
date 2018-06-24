import urllib.request
import json 
import argparse
from datetime import datetime
#zimport requests


class WeatherFetcher:
    def __init__(self, live):
        self.live = live

    def GetWeather(self):
        if self.live:
            now = datetime.now()
            self.GetWeatherLive(now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"))
        else:
            self.GetWeatherDebug()

    def GetWeatherDebug(self):
        self.temperature = "20"
    def GetWeatherLive(self, date, time):
        """Gets the temperatur of current position at given time and date
        Date should be in format HH:00:00, date in YY-MM-DD. Only works
        for current date"""
        # Get my position
        send_url = 'http://freegeoip.net/json'

        with urllib.request.urlopen(send_url) as url:
            data = json.loads(url.read().decode())
            lat = str(data['latitude'])
            lon = str(data['longitude'])
        print("lat: " + lat + " long: " + lon)


        # Get temperature

        baseUrl = "https://opendata-download-metfcst.smhi.se"
        addedUrl = "/api/category/pmp2g/version/2/geotype/point/lon/"+lon+"/lat/"+lat+"/data.json"

        with urllib.request.urlopen(baseUrl+addedUrl) as url:
            data = json.loads(url.read().decode())

            temperature = "NOTEMP"

            # Search through all prognosi and find correct time
            for hourPrognosis in data["timeSeries"]:
                #print(hourPrognosis)
                #print(json.dumps(hourPrognosis, indent=4, sort_keys=True))
                #quit()
                if date+"T"+time[:2]+":00:00" in hourPrognosis["validTime"]:
                    #print(hourPrognosis)
                    #print(json.dumps(hourPrognosis, indent=4, sort_keys=True))

                    # Search through parameters for correct values
                    for parameter in hourPrognosis["parameters"]:
                        # Temperature
                        if "Cel" in parameter["unit"]:
                            temperature = parameter["values"][0]

            self.temperature = temperature

    def GetTemperature(self):
        return self.temperature

def main():
    parser = argparse.ArgumentParser()
    #parser.add_argument("echo", help="echo the string you use here")
    #parser.add_argument("square", help="display a square of a given number", type=int)
    #parser.add_argument("-v", "--verbose", help="displays verbose debug info", action="store_true")
    parser.add_argument("-l", "--live", help="runs live/online", action="store_true")
    args = parser.parse_args()
    wf = WeatherFetcher(args.live)
    wf.GetWeather()
    print(wf.GetTemperature())
    #print(args.echo)
    #print(args.square**2)
    quit()






if __name__ == "__main__":
    main()
