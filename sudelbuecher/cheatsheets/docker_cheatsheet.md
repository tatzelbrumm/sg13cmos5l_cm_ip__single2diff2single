# Docker command-line cheat sheet

Replace names in `<angle-brackets>` before running.

## Status and help

```bash
docker version                                  # client/server versions
docker info                                     # engine configuration and usage
docker info --format '{{.DockerRootDir}}'       # image/container/volume storage root
docker --help                                   # command overview
docker <command> --help                         # help for one command
docker ps                                       # running containers
docker ps -a                                    # all containers
docker images                                   # local images
docker system df                                # Docker disk usage
```

## Pull and tag images

```bash
docker pull <image>:<tag>                       # download a specific image/tag
docker pull <image>:latest                      # download/update latest tag
docker pull <image>:<other-tag>                 # reuses identical local layers
docker tag <image>:<old-tag> <image>:<new-tag>  # add local tag; no copy/download
```

## Start, stop, restart

```bash
docker start <container>                        # start existing container
docker stop <container>                         # stop gracefully
docker restart <container>                      # restart
docker pause <container>                        # freeze processes
docker unpause <container>                      # resume processes
docker kill <container>                         # force-stop immediately
```

## Run a new container

```bash
docker run <image>                              # run in foreground
docker run --rm <image>                         # remove after exit
docker run -it --rm <image> bash                # disposable interactive shell
docker run -d --name <name> <image>             # detached with a name
docker run -d --restart unless-stopped <image>  # restart across failures/reboots
docker run -p 8080:80 <image>                   # host 8080 -> container 80
docker run -e KEY=value <image>                 # set environment variable
docker run --env-file .env <image>              # load environment variables
docker run -w /work <image> <command>           # set working directory
docker run --user "$(id -u):$(id -g)" <image>   # use host UID/GID on Linux
```

## Share host files

```bash
docker run -v "$PWD:/work:rw" <image>                     # current directory -> /work
docker run -v /host/path:/container/path:ro <image>       # read-only bind mount
docker run --mount type=bind,src="$PWD",dst=/work <image> # explicit bind syntax
docker run -v <volume>:/data <image>                      # named Docker volume
docker volume create <volume>                             # create named volume
docker volume ls                                          # list volumes
docker volume inspect <volume>                            # inspect volume
```

## Work inside a running container

```bash
docker exec -it <container> bash                 # open Bash
docker exec -it <container> sh                   # open POSIX shell
docker exec <container> <command>                # run one command
docker exec -u root -it <container> bash         # shell as root
docker top <container>                           # container processes
docker stats                                     # live resource usage
docker stats <container>                         # one container
```

## Logs and inspection

```bash
docker logs <container>                          # print logs
docker logs -f <container>                       # follow logs
docker logs --tail 100 <container>               # last 100 lines
docker inspect <container>                       # full JSON metadata
docker inspect -f '{{.State.Status}}' <container> # print one field
docker port <container>                          # published ports
docker diff <container>                          # changed filesystem paths
docker events                                    # live engine events
```

## Copy files and images

```bash
docker cp <container>:/path/file ./file          # container -> host
docker cp ./file <container>:/path/file          # host -> container
docker export <container> -o container.tar       # export container filesystem
docker save <image> -o image.tar                 # save image and layers
docker load -i image.tar                         # load saved image
docker build -t <name>:<tag> .                   # build current directory
docker build --no-cache -t <name>:<tag> .        # rebuild without cache
docker build --progress=plain -t <name>:<tag> .  # verbose build output
docker push <registry>/<image>:<tag>             # upload image
docker history <image>                           # image layers
```

## Docker Compose

```bash
docker compose config                            # resolved configuration
docker compose pull                              # pull service images
docker compose build                             # build service images
docker compose build --no-cache                  # rebuild without cache
docker compose up                                # start in foreground
docker compose up -d                             # start detached
docker compose up -d --build                     # build and start
docker compose ps                                # service status
docker compose logs -f                           # follow all logs
docker compose logs -f <service>                 # follow one service
docker compose exec <service> bash               # shell in running service
docker compose run --rm <service> <command>      # one-off service command
docker compose restart <service>                 # restart service
docker compose stop                              # stop without removing
docker compose down                              # remove containers/networks
docker compose down --volumes                    # DELETES Compose volumes too
```

## Remove and clean up

```bash
docker rm <container>                            # remove stopped container
docker rm -f <container>                         # force-remove running container
docker image rm <image>                          # remove image
docker volume rm <volume>                        # remove volume
docker container prune                           # remove stopped containers; prompts
docker image prune                               # remove dangling images; prompts
docker volume prune                              # remove unused volumes; DATA LOSS
docker system prune                              # remove unused objects; prompts
docker system prune -a                           # remove all unused images too
```

## IIC-OSIC-TOOLS

```bash
docker pull hpretl/iic-osic-tools:2026.07
docker pull hpretl/iic-osic-tools:latest
docker tag hpretl/iic-osic-tools:latest hpretl/iic-osic-tools:2026.07
cd ~/EDA/IIC-OSIC-TOOLS && ./start_x.sh
cd ~/EDA/IIC-OSIC-TOOLS && ./start_vnc.sh
cd ~/EDA/IIC-OSIC-TOOLS && ./start_shell.sh
cd ~/EDA/IIC-OSIC-TOOLS && DESIGNS="$HOME/EDA" ./start_x.sh
cd ~/EDA/IIC-OSIC-TOOLS && CONTAINER_NAME=iic-magic DESIGNS="$HOME/EDA" ./start_x.sh
cd ~/EDA/IIC-OSIC-TOOLS && DOCKER_EXTRA_PARAMS="-v $HOME/EDA:/share:rw" ./start_x.sh
docker ps --filter 'name=iic-osic-tools'
docker exec -it <iic-container> bash
```

```bash
docker ps -a --filter 'name=iic-osic-tools-2026-07'                 # find running/stopped container
docker exec -it iic-osic-tools-2026-07 bash                        # additional container shell
xfce4-terminal &                                                    # additional GUI terminal; run inside container
cd ~/EDA/IIC-OSIC-TOOLS && DESIGNS="$HOME/EDA" DOCKER_TAG=2026.07 CONTAINER_NAME=iic-osic-tools-2026-07 ./start_x.sh
```

Closing the GUI terminal stops the X11 container but does not delete it or files bind-mounted under `/foss/designs`.

```bash
sak-pdk ihp-sg13cmos5l
cd /foss/designs/sg13cmos5l_ocd_ip__biasgen/magic && magic sg13cmos5l_ocd_ip__biasgen1.mag
cd /foss/designs/sg13cmos5l_ocd_ip__analog_switches/magic && magic power_stage.mag
cd /foss/designs/sg13cmos5l_ocd_openframe/magic && magic openframe_user_project.mag
```

## Telluride 2026

```bash
cd ~/EDA/Telluride/2026 && ./build_docker.sh
cd ~/EDA/Telluride/2026 && ./up.sh
cd ~/EDA/Telluride/2026 && ./up-vnc.sh
docker exec -it open-dvs-x11 bash
docker exec -it open-dvs-vnc bash
cd ~/EDA/Telluride/2026 && ./down.sh
cd ~/EDA/Telluride/2026 && docker compose config
```

Telluride maps `~/EDA/Telluride/2026` to `/share` and contains Sky130A, not `ihp-sg13cmos5l`.

## Quick diagnosis

```bash
docker ps -a --no-trunc
docker logs --tail 200 <container>
docker inspect -f '{{json .Mounts}}' <container>
docker inspect -f '{{json .NetworkSettings.Ports}}' <container>
docker stats --no-stream <container>
docker system df -v
```
