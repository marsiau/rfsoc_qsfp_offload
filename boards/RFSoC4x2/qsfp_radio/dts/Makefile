# ChatGPT

DTSS := $(wildcard *.dts)
DTBOS := $(DTSS:.dts=.dtbo)

all: $(DTBOS)

%.dtbo: %.dts
	dtc -I dts -O dtb -o $@ $< -q

# If you run 'make ddr4', this rule will trigger
$(DTBOS): %: %.dtbo

clean:
	rm -f $(DTBOS)
