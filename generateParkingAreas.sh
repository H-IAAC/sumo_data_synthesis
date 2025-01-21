# Generating parking area files and rerouters
echo "This script will generate parking areas around the map and also rerouters for them"
read -p "Enter the name of the map folder: " folder
if [ ! -d "$folder" ]; then
    echo "The folder '$folder' does not exist."
    exit 1
fi
gzip -dk -f "$folder"/osm.net.xml.gz
python3 /usr/share/sumo/tools/generateParkingAreas.py --net "$folder/osm.net.xml" --out "$folder/park.add.xml"
python3 /usr/share/sumo/tools/generateParkingAreaRerouters.py -n "$folder/osm.net.xml" -a "$folder/park.add.xml" -o "$folder/pa_rerouter.xml" --max-number-alternatives 4 --max-distance-alternatives 100
