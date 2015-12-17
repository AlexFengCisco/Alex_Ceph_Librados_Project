import rados

#confgile='' use default /etc/ceph/ceph.conf and use default /etc/ceph ceph.client.admin.keyring
cluster=rados.Rados(conffile='')

cluster.connect()
cluster_version=cluster.version()
print 'cluster version = '+str(cluster_version)
cluster_id=cluster.get_fsid()
print 'cluster id = '+cluster_id
print 'cluster monitor member = '+str(cluster.conf_get('mon initial members'))

cluster_stats = cluster.get_cluster_stats()

print 'Cluster status'
for k,v in cluster_stats.iteritems():
	print k,v


print 'list pools in cluster'
pools = cluster.list_pools()
for pool in pools:
	print pool

#cluster.create_pool('alexdata')
ioctx = cluster.open_ioctx('alexdata')

ioctx.write_full("alex_object", "Hello World!")
ioctx.write_full("cisco_object", "Hello cisco!")

print 'List object content in pool alexdata'

object_iterator = ioctx.list_objects()

while True:
	try:
		rados_object = object_iterator.next()
		print "Object contents = " + rados_object.read()
	except StopIteration:
		break

ioctx.close()
cluster.shutdown()
