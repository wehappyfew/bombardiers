__author__ = 'wehappyfew'

import subprocess,time
from jenkins_job import create_jenkins_xml_config, post_new_xml_config

# User provided vars
locustfile 			= "locustfile.py"
client_gh_username  = "wehappyfew"
client_repo_name 	= "bombardiers"
client_branch_name 	= "master" #should default to master

# I define these vars
client_id 	= "d52gvn5"
j_url  		= "http://aws-instance-ip" # normally www.bombardier.com
j_port 		= 8080
j_user 		= "jenkins"
j_pass 		= "bombardier"
job_name 	= "bombardier"
new_config 	= "{0}_config.xml".format(client_id)

# --Start the jenkins container--
j_name = "{0}-jenkins".format(client_id)
workspace_path = "/var/jenkins_home/jobs/bombardier/workspace"

subprocess.call(["docker", "run", "-d",
				 "--name", j_name,
				 "-p", "8080", # maps it to a random host port
				 "-v", workspace_path, # connect volume with locust container
				 "kostadis/bombardier:jenkins-gh" # TODO repo:image-tag
				])
time.sleep(10)

# --Grab the Jenkins random host port
port_cmd = "docker inspect --format '{{ (index (index .NetworkSettings.Ports \"8080/tcp\") 0).HostPort }}' {0}".format(j_name)
p = subprocess.Popen( port_cmd, stdout=subprocess.PIPE, shell=True )
(j_output, j_err) = p.communicate()
jenkins_random_port = j_output

# Set the user's username & repo URL
# The Jenkins container has setup the bombardier job and the Gh plugin
create_jenkins_xml_config(client_gh_username, client_repo_name, client_branch_name, filename=new_config )
post_new_xml_config(j_url,j_port,job_name,j_user,j_pass,new_config_path=new_config)

# --Start the locust container--
l_name = "{0}-locust".format(client_id)

subprocess.call(["docker", "run", "-d",
				 "--name", l_name,
				 "-p", "8089",
				 "--volumes-from", j_name, # attach jenkins workspace volume
				 "kostadis/bombardier:lbomb", # TODO
				 "locust", "-f", "{0}/{1}".format(workspace_path,locustfile), "--master"
				])
time.sleep(10)

# --Grab the locust web UI random host port
port_cmd = "docker inspect --format '{{ (index (index .NetworkSettings.Ports \"8089/tcp\") 0).HostPort }}' {0}".format(l_name)
p = subprocess.Popen( port_cmd, stdout=subprocess.PIPE, shell=True )
(l_output, l_err) = p.communicate()
locust_random_port = l_output

print locust_random_port