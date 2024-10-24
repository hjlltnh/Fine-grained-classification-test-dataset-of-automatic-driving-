import datetime
import os
import signal
import carla
import time
import math
import saveInfo
from saveInfo import save_info
import sharedGlobal
from sharedGlobal import alter_shareGlobal as alter_Global
from sharedGlobal import get_shareGlobal as get_Global
from onTick import on_tick
from getInfo import get_info
from Event import event_info
import math
import subprocess

Global_client,Global_world,Global_actors,Global_vehicle=get_Global()

def distance_calculate(vehicle_location,end_location):
    vx=vehicle_location.x
    vy=vehicle_location.y
    vz=vehicle_location.z
    ex=end_location.x
    ey=end_location.y
    ez=end_location.z
    return math.sqrt((vx-ex)**2+(vy-ey)**2+(vz-ez)**2)


def start():
    global Global_client,Global_world,Global_actors,Global_vehicle
    alter=0
    count=200
    end_point=carla.Location(x=64.62,y=1.7,z=0)
    transform=sharedGlobal.global_vehicle.get_transform()
    ##观众视角
    spectator = sharedGlobal.global_world.get_spectator()
    spectator.set_transform(
      carla.Transform(transform.location + carla.Location(x=-10 * math.cos(math.radians(transform.rotation.yaw)),
                                                          y=-10 * math.sin(math.radians(transform.rotation.yaw)),
                                                          z=5),
                      carla.Rotation(pitch=-30, yaw=transform.rotation.yaw)))
    sharedGlobal.spectator = spectator
    blueprint_library=Global_world.get_blueprint_library()
    ##碰撞传感器
    collision_sensor_bp=blueprint_library.find('sensor.other.collision')
    collision_sensor_transform=carla.Transform(carla.Location(x=0.8,z=1.7))
    collision_sensor=Global_world.spawn_actor(collision_sensor_bp,collision_sensor_transform,attach_to=Global_vehicle)
    time.sleep(1.0)
    alter_Global(Global_world)
    collision_sensor_info=event_info()
    collision_sensor.listen(collision_sensor_info.collisionEvent_info)
    #cs=get_info()
    #cs.get_sensor_info(collision_sensor)


    ##lane invasion sensor
    lane_invasion_bp=blueprint_library.find('sensor.other.lane_invasion')
    lane_invasion_transform=carla.Transform(carla.Location(x=2.1,y=0,z=1.7))
    lane_invasion=Global_world.spawn_actor(lane_invasion_bp,lane_invasion_transform,attach_to=Global_vehicle)
    time.sleep(1.0)
    alter_Global(Global_world)
    lane_invasion_info=event_info()
    lane_invasion.listen(lane_invasion_info.laneInvasionEvent_info)

    ##obstacle detector
    obstacle_detector_bp=blueprint_library.find('sensor.other.obstacle')
    obstacle_detector_bp.set_attribute('distance','20.0')
    obstacle_detector_bp.set_attribute('hit_radius','20.0')
    obstacle_detector_transform=carla.Transform(carla.Location(x=1.5,y=0,z=1.7))
    obstacle_detector=Global_world.spawn_actor(obstacle_detector_bp,obstacle_detector_transform,attach_to=Global_vehicle)
    time.sleep(1.0)
    alter_Global(Global_world)
    obstacle_detector_info=event_info()
    obstacle_detector.listen(obstacle_detector_info.obstacleDetect_info)

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y%m%d%H%M%S")
    sharedGlobal.datetime=formatted_time
    print(sharedGlobal.datetime)
    folder_path=f'{sharedGlobal.directory}{formatted_time}'
    os.makedirs(folder_path,exist_ok=True)
    folder_path = f'{sharedGlobal.directory}{formatted_time}/Hazards_and_Issues'
    os.makedirs(folder_path, exist_ok=True)
    ##Initialize the column names of the vehicle driving information file
    save_info(f"{sharedGlobal.directory}{formatted_time}/vehicle_info.csv", saveInfo.fieldnames_vehicle)
    save_info(f"{sharedGlobal.directory}{formatted_time}/actor_info.csv", saveInfo.fieldnames_actor)
    save_info(f"{sharedGlobal.directory}{formatted_time}/Hazards_and_Issues/collision_info.csv",saveInfo.fieldnames_collision)
    save_info(f"{sharedGlobal.directory}{formatted_time}/Hazards_and_Issues/lane_invasion_info.csv",saveInfo.fieldnames_laneInvasion)
    save_info(f"{sharedGlobal.directory}{formatted_time}/Hazards_and_Issues/obstacle_info.csv",saveInfo.fieldnames_obstacle)
    save_info(f"{sharedGlobal.directory}{formatted_time}/Hazards_and_Issues/traffic_light_info.csv",saveInfo.fieldnames_trafficLight)
    save_info(f"{sharedGlobal.directory}{formatted_time}/Hazards_and_Issues/exceed_speed_limit_info.csv",saveInfo.fieldnames_speedLimit)
    save_info(f"{sharedGlobal.directory}{formatted_time}/Hazards_and_Issues/acceleration_change_info.csv",saveInfo.fieldnames_acceleration_change)
    save_info(f"{sharedGlobal.directory}{formatted_time}/Hazards_and_Issues/no_response_info.csv",saveInfo.fieldnames_noresponse)
    save_info(f"{sharedGlobal.directory}{formatted_time}/Hazards_and_Issues/sharp_turning_info.csv",saveInfo.fieldnames_sharpturn)
    save_info(f"{sharedGlobal.directory}{formatted_time}/Hazards_and_Issues/wrong_way_info.csv",saveInfo.fieldnames_wrong_way)
    # start record
    ##print(Global_vehicle,Global_world,Global_actors,Global_client)
    recorder_filename = f'{formatted_time}_recording.log'
    if Global_client:
        print("Recording on file: %s" % Global_client.start_recorder(recorder_filename))
    else:
        print("Not connected to client!")
        os.kill(os.getpid(), signal.SIGINT)
    try:
        while True:
            if alter==0:
                if Global_vehicle and Global_world:
                    Global_vehicle.set_transform(sharedGlobal.start_transform)
                    print("The vehicle has moved to the set starting point!")
                    alter=1
                    velocity=math.sqrt(
                      Global_vehicle.get_velocity().x ** 2 + Global_vehicle.get_velocity().y ** 2 + Global_vehicle.get_velocity().z ** 2)
                    sharedGlobal.velocity.append(velocity)
                    sharedGlobal.pre_acceleration = Global_vehicle.get_acceleration()
                    vehicle_info=get_info()
                    vehicle_info.get_vehicle_info(Global_vehicle)
                    sharedGlobal.no_response_prerecord=(vehicle_info.v_location,vehicle_info.v_rotation,
                                                        vehicle_info.v_velocity,vehicle_info.throttle,
                                                        vehicle_info.brake,vehicle_info.steering,vehicle_info.hand_brake,
                                                        vehicle_info.gear)
                    sharedGlobal.pre_turn_angle=Global_vehicle.get_transform().rotation.yaw
                    world_snapshot = Global_world.wait_for_tick()
                    on_tick(world_snapshot)
                else:
                    break
            else:
                transform=Global_vehicle.get_transform()
                dis=distance_calculate(transform.location,end_point)
                if dis>=0.001 and Global_world:
                    world_snapshot = Global_world.wait_for_tick()
                    on_tick(world_snapshot)
                else:
                    break
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        # stop record
        # client.stop_recorder()
        transform = Global_vehicle.get_transform()
        Global_vehicle.set_transform(sharedGlobal.start_transform)
        collision_sensor.stop()
        collision_sensor.destroy()
        lane_invasion.stop()
        lane_invasion.destroy()
        obstacle_detector.stop()
        obstacle_detector.destroy()

if __name__ == "__main__":
    start()
