import urllib.request
import json 
#zimport requests


def main():

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


        targetDate = "2018-05-11"
        targetTime = "T16:00:00"
        # Search through all prognosi and find correct time
        for hourPrognosis in data["timeSeries"]:
            if targetDate+targetTime in hourPrognosis["validTime"]:
                #print(hourPrognosis)
                #print(json.dumps(hourPrognosis, indent=4, sort_keys=True))

                # Search through parameters for correct values
                for parameter in hourPrognosis["parameters"]:
                    # Temperature
                    if "Cel" in parameter["unit"]:
                        temperature = parameter["values"][0]

        print(temperature)


if __name__ == "__main__":
    main()
