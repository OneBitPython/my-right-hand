import folium
import webbrowser
from geopy.geocoders import Nominatim


def lat_lng(place):
    geolocator = Nominatim(user_agent="Map")
    location = geolocator.geocode(place)
    coordinate = (location.latitude, location.longitude)
    return coordinate


def regularMap(place):
    lat, lng = lat_lng(place)
    print(lat, lng)

    token = "pk.eyJ1Ijoid2lsZHJvcCIsImEiOiJja2hpdHR3bXEwdXhzMzNvMTViN3U2OTBpIn0.uVDMCtkDDlwUAln3X0I3Sg"
    map_osm = folium.Map(location=[lat, lng],
                         tiles='https://api.mapbox.com/v4/mapbox.run-bike-hike/{z}/{x}/{y}.png?access_token=' + str(
                             token), attr="Mapbox", zoom_start=15)
    map_osm.save('maps\\osm.html')


try:
    regularMap(place)
except Exception as e:
    pass


def satelliteMap(place):
    lat, lng = lat_lng(place)
    print(lat, lng)

    token = "pk.eyJ1Ijoid2lsZHJvcCIsImEiOiJja2hpdHR3bXEwdXhzMzNvMTViN3U2OTBpIn0.uVDMCtkDDlwUAln3X0I3Sg"
    map_osm = folium.Map(location=[lat, lng],
                         tiles='https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}@2x.png?access_token=' + str(
                             token), attr="Mapbox", zoom_start=15)
    map_osm.save('maps\\sat.html')

    webbrowser.open("file:///C:/Users/acham/PycharmProjects/Competition/maps/sat.html")


try:
    satelliteMap(place)
except Exception as e:
    pass


def roadMap(place):
    lat, lng = lat_lng(place)
    print(lat, lng)

    map_osm = folium.Map(location=[lat, lng],
                         tiles='https://api.mapbox.com/styles/v1/wildrop/ckhju9pfn4q2i19np3p4k9ilw/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1Ijoid2lsZHJvcCIsImEiOiJja2hpdHMweTgwdXZ3MnpwOWd4aDRpa3cxIn0.yucO4mJ-Tog-HaW_3Fl5Kw',
                         attr="Mapbox", zoom_start=15)

    map_osm.save("maps\\roadMap.html")

    webbrowser.open("file:///C:/Users/acham/PycharmProjects/Competition/maps/roadMap.html")


try:
    roadMap(place)
except Exception as e:
    pass




