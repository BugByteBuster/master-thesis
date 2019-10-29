for PORT in $(neutron port-list | grep -v "atlas" | awk '{print $2}')
do
    echo Deleting PORT: $PORT
    neutron port-delete $PORT
done

for subnet in $(neutron subnet-list | grep -v "provider" | awk '{print $2}')
do
    echo Deleting subnet $subnet
    neutron subnet-delete $subnet
done

for net in $(neutron net-list | grep -v "provider" | awk '{print $2}')
do
    echo Deleting net $net
    neutron net-delete $net
done 
