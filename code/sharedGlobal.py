import carla
from __init__ import base_info

global_client,global_world,global_actors,global_vehicle=base_info()
spectator=None
startLocation=carla.Location(x=0,y=0,z=0)        ##Set it as the starting point at the position we want it to be at (x=13.3, y=2.17, z=0)
#x=-22.40,y=-138.65,z=0.41
startRotation = carla.Rotation(pitch=0, yaw=0, roll=0)  ##Car pose setting
start_transform = carla.Transform(startLocation, startRotation)
has_light=False
traffic_light_id = None
light_is_red=False
has_velocity=False
has_move=False
velocity=[]
traffic_light_location=None
pre_transform=global_vehicle.get_transform().location
pre_acceleration=0
no_response_time=0
has_light_no_response_time=0
no_response_prerecord=0
pre_turn_velocity=None
pre_turn_angle=None
datetime=None
directory='/media/hjl/TSD302/Town03/'      ##Set as the path for collecting data

endLocation=carla.Location(x=-9.5,y=-5.45,z=0)
def get_shareGlobal():
  if global_client and global_world and global_actors and global_vehicle:
      return global_client,global_world,global_actors,global_vehicle
  else:
    print("Not get base information!")
    return global_client,global_world,global_actors,global_vehicle

def alter_shareGlobal(world):
    global global_actors
    global_actors=world.get_actors()
    return global_actors


