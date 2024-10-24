import math
import os
import signal
import numpy as np

from saveInfo import save_info
import sharedGlobal
import carla
from getInfo import get_info
class event_info:
    def collisionEvent_info(self,CollisionEvent):
        self.frame_ID=CollisionEvent.frame
        self.timestamp=CollisionEvent.timestamp
        self.collision_actor=CollisionEvent.actor
        self.collision_other_actor=CollisionEvent.other_actor
        self.collision_degree=CollisionEvent.normal_impulse
        self.collision_pos=self.collision_actor.get_transform().location
        save_info.save_collision_info(self.frame_ID,self.timestamp,self.collision_actor.id,self.collision_actor.type_id,
                                      self.collision_other_actor.id,self.collision_other_actor.type_id,self.collision_pos,self.collision_degree)

    def laneInvasionEvent_info(self,LaneInvasionEvent):
      self.frame_ID = LaneInvasionEvent.frame
      self.timestamp = LaneInvasionEvent.timestamp
      self.laneinvasion_actor=sharedGlobal.global_vehicle
      self.lane_type=LaneInvasionEvent.crossed_lane_markings
      self.laneinvasion_pos=self.laneinvasion_actor.get_transform().location
      save_info.save_lane_invasion_info(self.frame_ID,self.timestamp,self.laneinvasion_actor.id,self.laneinvasion_actor.type_id,
                                        self.lane_type,self.laneinvasion_pos)

    def obstacleDetect_info(self,obstacleDetect):
      self.frame_ID=obstacleDetect.frame
      self.timestamp=obstacleDetect.timestamp
      self.detect_actor=obstacleDetect.actor.parent
      self.obstacle_actor=obstacleDetect.other_actor
      self.distance=obstacleDetect.distance
      save_info.save_obstacle_info(self.frame_ID,self.timestamp,self.detect_actor.id,self.detect_actor.type_id,self.obstacle_actor.id,
                                    self.obstacle_actor.type_id,self.distance)

    def traffic_light_state_detect(frame_id,timestamp,vehicle):
      vehicle_info=get_info()
      vehicle_info.get_vehicle_info(vehicle)
      velocity=math.sqrt(vehicle_info.v_velocity.x**2+vehicle_info.v_velocity.y**2+vehicle_info.v_velocity.z**2)
      if vehicle.is_at_traffic_light():    ##Not considering the situation where the vehicle cannot detect the signal lights
          sharedGlobal.has_light=True
          traffic_light=vehicle.get_traffic_light()
          sharedGlobal.traffic_light_id=vehicle.get_traffic_light().id
          sharedGlobal.traffic_light_location=vehicle.get_traffic_light().get_location()
          if traffic_light.get_state() == carla.TrafficLightState.Red:
              sharedGlobal.light_is_red=True
              if velocity > 0:
                sharedGlobal.has_velocity=True
                sharedGlobal.velocity.append(velocity)
                transform = vehicle_info.v_location
                if transform.x != sharedGlobal.pre_transform.x or transform.y != sharedGlobal.pre_transform.y or transform.z != sharedGlobal.pre_transform.z:
                  sharedGlobal.has_move=True
                  sharedGlobal.pre_transform=transform
                else:
                  sharedGlobal.has_move=False
                  sharedGlobal.pre_transform=transform

              else:
                sharedGlobal.has_velocity=False
                sharedGlobal.velocity.append(velocity)
          else:
            sharedGlobal.light_is_red=False
      else:
          if sharedGlobal.has_light:
              if sharedGlobal.light_is_red:
                  if sharedGlobal.has_velocity:
                      if sharedGlobal.has_move:
                          #print(sharedGlobal.traffic_light_id)
                          save_info.save_run_red_light(frame_id,timestamp,vehicle.id,vehicle.type_id,sharedGlobal.traffic_light_id,sharedGlobal.traffic_light_location,sharedGlobal.velocity)
          sharedGlobal.velocity.clear()
          sharedGlobal.has_light=False
          sharedGlobal.light_is_red=False
          sharedGlobal.has_velocity=False
          sharedGlobal.has_move=False
          sharedGlobal.velocity.append(velocity)
          sharedGlobal.pre_transform = vehicle.get_transform().location

      #print(sharedGlobal.has_velocity,sharedGlobal.has_move,sharedGlobal.light_is_red,sharedGlobal.has_light,sharedGlobal.velocity)


    def exceed_speed_limit(frame,timestamp,vehicle):
        velocity=vehicle.get_velocity()
        speed_mps=math.sqrt(velocity.x**2+velocity.y**2+velocity.z**2)
        speed_kmh=speed_mps*3.6
        if speed_kmh > vehicle.get_speed_limit():
          save_info.save_exceed_speed(frame,timestamp,vehicle.id,vehicle.type_id,vehicle.get_speed_limit(),speed_kmh)

    def acceleretation_change(frame,timestamp,vehicle):
        label=None
        current=vehicle.get_acceleration()
        current_acceleration=math.sqrt(current.x**2+current.y**2+current.z**2)
        past_acceleration=math.sqrt(sharedGlobal.pre_acceleration.x**2+sharedGlobal.pre_acceleration.y**2+sharedGlobal.pre_acceleration.z**2)
        delta_acceleration=current_acceleration-past_acceleration
        sharedGlobal.pre_acceleration=current
        if delta_acceleration > 0:
            label=f"MayRapidAcceleration"
        else:
            label=f"MayRapiDeceleration"
        if abs(delta_acceleration) > 6:
            save_info.save_acceleration_change(frame,timestamp,vehicle.id,vehicle.type_id,delta_acceleration,vehicle.get_transform(),label)

    def exceed_time_response(frame,timestamp,vehicle):
        vehicle_info=get_info()
        vehicle_info.get_vehicle_info(vehicle)
        current_vehicle_info=(vehicle_info.v_location,vehicle_info.v_rotation,vehicle_info.v_velocity,vehicle_info.throttle,vehicle_info.brake,vehicle_info.steering,vehicle_info.hand_brake,vehicle_info.gear)
        current_location_x=current_vehicle_info[0].x
        current_location_y=current_vehicle_info[0].y
        current_location_z=current_vehicle_info[0].z
        current_rotation_pitch=current_vehicle_info[1].pitch
        current_rotation_yaw=current_vehicle_info[1].yaw
        current_rotation_roll=current_vehicle_info[1].roll
        current_velocity_x = current_vehicle_info[2].x
        current_velocity_y = current_vehicle_info[2].y
        current_velocity_z = current_vehicle_info[2].z
        current_throttle=current_vehicle_info[3]
        current_brake = current_vehicle_info[4]
        current_steering = current_vehicle_info[5]
        current_hand_brake = current_vehicle_info[6]
        current_gear = current_vehicle_info[7]
        pre_location_x = sharedGlobal.no_response_prerecord[0].x
        pre_location_y = sharedGlobal.no_response_prerecord[0].y
        pre_location_z = sharedGlobal.no_response_prerecord[0].z
        pre_rotation_pitch = sharedGlobal.no_response_prerecord[1].pitch
        pre_rotation_yaw = sharedGlobal.no_response_prerecord[1].yaw
        pre_rotation_roll = sharedGlobal.no_response_prerecord[1].roll
        pre_velocity_x = sharedGlobal.no_response_prerecord[2].x
        pre_velocity_y = sharedGlobal.no_response_prerecord[2].y
        pre_velocity_z = sharedGlobal.no_response_prerecord[2].z
        pre_throttle = sharedGlobal.no_response_prerecord[3]
        pre_brake = sharedGlobal.no_response_prerecord[4]
        pre_steering = sharedGlobal.no_response_prerecord[5]
        pre_hand_brake = sharedGlobal.no_response_prerecord[6]
        pre_gear = sharedGlobal.no_response_prerecord[7]
        if current_location_x == pre_location_x and current_location_y == pre_location_y and current_location_z == pre_location_z and current_rotation_pitch == pre_rotation_pitch and current_rotation_yaw == pre_rotation_yaw and current_rotation_roll == pre_rotation_roll and abs(current_velocity_x-pre_velocity_x)<0.0005 and abs(current_velocity_y-pre_velocity_y)<0.0005 and abs(current_velocity_z-pre_velocity_z)<0.0005 and current_throttle == pre_throttle and current_brake == pre_brake and current_steering == pre_steering and current_hand_brake == pre_hand_brake and current_gear == pre_gear:
            sharedGlobal.no_response_time+=1
            print(sharedGlobal.has_light_no_response_time)
            if sharedGlobal.has_light == False and sharedGlobal.no_response_time > 300:  #300帧都没任何动作，认为其无响应，保留帧信息
                save_info.save_no_response(frame,timestamp,vehicle.id,vehicle.type_id,vehicle.get_transform().location,vehicle.get_transform().rotation)
                os.kill(os.getpid(),signal.SIGINT)
            elif sharedGlobal.has_light:
                sharedGlobal.has_light_no_response_time += 1
                print(sharedGlobal.has_light_no_response_time)
                if sharedGlobal.has_light_no_response_time > 400:
                    save_info.save_no_response(frame, timestamp, vehicle.id, vehicle.type_id,
                                                vehicle.get_transform().location, vehicle.get_transform().rotation)
                    os.kill(os.getpid(), signal.SIGINT)
        else:
          sharedGlobal.no_response_time=0
          sharedGlobal.no_response_prerecord=current_vehicle_info

    import carla
    import numpy as np

    def sharp_turning(frame,timestamp,vehicle):
      velocity = vehicle.get_velocity()
      transform = vehicle.get_transform()
      rotation = transform.rotation
      velocity_vector = np.array([velocity.x, velocity.y, velocity.z])
      pitch_rad = np.radians(rotation.pitch)
      yaw_rad = np.radians(rotation.yaw)
      roll_rad = np.radians(rotation.roll)
      rotation_matrix = np.array([
        [np.cos(yaw_rad) * np.cos(pitch_rad),
         np.cos(yaw_rad) * np.sin(pitch_rad) * np.sin(roll_rad) - np.sin(yaw_rad) * np.cos(roll_rad),
         np.cos(yaw_rad) * np.sin(pitch_rad) * np.cos(roll_rad) + np.sin(yaw_rad) * np.sin(roll_rad)],
        [np.sin(yaw_rad) * np.cos(pitch_rad),
         np.sin(yaw_rad) * np.sin(pitch_rad) * np.sin(roll_rad) + np.cos(yaw_rad) * np.cos(roll_rad),
         np.sin(yaw_rad) * np.sin(pitch_rad) * np.cos(roll_rad) - np.cos(yaw_rad) * np.sin(roll_rad)],
        [-np.sin(pitch_rad), np.cos(pitch_rad) * np.sin(roll_rad), np.cos(pitch_rad) * np.cos(roll_rad)]
      ])
      body_velocity = np.dot(rotation_matrix, velocity_vector)
      if sharedGlobal.pre_turn_velocity is None:
        sharedGlobal.pre_turn_velocity = body_velocity
      delta_velocity = body_velocity - sharedGlobal.pre_turn_velocity
      sharedGlobal.pre_turn_velocity = body_velocity
      lateral_acceleration = delta_velocity[1]
      if lateral_acceleration > 5:
          delta_angle=rotation.yaw-sharedGlobal.pre_turn_angle
          if delta_angle > 10:
            if math.sqrt(velocity.x**2+velocity.y**2+velocity.z**2) > 10:
              save_info.save_sharp_turning(frame,timestamp,vehicle.id,vehicle.type_id,lateral_acceleration,delta_angle,velocity)  ##需要后续人工筛选得到的结果，给一个标签列。是不是急转弯的情况

    def wrong_way(frame,timestamp,vehicle):
      location = vehicle.get_location()
      map = sharedGlobal.global_world.get_map()
      waypoint = map.get_waypoint(location, project_to_road=True, lane_type=carla.LaneType.Driving)
      lane_direction = waypoint.transform.get_forward_vector()
      transform = vehicle.get_transform()
      yaw = transform.rotation.yaw
      vehicle_direction = carla.Vector3D(x=math.cos(math.radians(yaw)), y=math.sin(math.radians(yaw)), z=0)
      dot_product = lane_direction.x * vehicle_direction.x + lane_direction.y * vehicle_direction.y
      magnitude_lane = math.sqrt(lane_direction.x ** 2 + lane_direction.y ** 2)
      magnitude_vehicle = math.sqrt(vehicle_direction.x ** 2 + vehicle_direction.y ** 2)
      cos_theta = dot_product / (magnitude_lane * magnitude_vehicle)
      theta = math.acos(cos_theta) * 180 / math.pi
      if abs(theta) > 90:
          print(1)
          save_info.save_wrong_way(frame,timestamp,vehicle.id,vehicle.type_id,waypoint.road_id,location,vehicle_direction,lane_direction)
          os.kill(os.getpid(), signal.SIGINT)









