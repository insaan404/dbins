from typing import Iterable


class Coordinates:
    lat: float
    lng: float

    def __init__(self, lat: float, lng: float):
        if not (-90 <= lat <= 90) or not (-180 <= lng < 180):
            raise ValueError(f"Wrong Coordinates: {lat}, {lng}")

        self.lat = lat
        self.lng = lng

    def to_dict(self):
        return {"lat": self.lat, "lng": self.lng}

    def __eq__(self, other):
        if abs(self.lat - other.lat) < 0.5 and abs(self.lng - other.lng) < 0.5:
            return True

    def __repr__(self):
        return f"Coordinates(lat={self.lat}, lng={self.lng})"


class Boundry:
    
    def __init__(self, coordinates: Iterable[Coordinates]):
        self.coordinates = coordinates
        self.center = self._calculate_center()

    def _calculate_center(self):
        sum_lat = sum_lng = 0
        for crd in self.coordinates:
            sum_lat += crd.lat
            sum_lng += crd.lng

        avg_lat = sum_lat/len(self.coordinates)
        avg_lng = sum_lng/len(self.coordinates)

        return Coordinates(avg_lat, avg_lng)
    
    def to_dict(self):
        return {
            "center": self.center.to_dict(),
            "coordinates": [crd.to_dict() for crd in self.coordinates]
        }
    
    def __repr__(self) -> str:
        cord = list(self.coordinates)
        return f"{cord!r}"
    
    
