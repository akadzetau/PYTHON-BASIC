import collections
import json
import os
from lxml import etree
from statistics import mean


def get_source_data(source_dir: str) -> collections:
    cities = os.listdir(source_dir)
    for city in cities:
        files = os.listdir(f"{source_dir}/{city}")
        for f in files:
            with open(f"{source_dir}/{city}/{f}", "r") as jsonSourceFile:
                yield {"city": city, "data": json.load(jsonSourceFile)}


def main(source_dir: str):
    # Calculating Temperature and Wind parameters
    results_step2 = []
    for jsonFile in get_source_data(source_dir):
        temp_wind_params = {"city": jsonFile["city"]}
        temp = [h["temp"] for h in jsonFile["data"]["hourly"]]
        wind_speed = [h["wind_speed"] for h in jsonFile["data"]["hourly"]]
        temp_wind_params["data"] = {}
        temp_wind_params["data"]["temp_min"] = min(temp)
        temp_wind_params["data"]["temp_max"] = max(temp)
        temp_wind_params["data"]["temp_mean"] = round(mean(temp), 2)
        temp_wind_params["data"]["wind_speed_min"] = min(wind_speed)
        temp_wind_params["data"]["wind_speed_max"] = max(wind_speed)
        temp_wind_params["data"]["wind_speed_mean"] = round(mean(wind_speed), 2)
        results_step2.append(temp_wind_params)

    # Calculating Summary of Temperature, Wind and places
    temp_mean = round(mean([ct["data"]["temp_mean"] for ct in results_step2]), 2)
    wind_speed_mean = round(mean([ct["data"]["wind_speed_mean"] for ct in results_step2]), 2)
    coldest_city = min(results_step2, key=lambda x: x["data"]["temp_min"])["city"]
    warmest_city = max(results_step2, key=lambda x: x["data"]["temp_max"])["city"]
    windiest_city = max(results_step2, key=lambda x: x["data"]["wind_speed_max"])["city"]

    # Building result XML
    weather = etree.Element("weather", country="Spain", date="2021-09-25")
    etree.SubElement(weather, "summary", mean_temp=str(temp_mean), mean_wind_speed=str(wind_speed_mean),
                     coldest_place=coldest_city, warmest_place=warmest_city, windiest_place=windiest_city)
    cities = etree.SubElement(weather, "cities")
    for city in results_step2:
        cities.append(
            etree.SubElement(cities, city["city"].replace(' ', '_'),
                             # it seems lxml doesn't support special characters in tag. Let's replace it with '_'
                             mean_temp=str(city["data"]["temp_mean"]),
                             max_temp=str(city["data"]["temp_max"]),
                             min_temp=str(city["data"]["temp_min"]),
                             mean_wind_speed=str(city["data"]["wind_speed_mean"]),
                             max_wind_speed=str(city["data"]["wind_speed_max"]),
                             min_wind_speed=str(city["data"]["wind_speed_min"])))

    print(etree.tostring(weather, pretty_print=True, encoding="Unicode"))
    with open("./result.xml", "w") as result:
        result.write(etree.tostring(weather, pretty_print=True, encoding="Unicode"))


if __name__ == "__main__":
    SourceDir: str = "parsing_serialization_task/source_data"

    main(SourceDir)
