# Deal with arguments
set overlay_name [lindex $argv 0]
set design_name [lindex $argv 1]

# Open project
open_project ./${overlay_name}/${overlay_name}.xpr

# Make block design
source ./${design_name}.tcl