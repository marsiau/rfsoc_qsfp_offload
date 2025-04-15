overlay_name := qsfp_radio
design_name := qsfp_radio
NOW := $(shell date +"%d-%m-%y_%H-%M")


all: clean export_overlay

project:
	vivado -mode batch -source make_project.tcl -tclargs $(overlay_name) -notrace

block_design: project
	vivado -mode batch -source make_block_design.tcl -tclargs $(overlay_name) $(design_name) -notrace

overlay: block_design
	mkdir overlay
	mkdir logs
	vivado -mode batch -source make_overlay.tcl -notrace 2>&1 | tee ./logs/bitstream_build_$(NOW).log

export_overlay overlay:
	vivado -mode batch -source export_overlay.tcl -tclargs $(overlay_name) $(design_name) -notrace

export_bd:
	vivado -mode batch -source export_bd.tcl -tclargs $(overlay_name) $(design_name) -notrace

open:
	vivado ./$(overlay_name)/$(overlay_name).xpr
clean:
	-rm -rf $(overlay_name) .Xil
	-rm -rf *.jou *.log NA
