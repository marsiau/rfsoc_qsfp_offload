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
env PYNQ_REMOTE=1 BOARD=RFSoC4x2 PYNQ_JUPYTER_NOTEBOOKS=./notebooks pixi install
```

* Rebuild
```
pixi clean
pixi install
```

## PYNQ.remote
* <>.bin gets stored in `/lib/firmware`