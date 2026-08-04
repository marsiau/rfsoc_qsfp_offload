## dev
PYNQ_REMOTE_DEVICES = "10.42.0.230"
BOARD = "RFSoC4x2"
clk files
.xsa

oot blocks
    qsfp.ol
    


## Pixi
*  Nuke
```
rm -rf .pixi pixi.lock
```

* Allow postscripts
```
pixi config set --local run-post-link-scripts insecure
```

* Install
```
env PYNQ_REMOTE=1 \
    BOARD=RFSoC4x2 \
    PYNQ_JUPYTER_NOTEBOOKS="$PWD/notebooks" \
    pixi install
```

* Rebuild
```
pixi clean
pixi install
```

## PYNQ.remote
* <>.bin gets stored in `/lib/firmware`
xclk files in ?

## 

mkdir -p notebooks

