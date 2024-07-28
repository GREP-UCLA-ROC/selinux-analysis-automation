#!/bin/bash


# decompress gz into tar file
gzip -d eaman-neo4j-3.tar.gz

# load the image from tarball
docker image load < eaman-neo4j-3.tar

# find the ID of the image and run it in a container
docker run -d `docker images | grep eaman-neo4j-3 |  grep -o '[0-9a-f]\{12\}'`

# here, the ID and name of the running container will appear
docker ps

## OPTIONAL: kill the running container
## This assumes that you are not running any other containers
# docker kill `docker ps | grep -o '[0-9a-f]\{12\}' | head -1`

# commit current content in container to create a new image
# docker container commit [container-ID] [image_repo:image_tag]
