# Fine-grained-classification-test-dataset-of-automatic-driving-system

We aim to create a high-coverage dataset that provides more targeted selection criteria for future researchers by finely partitioning driving scenarios. 

The fine-grained division includes but is not limited to road structures such as turning roads, ramps, lakes, intersections, roundabouts, etc. In the future, we will combine road structures with adverse weather conditions, not only focusing on ideal road conditions but also paying special attention to driving scenarios that are prone to danger, such as slippery slopes and lakes. 

In this way, we aim to provide more comprehensive data to support the safety test of the auto-drive system in different driving situations. We also offer data on the problem exposure of the monitoring system, which can visually show the status of the auto-drive system when the problem is exposed.

## Table of Contents

1.[Introduction](#introduction)  
2.[Data Download](#data-download)  
3.[Data Use](#data-use)  
4.[Citation](#citation)  

## Introduction

The dataset includes: car driving data that changes over time, actor data (including sensor data), records of various problem exposures, and log files that can be used for playback. All data in the driving scenario is saved in a timestamp folder. Driving scenes are classified according to road structure. And a map will store all types of road structures that exist. In addition, a map file also includes a starting point that records all driving scenes on the map.The overall framework is shown in the figure.

### Driving scene display
Some example videos are shown below:

### Straight Road
![](./examples/straight.gif)  

### Common Road
![](./examples/common_road.gif)  

### Ramp
![](./examples/ramp.gif)  

### Tunnel
![](./examples/Tunnel.gif)  

### circle
![](./examples/circle.gif)
## Data download

### Installation of Bridge
It was tested with Carla 0.9.14 and the Apollo v8.0.0 (v8.0.0),the operating system uses Ubuntu 20.04.6 LTS.
Refer to these link：  
https://blog.csdn.net/weixin_46336532/article/details/135017708,  
https://github.com/guardstrikelab/carla_apollo_bridge/blob/master/docs/GettingStarted.md

#### Prerequisites

* docker
```
sudo apt-get install docker.io
```
* NVIDIA Container Toolkit
```
curl https://get.docker.com | sh \
&& sudo systemctl --now enable docker
```
```
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
    && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
    && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
          sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
          sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```
```
sudo apt-get update
```
```
sudo apt-get install -y nvidia-docker2
```
```
sudo systemctl restart docker
```
 * docker-compose
```
 sudo curl -L "https://github.com/docker/compose/releases/download/v2.0.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
* Change File Permission
```
sudo chmod +x /usr/local/bin/docker-compose
```
#### Build And Run Apollo  
* Clone apollo v8.0.0
```
# Using SSH
git clone -b v8.0.0 git@github.com:ApolloAuto/apollo.git

#Using HTTPS
git clone -b v8.0.0 https://github.com/ApolloAuto/apollo.git
```
* Build Apollo
```
cd apollo
echo "export APOLLO_ROOT_DIR=$(pwd)" >> ~/.bashrc  && source ~/.bashrc
```
run:
```
sudo rm -rf /apollo/.cache
bash docker/scripts/dev_start.sh
```
Upon successful execution, you will see the following message
```
[ OK ] Congratulations! You have successfully finished setting up Apollo Dev Environment.
[ OK ] To login into the newly created apollo_dev_lei container, please run the following command:
[ OK ] bash docker/scripts/dev_into.sh
[ OK ] Enjoy!
```
Above If you occured error as "ERROR: Config value 'cuda' is not defined in any .rc file",you can try
```
./apollo.sh config -n
```
Run this command to enter the container
```
bash docker/scripts/dev_into.sh
```
Make the GPU version:
```
./apollo.sh build_gpu
```
After successful compilation, the following will be printed:
```
==============================================
[ OK ] Done building apollo. Enjoy!
==============================================
```
Run this command in the container to start Dreamview
```
./scripts/bootstrap.sh
```
Finally, open the link in your browser
```
http://localhost:8888/
```
#### Run Carla
* Clone the carla_apollo_bridge project outside Apollo container
```
# Using SSH
git clone git@github.com:guardstrikelab/carla_apollo_bridge.git

#Using HTTPS
git clone https://github.com/guardstrikelab/carla_apollo_bridge.git
```
Pull carla image and run
```
cd carla_apollo_bridge
./scripts/docker_run_carla.sh
```
#### Run carla_apollo_bridge
* Copy the src folder into Apollo container
```
docker cp carla_bridge <apollo_container_name>:/apollo/modules/carla_bridge
```
* Install carla_bridge  
Enter the Apollo container and run:
```
cd /apollo/modules/carla_bridge
chmod +x install.sh
./install.sh
source ~/.bashrc
```
* Start the bridge
```
python main.py
```

### Data Use
#### start a co-simulation
* Open the command prompt window
* Open the Apollo container and run it:
```
docker start apollo-dev-[username]/Apollo container name  
docker exec -it apollo-dev-[username]/Apollo container name /bin/bash
./scripts/bootstrap.sh
```
* Enter it in the website area of the browser to open the Dreamview website.
* Open apollo client: http://localhost:8888.
* If dreamview doesn't display the map, switch to carla_town04 and then switch back.
* (Optional) Select "Task" in the sidebar and turn on "Camera Sensor" in "Others".
* (Optional) Select "Layer Menu" in the sidebar and turn on "Point Cloud" in "Perception".
* Select "Module Controller" in the sidebar and turn on "Routing", "Planning", "Control", "Predict" module.

If you want to close Dreamview, run
```
./scripts/bootstrap.sh stop
```
* Open a new command prompt window:

* Open the Carla container:
```
docker start carla-simulator-1/carla container name
```
* Open a new command-line prompt window, run
```
docker exec -it apollo-dev-username/Apollo container name /bin/bash
```
Run the bridge
```
cd /apollo/modules/carla_bridge  
python main.py
```
If an error occurs, you can try using the statement: 
```
source /Apollo/cyber/setup.bash
```
Next, experiments can be conducted.
* Choose a path to save the downloaded dataset
* Open DOS in the selected path and use the command:
```
git lfs clone https://github.com/hjlltnh/Fine-grained-classification-test-dataset-of-automatic-driving-system.git
```
Please note that the 'dataset.zip' downloaded using the 'git clone' method cannot be used.
* Extract the dataset file from the folder, and select the timestamp folder you want to use to test the auto-drive-system according to the classified dataset.
* Place the timestamp file in the path:/apollo/modules/carla_bridge, copy the log file of the timestamp file corresponding to the dataset you want to use, such as 20240810145622_recording.log, to a certain location in the Carla container， We need to first open the Carla container,and then
```
docker cp /apollo/modules/carla_bridge/20240810145622_recording.log carla-simulator-1:/home/carla/.config/Epic/CarlaUE4/Saved/
```
* Copy the code folder to the path:
```
/apollo/modules/carla_bridge
```
* Open a new command prompt,enter the Apollo container,
* Open the replay.py file in the 'code' folder and replace the numbers in the 'replay_file=20240917133158_recording.log' sentence with the timestamp numbers you want,and then:
```
cd /apollo/modules/carla_bridge/code
```
and run
```
python replay.py
```
The other files with timestamps record the problems that occurred with Apollo, the information data of the cars controlled by Apollo, and the actor data in this timestamp folder.

## Citation
```
@inproceedings{dosovitskiy2017carla,
  title={CARLA: An open urban driving simulator},
  author={Dosovitskiy, Alexey and Ros, German and Codevilla, Felipe and Lopez, Antonio and Koltun, Vladlen},
  booktitle={Conference on robot learning},
  pages={1--16},
  year={2017},
  organization={PMLR}
}
```
```
@inproceedings{huang2018apolloscape,
  title={The apolloscape dataset for autonomous driving},
  author={Huang, Xinyu and Cheng, Xinjing and Geng, Qichuan and Cao, Binbin and Zhou, Dingfu and Wang, Peng and Lin, Yuanqing and Yang, Ruigang},
  booktitle={Proceedings of the IEEE conference on computer vision and pattern recognition workshops},
  pages={954--960},
  year={2018}
}
```
```
https://blog.csdn.net/weixin_46336532/article/details/135017708
```
```
https://github.com/guardstrikelab/carla_apollo_bridge/blob/master/docs/GettingStarted.md  
```
```
https://blog.csdn.net/condom10010/article/details/130386323
```
```
https://zhuanlan.zhihu.com/p/369780423
```
```
https://blog.csdn.net/weixin_44177594/article/details/126890190?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522BBE5EE0F-D9FF-40C4-8659-EAD3F37C8A28%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=BBE5EE0F-D9FF-40C4-8659-EAD3F37C8A28&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-10-126890190-null-null.142^v100^pc_search_result_base9&utm_term=carla%E5%9C%B0%E5%9B%BE%E8%BD%ACapollo&spm=1018.2226.3001.4187
```
```
https://blog.csdn.net/weixin_44177594/article/details/126890190?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522BBE5EE0F-D9FF-40C4-8659-EAD3F37C8A28%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=BBE5EE0F-D9FF-40C4-8659-EAD3F37C8A28&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-10-126890190-null-null.142^v100^pc_search_result_base9&utm_term=carla%E5%9C%B0%E5%9B%BE%E8%BD%ACapollo&spm=1018.2226.3001.4187
