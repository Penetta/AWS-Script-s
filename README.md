# AWS-Scripts

Examples:

    -a --address	    AWS Associated IP Public Instance (Start)
    -o --option 	    Option [ start | stop | restart | status | backup | delete (images) | visualizar (images) ]
    -f --filter		    AWS Filter Name  Images DELETAR
    -r --region   	  AWS Region (us-east-1 = USA / sa-east-1 = BR / us-west-2 = OREGON )
    -i --id           AWS Access Key ID
    -k --key          AWS Secret Access Key
    -s --server       AWS Server ID  (i-01af2xx)
    -d --days		      Delete/Visualizar AMI ( example =  AMI > 2 days )
    -c --account	    AWS Account number
 
 
	1) [ Start | Stop | restart | backup ] Instance 
	    ./ec2-schedule.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -s i-fc4d54ac -o start
	    ./ec2-schedule.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -s i-fc4d54ac -o start -a 53.20.40.1 
	    ./ec2-schedule.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -s i-fc4d54ac -o backup 
  
  2) [ Visualizar | Deletar | Contar | Delete SnapShot Orfao ] Images
      ./ec2-schedule.py -r us-east-1 -i YUYiUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -o contar -c '123456789'         
      ./ec2-schedule.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -o visualizar -f "BACKUP*"         
      ./ec2-schedule.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -o delete -f "BACKUP*"         
      ./ec2-schedule.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -s i-fc4d54ac -o visualizar -f *BACKUP*        
      ./ec2-schedule.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -s i-fc4d54ac -o delete -d 2        
      ./ec2-schedule.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -o delete_snapshot_orfao 
      ./ec2-penetta.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -o delete_vol_available 

For more information, my contact: eduardo@penetta.com

Thanks & regards