import carla
def show_all_log(filename):
    client=carla.Client('localhost',2000)
    client.set_timeout(10.0)
    log=client.show_recorder_file_info(filename,True)
    with open('record','w') as f:
      f.write(log)

show_all_log('20240804152023_recording.log')
