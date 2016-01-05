#!/usr/bin/python

#  Desenvolvimento Penetta
#  Date: 05/10/2015
#  CSC 
#


import boto.ec2
import getopt
import sys
import time
import datetime
import re

version = '1.0'
verbose = False

#print 'ARGV      :', sys.argv[1:]
region = ''
id     = ''
key    = ''
server = ''
option = ''
address= ''
filter = ''
day    = ''

def usage():
    msg = """

    -a --address	      AWS Associated IP Public Instance (Start)
    -o --option 	      Option [ start | stop | restart | status | backup | delete (images) | visualizar (images) ]
    -f --filter		      AWS Filter Name  Images DELETAR
    -r --region   	      AWS Region (us-east-1 = USA / sa-east-1 = BR / us-west-2 = OREGON )
    -i --id                   AWS Access Key ID
    -k --key                  AWS Secret Access Key
    -s --server               AWS Server ID  (i-01af2xx)
    -d --days		      Delete/Visualizar AMI ( example =  AMI > 2 days )
    -c --account	      AWS Account number
 
    Exemplo:
 
	1) [ Start | Stop | restart | backup ] Instance 
	    ./ec2-penetta.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -s i-fc4d54ac -o start
	    ./ec2-penetta.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -s i-fc4d54ac -o start -a 53.20.40.1 
	    ./ec2-penetta.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -s i-fc4d54ac -o backup 

        2) [ Visualizar | Deletar | Contar | Delete SnapShot Orfao ] Images
            ./ec2-penetta.py -r us-east-1 -i YUYiUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -o contar -c '123456789'         
            ./ec2-penetta.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -o visualizar -f "BACKUP*"         
            ./ec2-penetta.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -o delete -f "BACKUP*"         
            ./ec2-penetta.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -s i-fc4d54ac -o visualizar -f *BACKUP*        
            ./ec2-penetta.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -s i-fc4d54ac -o delete -d 2        
            ./ec2-penetta.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -o delete_snapshot_orfao 
            ./ec2-penetta.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -o delete_vol_available 


    """
    print msg
    #print (time.strftime("%d-%m-%Y %H:%M:%S"))
    sys.exit(1)

try:
   options, args = getopt.gnu_getopt(sys.argv[1:], 'r:i:k:s:h:o:a:f:d:c:', ['region=','id=','key=','server=','help=','option=','address=','filter=','days=','account=',])

except getopt.GetoptError as err:
        # print help information and exit:
        #print(err) # will print something like "option -a not recognized"
	usage();
        sys.exit(2)

for opt, arg in options:
    
    if opt in ('-r', '--region'):
        region = arg
    elif opt in ('-i', '--id'):
        id = arg
    elif opt in ('-k', '--key'):
        key = arg
    elif opt in ('-s', '--server'):
        server = arg
    elif opt in ('-o', '--option'):
        option = arg
    elif opt in ('-a', '--address'):
        address = arg 
    elif opt in ('-f', '--filter'):
        filter = arg 
    elif opt in ('-d', '--days'):
        day = arg 
    elif opt in ('-c', '--account'):
        account = arg 
    elif opt in ('-h', '--help'):
        usage()
    else: 
	usage()

if region == '' or id == '' or key == '' :
  print ""
  print "----  CAMPOS INVALIDOS / VAZIOS --" 
  usage()
else:
  print ''
  print ''
  print 'REGION    :', region
  print 'ID        :', id
  print 'KEY       :', key
  print 'SERVER ID :', server
  print 'OPTION    :', option
  print 'ADDRESS IP:', address
  print 'FILTER    :', filter
  print 'DAYS      :', day

#### Conecte AWS 
conn = boto.ec2.connect_to_region(region,aws_access_key_id=id,aws_secret_access_key=key)

def startstopbackup ():

   #list_instances = conn.get_all_instances()
   list_instances = conn.get_all_instances(instance_ids=server)

   for res in list_instances:
      for inst in res.instances:
         name = inst.tags['Name'] if 'Name' in inst.tags else 'Unknown'
         #start_sched = inst.tags['auto:start'] if 'auto:start' in inst.tags else None

         # Verified is Server 
         if inst.id == server:			
            #print "%s (%s) [%s] {%s} [%s]" % (name, inst.id, inst.state, inst.image_id, inst.ip_address   )

	    # START INSTANCE
            if option == "start":
               if inst.state == "stopped":
	         conn.start_instances(server)
	         print "Server %s iniciando! " % (server)
	         # Sleep for a few seconds to ensure starting
	         time.sleep(10)
	         # Associate the Elastic IP with instance 
   	         if address:
	           conn.associate_address(server, address)
	           print "Server %s Associando IP %s " % (server, address)
               else:
                   print "Server %s ja estava INICIADO!!!! " % (server)

	    # RESTART INSTANCE
            elif option == "restart":
	       conn.reboot_instances(server)
	       print "Server %s reiniciando! " % (server)

	    # STOP INSTANCE
            elif option == "stop":
               if inst.state == "running":	
	          conn.stop_instances(server)
	          print "Server %s Desligando!!! " % (server)
               else:
	          print "Server %s ja ESTAVA DESLIGADO!!! " % (server)

	    # STATUS INSTANCE
            elif option == "status":
	       print ""
	       print "Server: %s  Status: %s  IP: %s " % (name, inst.state, inst.ip_address)
               print ""
	    
            # BACKUP VOLUME INSTANCE
            elif option == "backup":
               datatime = (time.strftime("%d/%m/%Y %H-%M-%S"))
               name_vl  = "[BACKUP-AGENDADO] %s - %s" % (server, datatime)
               descript = "BACKUP: %s" % (name)
	       image_id = conn.create_image(server, name=name_vl, description=descript, no_reboot=True)
	       #image_id = 'ami-a35c4cc2'
               print("Tagging image and snapshot wait ....")
	       while 1 :
                  img = conn.get_image(image_id)
                  if img.state == 'available':

		     ### LIST TAG INSTANCE
                     for tags in inst.tags: # search all tag instance
                       #print "%s: %s" % (tags, inst.tags[tags])
                       tag_name  = tags
                       tag_value = inst.tags[tags]
		       ### Add Tag IMAGE
                       img.add_tag(tag_name, tag_value)

		     ### SEARCH SNAMPSHOTS CREATOR BY IMAGE
		     snapshots = conn.get_all_snapshots(filters={'description':'*'+image_id+'*'})
		     #print 'entrou aqui : %s' % (snapshots)

		     ### LIST VOLUME SNAPSHOTS
		     for snaps in snapshots:
		       #print snaps.id,"-",snaps.start_time, "-",snaps.volume_size, "\n"

		       ### LIST TAG INSTANCE
		       for tags in inst.tags: # search all tag instance
		 	 #print "%s: %s" % (tags, inst.tags[tags])
			 tag_name  = tags
			 tag_value = inst.tags[tags]
			 ### Add Tag Snapshot
			 conn.create_tags(snaps.id,{tag_name: tag_value})

		     break

		  time.sleep(5)

	       print "Server %s Backup Image id = %s !!! Nome backup = %s , Descricao = %s" % (server, image_id, name_vl ,descript)
	 
         #else:			
         #   print "Servidor ( %s ) nao localizado! tente novamente." % (server) 


def limpaimagens ():

   ##list_imagens = conn.get_all_images()
   #if filter == '' and day != '' :
   if option == 'delete' :
     #print 'entrouuuuuu'
     date_now = datetime.datetime.now()
     day_old  = date_now - datetime.timedelta(days=int(day))

     for d in range(1,6):

        #search = date_now - datetime.timedelta(days=int(d))	     
        search = day_old - datetime.timedelta(days=int(d))	     
        search = search.strftime("%d/%m/%Y")
        search = "[BACKUP-AGENDADO] %s - %s*" % (server, search)
        print search
        list_imagens = conn.get_all_images(filters={'name' : search })

        if len(list_imagens) < 1:
          print "Imagem nao localizada!" 

        for images in list_imagens:
          #images.deregister(delete_snapshot=True)
          conn.deregister_image(images.id, delete_snapshot=True)
          print "Imagen sendo deletada (%s) - %s  - [%s] - {%s} (%s) ... " % (images.id,images.name, images.description,images.state,images.location)

     time.sleep(3)
     # DELETE ORPHAN SNAPSHOTS
     delete_orphan_snapshots()

   elif option == 'contar':
	list_imagens = conn.get_all_images(owners=account)
	print "Total de Imagens %s"  % len(list_imagens)
	#for images in list_imagens:
	#	 print "Imagen count  (%s) - %s  - [%s] - {%s} - (%s)  ... " % (images.id,images.name, images.description,images.state,images.location)   
   #else:
   elif option == 'visualizar':
     #list_imagens = conn.get_all_images(filters={'name' : '*AGENDADO*'})
     print filter
     list_imagens = conn.get_all_images(filters={'name' : filter })
     for images in list_imagens:
         print "Imagen visualizar  (%s) - %s  - [%s] - {%s} - (%s)  ... " % (images.id,images.name, images.description,images.state,images.location)


def delete_orphan_snapshots(vdryRun=True):
    #ec2conn = boto.ec2.connect_to_region("eu-west-1", profile_name=awsAccount)

    imageIds = []
    for image in conn.get_all_images(owners='self'):
        #print image.id, image.name + ", " + image.description
        #imageIds, imageNames = zip(*[(image.id, image.id)])
        imageIds.append(image.id)

    print 'Number of AMIs: '+str(len(imageIds))

    # Get list of snapshots and AMIs
    reAmi = re.compile('ami-[^ ]+')
    snapshots = []
    snapshotsToDelete = []
    snapshotsUnknown = []
    imageSnapshots = {}

    for snapshot in conn.get_all_snapshots(owner='self'):
        # Get id and image ID via regex.
        snapshotId = snapshot.id
        snapshotImageId = reAmi.findall(snapshot.description)
        if len(snapshotImageId) != 1:
            snapshotsUnknown.append(snapshotId)
        else:
            snapshotImageId = snapshotImageId[0]
            
        # Update lists
        snapshots.append(snapshotId)
        #print 'snapshotImageId: '+str(snapshotImageId)
        if snapshotImageId not in imageIds:
            snapshotsToDelete.append(snapshotId)
        else:
            if snapshotImageId in imageSnapshots:
                imageSnapshots[snapshotImageId].append(snapshotId)
            else:
                imageSnapshots[snapshotImageId] = [snapshotId]
    
    print 'Number of orphaned snapshots to delete: '+str(len(snapshotsToDelete))
    print 'Number of mapped snapshots to keep: '+str(len(imageSnapshots))
    
    if vdryRun == True:
        for snapshot in snapshotsToDelete:
            print 'Removing ' + snapshot + '...'
            conn.delete_snapshot(snapshot)



def delete_volume_available():

    print "Deleting volumes not used..."
    # List out the volumes
    vol_id = conn.get_all_volumes(volume_ids=None, filters=None)
    for volume in vol_id:
        #if volumes.attachment_state() == 'attached':
        #if volume.attachment_state() != 'attached':
        if volume.status == 'available':
            print "Volumes: "+ volume.id, volume.status
            #print volumes.attachment_state()
            conn.delete_volume(volume.id)



##### CHAMANDO AS FUNCOES
if option in ('backup', 'start', 'stop','status'):
   #print "BACKUP INSTANCE"
   startstopbackup()

elif option in ('delete','visualizar','contar'):
   print ''
   limpaimagens()

elif option in ('delete_snapshot_orfao'):
   #print  "IMAGES    : %s " % (option)
   delete_orphan_snapshots()

elif option in ('delete_vol_available'):
   #print  "IMAGES    : %s " % (option)
   delete_volume_available()

else:
   #print "OPCAO ESCOLHIDA ERRADA!"
   print "----  CAMPOS INVALIDOS --" 
   usage()


### DELET IMAGEM
   #images = connection.get_all_images(image_ids=['ami-cf86xxxx'])
   #images[0].deregister()

### STATUS INSTANCE
  #instance = conn.get_all_instances(instance_ids=['instance_id'])
  #print instance[0].instances[0].start()

### STOP INSTANCE
   #conn.stop_instances(instance_ids=['instance-id-1','instance-id-2', ...])

### START INSTANCE
   #conn.start_instances(instance_ids=['instance-id-1','instance-id-2', ...])
   # Sleep for a few seconds to ensure starting
   #sleep(10)
   # Associate the Elastic IP with instance 
   #if ip:
     # conn.associate_address(instance, ip)

