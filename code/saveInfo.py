import csv
from getInfo import get_info
import sharedGlobal

fieldnames_vehicle=["Frame","Timestamp","VehicleID","Spectator_Location","Spectator_Rotation","Vehicle_Location","Vehicle_Rotation",
                    "Vehicle_Velocity","Vehicle_Control"]
fieldnames_actor=["Frame","Timestamp","ActorID",
                  "Weather_cloudiness","Weather_precipitation","Weather_precipitation_deposits","Weather_wind_intensity",
                  "Weather_sun_azimuth_angle","Weather_sun_altitude_angle","Weather_fog_density","Weather_fog_distance",
                  "Weather_wetness","Weather_fog_falloff","Weather_scattering_intensity","Weather_mie_scattering_scale",
                  "Weather_rayleigh_scattering_scale","Weather_dust_storm",
                  "Type","Actor_Content"]
fieldnames_pointcloud=['x','y','z']
fieldnames_collision=['Frame','Timestamp','ActorID','ActorType','Other_ActorID','Other_ActorType','CollisionPos','CollisionDegree']
fieldnames_laneInvasion=['Frame','Timestamp','ActorID','ActorType','LaneMarking','LaneInvasionPos']
fieldnames_obstacle=['Frame','Timestamp','ActorID','ActorType','Other_ActorID','Other_ActorType','Distance']
fieldnames_trafficLight=['Frame','Timestamp','ActorID','ActorType','TrafficLightID','TrafficLightPos','ActorVelocity']
fieldnames_speedLimit=['Frame','Timestamp','ActorID','ActorType','SpeedLimitValue(km/h)','Velocity']
fieldnames_acceleration_change=['Frame','Timestamp','ActorID','ActorType','DeltaAcceleration(m/s)','ChangePos','MayRapidAcceleration/MayRapiDeceleration']
fieldnames_noresponse=['Frame','Timestamp','ActorID','ActorType','NoResponseLocation','NoResponseRotation']
fieldnames_sharpturn=['Frame','Timestamp','ActorID','ActorType','Lateral_acceleration','TurnAngle','Velocity']
fieldnames_wrong_way=['Frame','Timestamp','ActorID','ActorType','LandID','Location','VehicleDirection','LaneDirection']
class save_info:
    def __init__(self,filename,fieldnames):
        with open(filename,'w',newline='') as file:
            writer=csv.DictWriter(file,fieldnames=fieldnames)
            writer.writeheader()

    def format_location_vector(vector):
        return f"({vector.x},{vector.y},{vector.z})"

    def format_rotation_vector(vector):
        return f"({vector.pitch},{vector.yaw},{vector.roll})"

    def format_trafficLight(L_location,L_rotation,L_state,L_elapsed_time):
        return f"('Light_Location':{L_location},'Light_rotation': {L_rotation},'Light_state': {L_state},'Light_elapsed_time': {L_elapsed_time})"
    def format_trafficSign(TS_location,TS_rotation,TS_type):
        return f"('Sign_Location':{TS_location},'Sign_Rotation':{TS_rotation},'Sign_Type':{TS_type})"

    def format_sensor(Sen_location,Sen_rotation,Sen_type,Sen_listen):
      return f"('Sensor_Location':{Sen_location},'Sensor_Rotation':{Sen_rotation},'Sensor_Type':{Sen_type},'Sensor_listen':{Sen_listen})"

    def format_laneMarking(lanemarking):
      for lane in lanemarking:
        lane_color=lane.color
        lane_type=lane.type
        lane_change=lane.lane_change
        lane_width=lane.width
        return f"('LaneMarking_Color':{lane_color},'LaneMarking_LaneChange':{lane_change},'LaneMarking_Type':{lane_type},'LaneMarking_Width':{lane_width})"

    def save_vehicle_info(vehicle,frame, timestamp, s_location,s_rotation,v_location,v_rotation,v_velocity,v_control_info):
        with open(f'{sharedGlobal.directory}{sharedGlobal.datetime}/vehicle_info.csv','a') as file:
            writer=csv.DictWriter(file,fieldnames=fieldnames_vehicle)
            writer.writerow({
                "Frame":frame,
                "Timestamp":timestamp,
                "VehicleID":vehicle.id,
                "Spectator_Location":save_info.format_location_vector(s_location),
                "Spectator_Rotation":save_info.format_rotation_vector(s_rotation),
                "Vehicle_Location":save_info.format_location_vector(v_location),
                "Vehicle_Rotation":save_info.format_rotation_vector(v_rotation),
                "Vehicle_Velocity":v_velocity,
                "Vehicle_Control":v_control_info
            })

    def save_actor_info(actor,tag,frame,timestamp):
        actor_info=get_info()
        actor_info.get_weather_info()
        with open(f'{sharedGlobal.directory}{sharedGlobal.datetime}/actor_info.csv','a') as file:
            writer=csv.DictWriter(file,fieldnames=fieldnames_actor)
            if tag==1:
                actor_info.get_trafficSign_info(actor)
                writer.writerow({
                    "Frame": frame,
                    "Timestamp": timestamp,
                    "ActorID": actor.id,
                    "Weather_cloudiness": actor_info.cloudiness,
                    "Weather_precipitation": actor_info.precipitation,
                    "Weather_precipitation_deposits": actor_info.precipitation_deposits,
                    "Weather_wind_intensity": actor_info.wind_intensity,
                    "Weather_sun_azimuth_angle": actor_info.sun_azimuth_angle,
                    "Weather_sun_altitude_angle": actor_info.sun_altitude_angle,
                    "Weather_fog_density": actor_info.fog_density,
                    "Weather_fog_distance": actor_info.fog_distance,
                    "Weather_wetness":actor_info.wetness,
                    "Weather_fog_falloff":actor_info.fog_falloff,
                    "Weather_scattering_intensity":actor_info.scattering_intensity,
                    "Weather_mie_scattering_scale":actor_info.mie_scattering_scale,
                    "Weather_rayleigh_scattering_scale":actor_info.rayleigh_scattering_scale,
                    "Weather_dust_storm":actor_info.dust_storm,
                    "Type":actor.type_id,
                    "Actor_Content":save_info.format_trafficSign(actor_info.sign_location,actor_info.sign_rocation,actor_info.sign_type_id)
                })
            elif tag == 2:
                actor_info.get_trafficLight_info(actor)
                writer.writerow({
                    "Frame": frame,
                    "Timestamp": timestamp,
                    "ActorID": actor.id,
                    "Weather_cloudiness": actor_info.cloudiness,
                    "Weather_precipitation": actor_info.precipitation,
                    "Weather_precipitation_deposits": actor_info.precipitation_deposits,
                    "Weather_wind_intensity": actor_info.wind_intensity,
                    "Weather_sun_azimuth_angle": actor_info.sun_azimuth_angle,
                    "Weather_sun_altitude_angle": actor_info.sun_altitude_angle,
                    "Weather_fog_density": actor_info.fog_density,
                    "Weather_fog_distance": actor_info.fog_distance,
                    "Weather_wetness": actor_info.wetness,
                    "Weather_fog_falloff": actor_info.fog_falloff,
                    "Weather_scattering_intensity": actor_info.scattering_intensity,
                    "Weather_mie_scattering_scale": actor_info.mie_scattering_scale,
                    "Weather_rayleigh_scattering_scale": actor_info.rayleigh_scattering_scale,
                    "Weather_dust_storm": actor_info.dust_storm,
                    "Type":actor.type_id,
                    "Actor_Content":save_info.format_trafficLight(actor_info.light_location,actor_info.light_rocation,actor_info.light_state,actor_info.light_elapsed_time)
                })
            elif tag==3:
                actor_info.get_sensor_info(actor)
                writer.writerow({
                    "Frame": frame,
                    "Timestamp": timestamp,
                    "ActorID": actor.id,
                    "Weather_cloudiness": actor_info.cloudiness,
                    "Weather_precipitation": actor_info.precipitation,
                    "Weather_precipitation_deposits": actor_info.precipitation_deposits,
                    "Weather_wind_intensity": actor_info.wind_intensity,
                    "Weather_sun_azimuth_angle": actor_info.sun_azimuth_angle,
                    "Weather_sun_altitude_angle": actor_info.sun_altitude_angle,
                    "Weather_fog_density": actor_info.fog_density,
                    "Weather_fog_distance": actor_info.fog_distance,
                    "Weather_wetness": actor_info.wetness,
                    "Weather_fog_falloff": actor_info.fog_falloff,
                    "Weather_scattering_intensity": actor_info.scattering_intensity,
                    "Weather_mie_scattering_scale": actor_info.mie_scattering_scale,
                    "Weather_rayleigh_scattering_scale": actor_info.rayleigh_scattering_scale,
                    "Weather_dust_storm": actor_info.dust_storm,
                    "Type": actor.type_id,
                    "Actor_Content": save_info.format_trafficLight(actor_info.sensor_location, actor_info.sensor_rotation,actor_info.sensor_listen, actor_info.sensor_type_id)
                })

    def save_collision_info(frame,timestamp,actorID,actorType,other_ActorID,other_ActorType,collisionPos,collisionDegree):
        with open(f"{sharedGlobal.directory}{sharedGlobal.datetime}/Hazards_and_Issues/collision_info.csv",'a') as file:
            writer=csv.DictWriter(file,fieldnames=fieldnames_collision)
            writer.writerow({
                "Frame":frame,
                "Timestamp":timestamp,
                "ActorID":actorID,
                "ActorType":actorType,
                "Other_ActorID":other_ActorID,
                "Other_ActorType":other_ActorType,
                "CollisionPos":collisionPos,
                "CollisionDegree":collisionDegree
            })

    def save_lane_invasion_info(frame,timestamp,actorID,actorType,laneMarking,laneInvasionPos):
        with open(f"{sharedGlobal.directory}{sharedGlobal.datetime}/Hazards_and_Issues/lane_invasion_info.csv",'a') as file:
            writer=csv.DictWriter(file,fieldnames=fieldnames_laneInvasion)
            writer.writerow({
                "Frame":frame,
                "Timestamp":timestamp,
                "ActorID":actorID,
                "ActorType":actorType,
                "LaneMarking":save_info.format_laneMarking(laneMarking),
                "LaneInvasionPos":laneInvasionPos
            })

    def save_obstacle_info(frame,timestamp,actorID,actorType,other_ActorID,other_ActorType,distance):
        with open(f"{sharedGlobal.directory}{sharedGlobal.datetime}/Hazards_and_Issues/obstacle_info.csv",'a') as file:
            writer=csv.DictWriter(file,fieldnames=fieldnames_obstacle)
            writer.writerow({
                "Frame":frame,
                "Timestamp":timestamp,
                "ActorID":actorID,
                "ActorType":actorType,
                "Other_ActorID":other_ActorID,
                "Other_ActorType":other_ActorType,
                "Distance":distance
          })

    def save_run_red_light(frame,timastamp,actorID,actorType,trafficLightID,pos,actorVelocity):
        with open(f"{sharedGlobal.directory}{sharedGlobal.datetime}/Hazards_and_Issues/traffic_light_info.csv",'a') as file:
            writer=csv.DictWriter(file,fieldnames=fieldnames_trafficLight)
            writer.writerow({
                "Frame":frame,
                "Timestamp":timastamp,
                "ActorID":actorID,
                "ActorType":actorType,
                "TrafficLightID":trafficLightID,
                "TrafficLightPos":pos,
                "ActorVelocity":actorVelocity
            })

    def save_exceed_speed(frame,timestamp,actorID,actorType,speedLimit,velocity):
        with open(f"{sharedGlobal.directory}{sharedGlobal.datetime}/Hazards_and_Issues/exceed_speed_limit_info.csv",'a') as file:
            writer=csv.DictWriter(file,fieldnames=fieldnames_speedLimit)
            writer.writerow({
                "Frame":frame,
                "Timestamp":timestamp,
                "ActorID":actorID,
                "ActorType":actorType,
                "SpeedLimitValue(km/h)":speedLimit,
                "Velocity":velocity
            })

    def save_acceleration_change(frame,timestamp,actorID,actorType,DeltaAcceleration,pos,label):
        with open(f"{sharedGlobal.directory}{sharedGlobal.datetime}/Hazards_and_Issues/acceleration_change_info.csv",'a') as file:
            writer=csv.DictWriter(file,fieldnames=fieldnames_acceleration_change)
            writer.writerow({
                "Frame":frame,
                "Timestamp":timestamp,
                "ActorID":actorID,
                "ActorType":actorType,
                "DeltaAcceleration(m/s)":DeltaAcceleration,
                "ChangePos":pos,
                "MayRapidAcceleration/MayRapiDeceleration":label
            })

    def save_no_response(frame,timestamp,actorID,actorType,actorLocation,actorRotation):   
        with open(f"{sharedGlobal.directory}{sharedGlobal.datetime}/Hazards_and_Issues/no_response_info.csv",'a') as file:
            writer=csv.DictWriter(file,fieldnames=fieldnames_noresponse)
            writer.writerow({
              "Frame": frame,
              "Timestamp": timestamp,
              "ActorID": actorID,
              "ActorType": actorType,
              'NoResponseLocation':actorLocation,
              'NoResponseRotation':actorRotation
            })

    def save_sharp_turning(frame,timestamp,actorID,actorType,lateral_acceleration,delta_angle,Velocity):
        with open(f"{sharedGlobal.directory}{sharedGlobal.datetime}/Hazards_and_Issues/sharp_turning_info.csv",'a') as file:
            writer=csv.DictWriter(file,fieldnames=fieldnames_sharpturn)
            writer.writerow({
                "Frame":frame,
                "Timestamp":timestamp,
                "ActorID":actorID,
                "ActorType":actorType,
                "Lateral_acceleration":lateral_acceleration,
                "TurnAngle":delta_angle,
                "Velocity":Velocity
            })

    def save_wrong_way(frame,timestamp,actorID,actorType,LandID,Location,VehicleDirection,LaneDirection):
        with open(f"{sharedGlobal.directory}{sharedGlobal.datetime}/Hazards_and_Issues/wrong_way_info.csv",'a') as file:
            writer=csv.DictWriter(file,fieldnames=fieldnames_wrong_way)
            writer.writerow({
              "Frame":frame,
              "Timestamp":timestamp,
              "ActorID":actorID,
              "ActorType":actorType,
              "LandID":LandID,
              "Location":Location,
              "VehicleDirection":VehicleDirection,
              "LaneDirection":LaneDirection
            })


