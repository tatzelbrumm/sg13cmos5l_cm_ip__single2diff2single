# IIC-OSIC-TOOLS command-line cheat sheet

## Pull image

```bash
docker pull hpretl/iic-osic-tools:2026.08
```

## Start with local X11

```bash
cd ~/EDA/IIC-OSIC-TOOLS
DESIGNS="$HOME/EDA" DOCKER_TAG=2026.08 CONTAINER_NAME=iic-osic-tools-2026-08-sw DOCKER_EXTRA_PARAMS='-e LIBGL_ALWAYS_SOFTWARE=1' ./start_x.sh
```

Host directory and container path:

```text
~/EDA  ->  /foss/designs
```

Start without display hangup safeguards

```bash
cd ~/EDA/IIC-OSIC-TOOLS
DESIGNS="$HOME/EDA" DOCKER_TAG=2026.08 CONTAINER_NAME=iic-osic-tools-2026-08 ./start_x.sh
```

Closing the graphical container terminal stops the X11 container.  
  
## Restart and restore X11

```bash
cd ~/EDA/IIC-OSIC-TOOLS
DESIGNS="$HOME/EDA" DOCKER_TAG=2026.08 CONTAINER_NAME=iic-osic-tools-2026-08-sw DOCKER_EXTRA_PARAMS='-e LIBGL_ALWAYS_SOFTWARE=1' ./start_x.sh
```
If stopped: press `s` to start. If still running with a dead X11 connection: press `s` to stop, then `s` to start.

## Start with local X11 and avoid display hangups

X11 fallback with software rendering; use a new container name:

```bash
cd ~/EDA/IIC-OSIC-TOOLS
DESIGNS="$HOME/EDA" DOCKER_TAG=2026.08 CONTAINER_NAME=iic-osic-tools-2026-08-sw DOCKER_EXTRA_PARAMS='-e LIBGL_ALWAYS_SOFTWARE=1' ./start_x.sh
```

Prefer VNC instead of direct X11/GPU forwarding:

```bash
cd ~/EDA/IIC-OSIC-TOOLS
DESIGNS="$HOME/EDA" DOCKER_TAG=2026.08 CONTAINER_NAME=iic-osic-tools-2026-08-vnc ./start_vnc.sh
```

```bash
vncviewer localhost:5901
```

```text
Password: abc123
```

## Restart and restore X11

Do not use `docker start` or `docker restart`. Rerun the host startup script so it can restore Xauthority:

```bash
cd ~/EDA/IIC-OSIC-TOOLS
DESIGNS="$HOME/EDA" DOCKER_TAG=2026.08 CONTAINER_NAME=iic-osic-tools-2026-08-sw DOCKER_EXTRA_PARAMS='-e LIBGL_ALWAYS_SOFTWARE=1' ./start_x.sh
```

If stopped: press `s` to start. If still running with a dead X11 connection: press `s` to stop, then `s` to start.

If an earlier `docker start` created the Xauthority source as a directory:

```bash
docker inspect -f '{{range .Mounts}}{{if eq .Destination "/headless/.xauthority"}}{{.Source}}{{end}}{{end}}' iic-osic-tools-2026-08-sw
sudo rmdir /tmp/<exact-path-printed-above>
```

Rerun `start_x.sh`. Container files persist, but stopped applications must be reopened.

## Open another terminal

From a host terminal:

```bash
docker exec -it iic-osic-tools-2026-08-sw bash
```

From the graphical container terminal opened by `start_x.sh`:

```bash
xfce4-terminal &
```

## Persistent aliases

Put aliases in the host-mounted startup file, not the container's `.bashrc`:

```bash
printf "%s\n" "alias lart='ls -lart'" >> "$HOME/EDA/.designinit"
```

Reload in an existing container:

```bash
source /foss/designs/.designinit
type lart
```

Alias syntax has no space after `=`:

```bash
alias lart='ls -lart'
```

## Container status

```bash
docker ps --filter 'name=iic-osic-tools'
docker ps -a --filter 'name=iic-osic-tools'
```

## Select process/PDK

Run inside the container:

```bash
sak-pdk ihp-sg13cmos5l
```

```bash
echo "$PDK"
echo "$PDK_ROOT"
echo "$PDKPATH"
```

Expected process:

```text
ihp-sg13cmos5l
```

## Generate Magic library cells for openframe

Run once inside the container after selecting the process:

```bash
cd /foss/designs/sg13cmos5l_ocd_openframe
./scripts/setup.sh
```

The script generates:

```text
magic/sg13cmos5l_io/
magic/sg13cmos5l_stdcell/
```

Open the padframe afterward:

```bash
cd /foss/designs/sg13cmos5l_ocd_openframe/magic
magic sg13cmos5l_padframe.mag
```
