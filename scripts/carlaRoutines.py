import csv
import carla

def get_spawn_points_from_csv(csv_file):
    spawn_points = {}
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            loc = carla.Location(float(row['x']), float(row['y']), float(row['z']))
            rot = carla.Rotation(float(row['pitch']), float(row['yaw']), float(row['roll']))
            spawn_points[row['Name']] = carla.Transform(loc, rot)
    
    return spawn_points