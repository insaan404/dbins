import googlemaps
import googlemaps.convert as convert
import requests

def get_pline():
    key = "AIzaSyAqNSUFlOlgV1yLfKBF7MGpcwj_c1476Cc"

    distance_api = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins=34.46184%2C72.01538&destinations=34.18965%2C72.19666&key={key}"

    direction_api = "https://maps.googleapis.com/maps/api/directions/json" \
    "?destination=34.18965%2C72.19666" \
    "&origin=34.46184%2C72.01538"\
    f"&key={key}"

    payload={}
    headers = {}

    response = requests.request("GET", direction_api, headers=headers, data=payload)
    data = response.json()
    route = data["routes"][0]
    polyline = route["overview_polyline"]
    return convert.decode_polyline(polyline["points"])

