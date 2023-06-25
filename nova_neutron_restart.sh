#!/bin/bash

restart_services() {
    local node_name=$1
    echo "Node: $node_name"
    ssh "$node_name" "service nova-compute restart; sleep 5; service neutron-openvswitch-agent restart"
}

# Get the list of node names
node_names=$(fuel node list | grep compute | awk '{print $5}')

# Iterate over each node name and restart services
for node_name in $node_names; do
    restart_services "$node_name"
done
