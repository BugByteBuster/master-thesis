#!/bin/bash

delete_ports() {
    for PORT in $(neutron port-list | grep -v "atlas" | awk '{print $2}')
    do
        echo "Deleting PORT: $PORT"
        neutron port-delete $PORT
    done
}

delete_subnets() {
    for subnet in $(neutron subnet-list | grep -v "provider" | awk '{print $2}')
    do
        echo "Deleting subnet $subnet"
        neutron subnet-delete $subnet
    done
}

delete_networks() {
    for net in $(neutron net-list | grep -v "provider" | awk '{print $2}')
    do
        echo "Deleting net $net"
        neutron net-delete $net
    done
}

# Call the functions
delete_ports
delete_subnets
delete_networks
