# AWS-Scripts

<b>Options Script: </b><br>
	. Start EC2 <br>
	. Stop EC2 <br>
	. Backup AMI EC2 ( With copy the tags ) <br>
	. Delete AMI EC2 <br>
	. Delete SnapShot Orphaned<br>
	. Delete Volume Orphaned<br>
	

<b>Examples:</b>

    -a --address	AWS Associated IP Public Instance (Start)
    -o --option		Option [ start | stop | restart | status | backup | delete (images) | visualizar = view (images) ]
    -f --filter		AWS Filter Name Images DELETAR
    -r --region		AWS Region (us-east-1 = Virginia / sa-east-1 = SaoPaulo / us-west-2 = Oregon )
    -i --id		AWS Access Key ID
    -k --key		AWS Secret Access Key
    -s --server		AWS Server ID  (i-01af2xx)
    -d --days		Delete/Visualizar AMI ( example =  AMI > 2 days )
    -c --account	AWS Account number
 
 
	1) [ Start | Stop | restart | backup ] Instance 
	    ./ec2-schedule.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -s i-01af2xx -o start
	    ./ec2-schedule.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -s i-01af2xx -o start -a 53.20.40.1 
	    ./ec2-schedule.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -s i-01af2xx -o backup 
  
  	2) [ Visualizar | Deletar | Contar | Delete SnapShot Orfao ] Images
            ./ec2-schedule.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -o contar -c '123456789'         
	    ./ec2-schedule.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -o visualizar -f "BACKUP*"         
	    ./ec2-schedule.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -o delete -f "BACKUP*"         
	    ./ec2-schedule.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -s i-01af2xx -o visualizar -f *BACKUP*        
	    ./ec2-schedule.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -s i-01af2xx -o delete -d 2        
	    ./ec2-schedule.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -o delete_snapshot_orfao 
	    ./ec2-schedule.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -o delete_vol_available 

For more information, my contact: eduardo@penetta.com

Thanks & regards
