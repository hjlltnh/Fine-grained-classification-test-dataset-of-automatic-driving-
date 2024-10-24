import carla
import time

client=None
world = None
actors = None
vehicle = None

def base_info():
    global client,world,actors,vehicle
    client = carla.Client('localhost', 2000)
    client.set_timeout(30.0)

    try:
        while True:
            world = client.get_world()

            actors = world.get_actors()
            vehicles = [actor for actor in actors if 'vehicle.' in actor.type_id]
            if vehicles:
                vehicle = vehicles[0]
                break
            else:
                time.sleep(1.0)
        return client,world,actors,vehicle
    except KeyboardInterrupt:
        print("Interrupted by user")
