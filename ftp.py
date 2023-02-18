import pysftp
import paramiko

sysdir = "C:\\Users\\15601\\PycharmProjects\\covid-ml2\\"
def transfer(local_dir,target_dir):
    target_dir = "/home/ubuntu/COVID_19_Website/Data/"+target_dir
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    srv = pysftp.Connection(host="18.220.160.90", username="ubuntu",
                            private_key='./covid19risk_server.pem',cnopts=cnopts)

    # Get the directory and file listing
    #data = srv.listdir()
    srv.chdir(target_dir)
    print("transmitting ",sysdir+local_dir,"to", target_dir)
    srv.put(sysdir+local_dir)
    # Closes the connection

    srv.close()

    # client = paramiko.SSHClient()
    # client.load_system_host_keys()
    # client.set_missing_host_key_policy(paramiko.WarningPolicy)
    # client.connect(hostname='18.220.160.90', username='ubuntu', port=22,
    #                key_filename='./covid19risk_server.pem')
    #
    # # -------------------------- [ just for testing ] --------------------------
    # stdin, stdout, stderr = client.exec_command('ls -la')  # THIS IS FOR TESTING
    # print(stdout.read())


if __name__ == "__main__":
    transfer("cbsasdata.csv","predicted")