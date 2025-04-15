set origin_dir "."
set project_part xczu48dr-ffvg1517-2-e
set board_part realdigital.org:rfsoc4x2:part0:1.0
set iprepo_dir $origin_dir/../../ip_repo

# Deal with arguments
set projectame [lindex $argv 0]

# Create project
create_project $projectame $origin_dir/$projectame -part $project_part
if { $board_part != "" } {
    set_property BOARD_PART $board_part [current_project]
}

set_property target_language VHDL [current_project]

# Set IP repo
set_property  ip_repo_paths $iprepo_dir [current_project]
update_ip_catalog
