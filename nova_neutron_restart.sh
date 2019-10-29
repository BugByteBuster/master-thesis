for node_name in $(fuel node list | grep compute | awk '{print $5}' ); 
do
    echo Node: $node_name
    ssh ${node_name} "service nova-compute restart; sleep 5 ; service neutron-openvswitch-agent restart"
done
