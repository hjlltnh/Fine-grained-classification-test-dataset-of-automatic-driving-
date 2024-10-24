import importlib
import os
import signal
import carla
import time
from getInfo import get_info
import sharedGlobal
from sharedGlobal import get_shareGlobal
from saveInfo import save_info
from Event import event_info

Global_client,Global_world,Global_actors,Global_vehicle=get_shareGlobal()
def on_tick(world_snapshot):
    try:
        frame_id=world_snapshot.frame
        timestamp = world_snapshot.timestamp.elapsed_seconds
        weather_info=get_info()
        weather_info.get_weather_info()
        tag=0

        vehicle_info = get_info()
        vehicle_info.get_vehicle_info(Global_vehicle)
        spectator_info = get_info()
        spectator=sharedGlobal.spectator
        spectator_info.get_spectator_info(spectator)


        save_info.save_vehicle_info(Global_vehicle, frame_id, timestamp, spectator_info.s_location,spectator_info.s_rotation,
                                    vehicle_info.v_location, vehicle_info.v_rotation,vehicle_info.v_velocity, vehicle_info.control_info)

        for actor in sharedGlobal.global_actors:
          if isinstance(actor, carla.TrafficSign):
            tag=1
            #traffic_lights_info = get_info()
            #traffic_lights_info.get_trafficSign_info(actor)
            save_info.save_actor_info(actor, tag, frame_id, timestamp)
          if isinstance(actor, carla.TrafficLight):
            tag=2
            #traffic_sign_info = get_info()
            #traffic_sign_info.get_trafficLight_info(actor)
            save_info.save_actor_info(actor, tag, frame_id, timestamp)
          if isinstance(actor,carla.Sensor):
            tag=3
            #sensor_info=get_info()
            #sensor_info.get_sensor_info(actor)
            save_info.save_actor_info(actor, tag, frame_id, timestamp)

        event_info.traffic_light_state_detect(frame_id,timestamp,Global_vehicle)
        event_info.exceed_speed_limit(frame_id,timestamp,Global_vehicle)
        event_info.acceleretation_change(frame_id,timestamp,Global_vehicle)
        event_info.exceed_time_response(frame_id,timestamp,Global_vehicle)
        event_info.sharp_turning(frame_id,timestamp,Global_vehicle)
        print("x:",Global_vehicle.get_location().x)
        print("xt:",sharedGlobal.endLocation.x)
        print("y:",Global_vehicle.get_location().y)
        print("yt:",sharedGlobal.endLocation.y)

    except Exception as e:
        print(f"Error during on_tick: {e}")
