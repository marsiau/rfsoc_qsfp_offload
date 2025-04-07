# Deal with arguments
set overlay_name [lindex $argv 0]
set design_name [lindex $argv 1]

# Open project
open_project ./${overlay_name}/${overlay_name}.xpr
open_bd_design ./${overlay_name}/${overlay_name}.srcs/sources_1/bd/${design_name}/${design_name}.bd

# Figure out the location & write the block design
set project_dir [get_property DIRECTORY [current_project]]
write_bd_tcl -force ${project_dir}/../${design_name}.tcl
