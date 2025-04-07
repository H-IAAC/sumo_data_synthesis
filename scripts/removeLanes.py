import argparse
import os
from lxml import etree as ET

def remove_lanes(root, verbose=False):
    removed_lanes = []
    lane_id = {} # Keeps the current lane ID for each parent element
    mapping = {} # Maps the old lane ID to the new lane ID
    for lane in root.xpath(".//lane"):
        lane_type = lane.get("type")
        lane_id[lane.getparent()] = 0

        if lane_type in ["sidewalk", "shoulder"]:
            removed_lanes.append(lane.get("id"))
            parent = lane.getparent()
            print(f"Removing {lane_type} lane: {lane.attrib.get('id')}")
            parent.remove(lane)

        elif lane_type == "driving":
            lane.set("index", str(lane_id[parent]))
            new_id = lane.get("id").split("_")[0] + f"_{lane_id[parent]}"
            mapping[lane.get("id")] = new_id
            lane.set("id", new_id)
            lane_id[parent] += 1

    edge_ids = [x for x in root.xpath(".//edge/@id") if not x.startswith(":")]
    
    for connect in root.xpath(".//connection"):
        if connect.get("from") in edge_ids:
            print(f"Changing of {connect.get('from')} to 0")
            connect.set("fromLane", "0")
        if connect.get("to") in edge_ids:
            print(f"Changing of {connect.get('to')} to 0")
            connect.set("toLane", "0")
        
    for junction in root.xpath(".//junction"):
        lanes = junction.get("incLanes").split(" ")
        new_lanes = []

        for lane in lanes:
            if lane not in removed_lanes:
                if lane in mapping:
                    print(f"Changing {lane} to {mapping[lane]} in junction {junction.get('id')}")
                    new_lanes.append(mapping[lane])
                else:
                    print(f"Keeping {lane} in junction {junction.get('id')}")
            else:
                print(f"Removing {lane} from junction {junction.get('id')}")

        junction.set("incLanes", " ".join(new_lanes))


    return root

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove <lane allow='pedestrian'> elements from a SUMO net XML file.")
    parser.add_argument("input_file", help="Path to the input XML file.")
    parser.add_argument("-o", "--output", help="Path to the output XML file.")
    parser.add_argument("--sidewalk", action="store_true", help="Enable verbose output.")
    args = parser.parse_args()

    tree = ET.parse(args.input_file)
    root = tree.getroot()

    root = remove_lanes(root, verbose=args.sidewalk)

    print("Writing modified XML to file...")

    output_file = args.output or f"{os.path.splitext(args.input_file)[0]}_modified.net.xml"

    # Write the modified XML back to a file
    tree.write(output_file, encoding="utf-8", xml_declaration=True, pretty_print=True)
