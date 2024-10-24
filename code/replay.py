import carla
import math
client=carla.Client('localhost',2000)
client.set_timeout(10.0)
world=client.get_world()
replay_file='20240917133158_recording.log'
client.replay_file(replay_file,0,0,197,True)
spectator=world.get_spectator()
# while True:
    # vehicles=world.get_actors().filter('vehicle.*')
    # vehicle=vehicles[0]
    # transform=vehicle.get_transform()
    # spectator.set_transform(
    #   carla.Transform(transform.location + carla.Location(x=-10 * math.cos(math.radians(transform.rotation.yaw)),
    #                                                       y=-10 * math.sin(math.radians(transform.rotation.yaw)),
    #                                                       z=5),
    #                   carla.Rotation(pitch=-30, yaw=transform.rotation.yaw)))
