#!/bin/sh

if [ "$1" = "build" ]
then
  ./docker/compose_hooks/pre_build.sh
  docker-compose -f ./docker/docker-compose.yml $@
  ./docker/compose_hooks/post_build.sh
elif [ "$1" = "clean" ]
then
  docker container prune -f
  docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
else
  docker-compose -f ./docker/docker-compose.yml $@
fi