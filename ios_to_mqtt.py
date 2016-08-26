import sys
import paramiko
import select
import time
import paho.mqtt.client as mqtt
import flynn
import json
import paramiko
sys.path.append("/home/ubuntu/")

flag = False
host = "192.168.2.254"
data = {}

while flag == False :
    try :
        client = mqtt.Client()
        client.connect("173.38.154.151", 80, 60)
        flag=True
        client.loop_start()
    except :
        print "Waiting for connectivity"
	time.sleep(3)


while True :
	try:
        	ssh=paramiko.SSHClient()
        	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        	ssh.connect(host, port=22, username='cisco', password='!Cisc0_')
        	#print "Connected to %s" % host
	except paramiko.AuthenticationException:
        	print "Authentication failed when connecting to %s" % host
        	sys.exit(1)
	except:
        	print "Could not SSH to %s, waiting for it to start" % host
		# Send the command (non-blocking)
	stdin, stdout, stderr = ssh.exec_command("show processes memory")

	for line in stdout.readlines():
        	#print line.strip()
		if line.strip().find("Processor") == 0 :
			tab=line.split(" ")
		 	mem=tab[7]

	data['devid'] = '1122334455'
    	data['proto'] = 'tcp'
    	data['type'] = 'iox'
    	data['mem'] = mem
    	msg = json.dumps(data)
    	client.publish("adt/tcp/iox/1122334455", msg, qos=0, retain=False)
	time.sleep(3)
    # or with cbor - that should first go to our GW
    #enc = flynn.dumps(msg)
    #encArr = bytearray(enc)
    #client.publish("ioxsensor", encArr, qos=0, retain=False)ait for the command to terminate


#while not stdout.channel.exit_status_ready():
	# Only print data if there is data to read in the channel
#	if stdout.channel.recv_ready():
#		rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
#        	if len(rl) > 0:
            	# Print data from stdout
#        		print '-------------------------------'
#            		print stdout.channel.recv(65536)
#        		print '-------------------------------'