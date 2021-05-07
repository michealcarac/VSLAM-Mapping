Official Documents can be found here: https://openvslam-community.readthedocs.io/_/downloads/en/latest/pdf/

Pre-Requisites:

#Note: j8 means 8 cores, use j# for your number of cores

#Note: OpenCV may need others, hence why a guide is linked

```
$ apt update -y
$ apt upgrade -y --no-install-recommends
```

# Basic dependencies
```$ apt install -y build-essential pkg-config cmake git wget curl unzip```

# g2o dependencies
```$ apt install -y libatlas-base-dev libsuitesparse-dev```

# OpenCV dependencies
```
$ apt install -y libgtk-3-dev
$ apt install -y ffmpeg
$ apt install -y libavcodec-dev libavformat-dev libavutil-dev libswscale-dev libavresample-dev
```

# Eigen dependencies
```$ apt install -y gfortran```

# Other dependencies
```$ apt install -y libyaml-cpp-dev libgoogle-glog-dev libgflags-dev```

# Pangolin dependencies
```

$ apt install -y libglew-dev
```

# Build Programs

Create a directory for all programs:

```
$ mkdir VSLAMdir && cd VSLAMdir
```
Eigen: 
```
$ cd /path/to/VSLAMdir
$ wget -q https://gitlab.com/libeigen/eigen/-/archive/3.3.7/eigen-3.3.7.tar.bz2
$ tar xf eigen-3.3.7.tar.bz2
$ rm -rf eigen-3.3.7.tar.bz2
$ cd eigen-3.3.7
$ mkdir -p build && cd build
$ cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local

$ make -j8
$ make install 
```
#NOTE: may need sudo for the $ make install

OpenCV:
```
$ cd /path/to/VSLAMdir
```
Follow guide to install OpenCV: https://learnopencv.com/install-opencv-3-4-4-on-ubuntu-18-04/ 
Make sure to CMAKE_INSTALL_PREFIX=/usr/local when running the cmake for OpenCV.
If you cannot find libjasper, run this:
```
$ echo "deb http://us.archive.ubuntu.com/ubuntu/ yakkety universe" | sudo tee -a /etc/apt/sources.list
$ echo "deb http://'old-releases.ubuntu.com/ubuntu/ yakkety universe" | sudo tee -a /etc/apt/sources.list
$ sudo apt-get update
```
Then, try to download the libjasper again. 

DBoW2:
```
$ cd /path/to/VSLAMdir
$ git clone https://github.com/OpenVSLAM-Community/DBoW2.git
$ cd DBoW2
$ mkdir build && cd build
$ cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local 

$ make -j8
$ make install
```
g2o:
```
$ cd path/to/VSLAMdir
$ git clone https://github.com/RainerKuemmerle/g2o.git
$ cd g2o
$ git checkout 9b41a4ea5ade8e1250b9c1b279f3a9c098811b5a
$ mkdir build && cd build
$ cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local -DCMAKE_CXX_FLAGS=-std=c++11 -DBUILD_SHARED_LIBS=ON -DBUILD_UNITTESTS=OFF -DBUILD_WITH_MARCH_NATIVE=OFF -DG2O_USE_CHOLMOD=OFF -DG2O_USE_CSPARSE=ON -DG2O_USE_OPENGL=OFF -DG2O_USE_OPENMP=ON 

$ make -j8
$ make install
```

Pangolin:
```
$ cd /path/to/VSLAMdir
$ git clone https://github.com/stevenlovegrove/Pangolin.git
$ cd Pangolin
$ git checkout ad8b5f83222291c51b4800d5a5873b0e90a0cf81
$ mkdir build && cd build
$ cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local 

$ make -j8
$ make install
```
OpenVSLAM:
```
$ cd /path/to/VSLAMdir
$ git clone https://github.com/2020fork/openvslam.git
$ cd openvslam
```
Replace the /examples/run_camera_localization with our modified Settings/run_camera_localization
Add the Settings/orb_vocab folder to the openvslam directory
Add Settings/CameraConfig to the openvslam directory
In OPENVSLAM directory:
```
$ cmake -DBUILD_WITH_MARCH_NATIVE=OFF -DUSE_PANGOLIN_VIEWER=ON -DINSTALL_PANGOLIN_VIEWER=ON -DUSE_SOCKET_PUBLISHER=OFF -DUSE_STACK_TRACE_LOGGER=ON -DBOW_FRAMEWORK=DBoW2 -DBUILD_TESTS=ON -DBUILD_EXAMPLES=ON

$ make -j8
$ make install
```
Make a map: 
```
$ ./run_camera_slam -v ./orb_vocab/orb_vocab.dbow2 -n 2 -c ./cameraConfig/realsense60.yaml -p ../../ECELAB_map.msg
```
Note: Make sure the msg file is outside of VSLAM's directory as it may not create it due to permission issues
Run Localization on said map:
```
$ ./run_camera_localization -v ./orb_vocab/orb_vocab.dbow2 -n 2 -c ./cameraConfig/realsense60.yaml -p ../../ECELAB_map.msg
```

Note: For all map names, name them whatever you would like, but remember the names. Also good to put the maps into /data/
