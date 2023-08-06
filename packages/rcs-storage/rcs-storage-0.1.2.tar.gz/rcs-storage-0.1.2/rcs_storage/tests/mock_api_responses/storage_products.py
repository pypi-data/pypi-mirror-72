# Result from response = requests.get('.../api/storage_products/')

# response.content
content = b'[{"name":"Market.Melbourne.Mediaflux","verbose_name":"Mediaflux"},{"name":"Ceph.S3","verbose_name":"S3 Object Storage"},{"name":"DaRIS","verbose_name":"DaRIS"},{"name":"NetApp.NFS","verbose_name":"NetApp NFS"},{"name":"NetApp.CIFS","verbose_name":"NetApp CIFS"}]'

# response.json()
json = [{'name': 'Market.Melbourne.Mediaflux', 'verbose_name': 'Mediaflux'}, {'name': 'Ceph.S3', 'verbose_name': 'S3 Object Storage'}, {'name': 'DaRIS', 'verbose_name': 'DaRIS'}, {'name': 'NetApp.NFS', 'verbose_name': 'NetApp NFS'}, {'name': 'NetApp.CIFS', 'verbose_name': 'NetApp CIFS'}]
