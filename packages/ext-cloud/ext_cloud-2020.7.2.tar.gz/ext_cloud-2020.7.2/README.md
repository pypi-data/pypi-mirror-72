# ext_cloud
Multi cloud library in python 

* BaseCloud folder has abstact class for all cloud objects.Each BaseCloud class has abstract properties and abstract methods only forcing concrete class to implement them
* OpenStackBaseCloud has id and name property and all the openstack cloud object should be dervied from BaseCloud and OpenStackBaseCloud
