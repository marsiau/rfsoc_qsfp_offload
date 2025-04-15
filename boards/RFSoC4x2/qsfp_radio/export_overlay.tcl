# Deal with arguments
set overlay_name [lindex $argv 0]
set design_name [lindex $argv 1]

# Open project
open_project ./${overlay_name}/${overlay_name}.xpr
open_bd_design ./${overlay_name}/${overlay_name}.srcs/sources_1/bd/${design_name}/${design_name}.bd

set origin_dir [get_property DIRECTORY [current_project]]
set topname [current_bd_design]
set topwrapper [get_property top [current_fileset]]

set overlay_dir ${origin_dir}/../overlay
file mkdir -p $overlay_dir

write_hw_platform -fixed -include_bit -force -file ${overlay_dir}/${overlay_name}.xsa