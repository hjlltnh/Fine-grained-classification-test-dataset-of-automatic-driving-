import sharedGlobal


def changePos():
    # sharedGlobal.global_vehicle.set_transform(sharedGlobal.start_transform)
    # print("The vehicle has moved to the set starting point!")
    map=sharedGlobal.global_world.get_map()
    spawn_point=sharedGlobal.start_transform
    waypoint=map.get_waypoint(spawn_point.location)
    spawn_point.location=waypoint.transform.location
    sharedGlobal.global_vehicle.set_transform(spawn_point)
    print(spawn_point.location)
    print("The vehicle has moved to the set starting point!")

def getPos():
  print(sharedGlobal.global_vehicle.get_transform())


changePos()
#print(sharedGlobal.global_vehicle.get_transform().location)
