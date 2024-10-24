import importlib
import sharedGlobal
from sharedGlobal import get_shareGlobal as get_Global

Global_client,Global_world,Global_actors,Global_vehicle=get_Global()


class get_info:
    def __init__(self):
        global Global_client,Global_world,Global_actors,Global_vehicle
        if Global_world:
          self.world=Global_world
    def get_weather_info(self):
        weather_info = self.world.get_weather()
        self.cloudiness = weather_info.cloudiness
        self.precipitation = weather_info.precipitation
        self.precipitation_deposits = weather_info.precipitation_deposits
        self.wind_intensity = weather_info.wind_intensity
        self.sun_azimuth_angle = weather_info.sun_azimuth_angle
        self.sun_altitude_angle = weather_info.sun_altitude_angle
        self.fog_density = weather_info.fog_density
        self.fog_distance = weather_info.fog_distance
        self.wetness = weather_info.wetness
        self.fog_falloff = weather_info.fog_falloff
        self.scattering_intensity = weather_info.scattering_intensity
        self.mie_scattering_scale = weather_info.mie_scattering_scale
        self.rayleigh_scattering_scale = weather_info.rayleigh_scattering_scale
        self.dust_storm = weather_info.dust_storm

    def get_vehicle_info(self,vehicle):
        self.transform = vehicle.get_transform()
        self.vehicle = vehicle
        self.v_location = self.transform.location
        self.v_rotation = self.transform.rotation
        self.v_velocity = self.vehicle.get_velocity()
        control=self.vehicle.get_control()
        self.throttle=control.throttle,
        self.brake=control.brake,
        self.steering=control.steer,
        self.hand_brake=control.hand_brake
        self.gear=control.gear
        self.control_info=f"('throttle':{self.throttle},'brake':{self.brake},'steering':{self.steering},'hand_brake':{self.hand_brake},'gear':{self.gear})"

    def get_spectator_info(self,spectator):
        self.s_location=spectator.get_transform().location
        self.s_rotation=spectator.get_transform().rotation

    def get_trafficLight_info(self,actor):
        self.light_state=actor.get_state()  
        self.light_elapsed_time=actor.get_elapsed_time()
        self.light_location=actor.get_transform().location
        self.light_rocation = actor.get_transform().rotation

    def get_trafficSign_info(self,actor):
        self.sign_location=actor.get_transform().location
        self.sign_rocation = actor.get_transform().rotation
        self.sign_type_id=actor.type_id

    def get_sensor_info(self,actor):
        self.sensor_location=actor.get_transform().location
        self.sensor_rotation=actor.get_transform().rotation
        self.sensor_type_id=actor.type_id
        self.sensor_listen=actor.is_listening()
