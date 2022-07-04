Provides scripts useful for workspace management of a CHRIS software setup.

* `ros2 run chris_scripts chris_status.sh`
  * scans workspace src folder and does systematic `git status` to check if changes on desired branch

* `ros2 run chris_scripts chris_update.sh`
  * Uses wstool to perform `git pull` on repos installed using `rosinstall` files
  * The standard `chris_install` set up will create the `rosinstall` files with specified target versions

* `ros2 run chris_scripts log_params.py`
  * Simple python script to request all parameters and document.
  * has option to verify value (e.g. use_sim_time) across all nodes
  * writes complete set to `~/.ros` by default


The `setup.bash` created by `chris_install` will add the `chris_scripts` library path to the system path
to allow directly invoking the scripts.
