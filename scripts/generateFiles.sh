#!/bin/bash
gzip -dk -f osm.net.xml.gz
python3 /usr/share/sumo/tools/generateParkingAreas.py --net osm.net.xml --out park.add.xml
python3 /usr/share/sumo/tools/generateParkingAreaRerouters.py -n osm.net.xml -a park.add.xml -o pa_rerouter.xml --max-number-alternatives 4 --max-distance-alternatives 100
