function draw_boundry(map, coordinates) {
  var boundry = new google.maps.Polygon({
    fillColor: "#00f0f0",
    fillOpacity: 0.2,
    map: map,
    paths: coordinates,
    strokeColor: "#ff0000",
    strokeOpacity: 1.0,
  });

  return boundry;
}

function findCenter(coordinates) {
  bound = new google.maps.LatLngBounds();
  coordinates.forEach((element) => {
    bound.extend(element);
  });

  return bound.getCenter();
}

function putMarker(map, crd, icn, size) {
  var icon = google.maps.SymbolPath.CIRCLE;
  if (!size) size = new google.maps.Size(60, 60);
  else size = new google.maps.Size(size[0], size[1]);

  if (icn) {
    icon = {
      url: icn,
      scaledSize: size,
      fillColor: "#fd0000",
      fillOpacity: 1,
      strokeWeight: 0,
    };
  } else {
    icon = {
      path: google.maps.SymbolPath.CIRCLE,
      scale: 6,
      scaledSize: size,
      fillColor: "#fd0000",
      fillOpacity: 1,
      strokeWeight: 0,
    };
  }

  var marker = new google.maps.Marker({
    position: new google.maps.LatLng(crd.lat, crd.lng),
    map: map,
    icon: icon,
  });
  console.log("marker: ", marker);
  return marker;
}

function putWdas(map, wdas) {
  wdas.forEach((wda) => {
    var marker = putMarker(
      map,
      wda.location,
      "/media/static/images?image=wda.png",
      [30, 30]
    );
    marker.setTitle(wda.name);
  });
}

class OfficeMap {
  map;
  coordinates;
  boundry = null;
  center;
  office = null;
  markers = [];
  dbin_markers = [];
  identifierMarker = null;
  dbins;
  _prev_dbin = null;

  constructor(map, office, dbins) {
    this.coordinates = office.boundry.coordinates;
    this.center = office.boundry.center;
    this.office = office;
    this.map = map;
    this.dbins = dbins;

    this.draw_boundry();
    this._putIdentifierMarker();
    this._putDbins();
  }

  delete = function () {
    this.boundry.setMap(null);
    this.markers.forEach((marker) => {
      marker.setMap(null);
    });
    this._removeDbinMarkers();
    this.removeIdentifierMarker();
  };

  _putDbin = function (dbin) {
    var marker = this.put_marker(
      dbin.location,
      "/media/static/images?image=green_bin.png",
      [20, 20]
    );

    this.dbin_markers.push(marker);
  };

  _putDbins = function () {
    this.dbins.forEach((dbin) => {
      this._putDbin(dbin);
    });
  };

  _removeDbinMarkers = function () {
    console.log(this.dbin_markers);
    this.dbin_markers.forEach((marker) => {
      marker.setMap(null);
    });
    this.dbin_markers.splice(0);
  };

  draw_boundry() {
    this.boundry = new google.maps.Polygon({
      fillColor: "#00f0f0",
      fillOpacity: 0.2,
      map: this.map,
      paths: this.coordinates,
      strokeColor: "#ff0000",
      strokeOpacity: 1.0,
    });
  }

  removeIdentifierMarker() {
    if (this.identifierMarker !== null) {
      this.identifierMarker.setMap(null);
    }
  }

  showIdentifierMarker() {
    if (this.identifierMarker !== null) {
      this.identifierMarker.setMap(this.map);
    }
  }

  _putIdentifierMarker() {
    this.identifierMarker = new google.maps.marker.AdvancedMarkerElement({
      map: this.map,
      position: this.center,
      title: this.office.area_name,
    });
  }

  putRedDot = function (crd, size) {
    if (!size) size = new google.maps.Size(60, 60);
    else size = new google.maps.Size(size[0], size[1]);

    var marker = new google.maps.Marker({
      position: new google.maps.LatLng(crd.lat, crd.lng),
      map: this.map,
      icon: {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 6,
        scaledSize: size,
        fillColor: "#fd0000",
        fillOpacity: 1,
        strokeWeight: 0,
      },
    });

    return marker;
  };

  putDbin = function (crd) {
    this._removePrevDbin();
    var dbin = this.put_marker(
      crd,
      "/media/static/images?image=green_bin.png",
      [25, 25]
    );

    this._prev_dbin = dbin;
  };

  _removePrevDbin() {
    if (this._prev_dbin) {
      this._prev_dbin.setMap(null);
      this._prev_dbin = null;
    }
  }

  put_marker(crd, icn, size) {
    var icon = google.maps.SymbolPath.CIRCLE;
    if (!size) size = new google.maps.Size(60, 60);
    else size = new google.maps.Size(size[0], size[1]);

    if (icn) {
      icon = {
        url: icn,
        scaledSize: size,
        fillColor: "#fd0000",
        fillOpacity: 1,
        strokeWeight: 0,
      };
    } else {
      icon = {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 6,
        scaledSize: size,
        fillColor: "#fd0000",
        fillOpacity: 1,
        strokeWeight: 0,
      };
    }

    var marker = new google.maps.Marker({
      position: new google.maps.LatLng(crd.lat, crd.lng),
      map: this.map,
      icon: icon,
    });

    return marker;
  }
}
