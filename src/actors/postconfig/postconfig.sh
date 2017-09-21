CONTAINER_DIRECTORY=$1

cd $CONTAINER_DIRECTORY 

# Move hosts, so it can be used in docker 
mv etc/hosts etc/hosts.source
ln -s etc/hosts.source etc/hosts
