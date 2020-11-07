cmake_minimum_required(VERSION 2.8.3)
project(crane_x7_examples)
set(CMAKE_CXX_FLAGS "-std=c++11 ${CMAKE_CXX_FLAGS}")
find_package(catkin REQUIRED COMPONENTS
  rospy
  roscpp
  std_msgs
  geometry_msgs
  message_generation
)

add_service_files(FILES ObstacleAvoidance.srv)
generate_messages(DEPENDENCIES std_msgs geometry_msgs)

###################################
## catkin specific configuration ##
###################################
## The catkin_package macro generates cmake config files for your package
## Declare things to be passed to dependent projects
## INCLUDE_DIRS: uncomment this if your package contains header files
## LIBRARIES: libraries you create in this project that dependent projects also need
## CATKIN_DEPENDS: catkin_packages dependent projects also need
## DEPENDS: system dependencies of this project that dependent projects also need
catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES crane_x7_examples
 CATKIN_DEPENDS message_runtime
#  DEPENDS system_lib
)

###########
## Build ##
###########

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)
add_executable(main_node src/main_node.cpp)
target_link_libraries(main_node ${catkin_LIBRARIES})

#############
## Install ##
#############

install(PROGRAMS
  scripts/crane_x7_pick_and_place_demo.py
  scripts/gripper_action_example.py
  scripts/pose_groupstate_example.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
