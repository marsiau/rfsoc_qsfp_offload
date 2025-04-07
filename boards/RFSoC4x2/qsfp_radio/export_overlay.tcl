# Deal with arguments
set overlay_name [lindex $argv 0]
set design_name [lindex $argv 1]

# Open project
open_project ./${overlay_name}/${overlay_name}.xpr
open_bd_design ./${overlay_name}/${overlay_name}.srcs/sources_1/bd/${design_name}/${design_name}.bd

set origin_dir [get_property DIRECTORY [current_project]]
set topname [current_bd_design]
set topwrapper [get_property top [current_fileset]]

set overlay_dir $origin_dir/../overlay
file mkdir -p $overlay_dir

# .bit
file copy -force $origin_dir/$overlay_name.runs/impl_1/$topwrapper.bit $overlay_dir/$overlay_name.bit
# .hwh
file copy -force $origin_dir/$overlay_name.srcs/sources_1/bd/$topname/hw_handoff/$topname.hwh $overlay_dir$overlay_name.hwh
