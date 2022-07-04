cmake_minimum_required(VERSION 3.5)
project(chris_scripts)

find_package(ament_cmake REQUIRED)

# Install bash launch scripts
install(PROGRAMS
  scripts/helper/chris_status.sh
  scripts/helper/chris_update.sh
  scripts/helper/log_params.py
  # NOTE: plot and record desktop scripts are not up to date, so don't install
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
