import paramiko

def connect_ssh(hostname, username, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hostname, username=username, password=password)
    return ssh_client

def execute_command(ssh_client, command):
    stdin, stdout, stderr = ssh_client.exec_command(command)
    return stdout.readlines()

def download_file(ssh_client, remote_path, local_path):
    ftp_client = ssh_client.open_sftp()
    ftp_client.get(remote_path, local_path)
    ftp_client.close()

def remove_file(ssh_client, remote_path):
    ssh_client.exec_command("rm -rf " + remote_path)

def main():
    hostname = "192.168.xx.xx"
    username = "XXXXX"
    password = "XXXXX"

    ssh_client = connect_ssh(hostname, username, password)
    print("SSH connection established.")

    command = "ls"
    output = execute_command(ssh_client, command)
    print(output)

    remote_path = "scr.sh"
    local_path = "/home/vidyadhar/scr.sh"
    download_file(ssh_client, remote_path, local_path)

    remove_file(ssh_client, remote_path)

    ssh_client.close()
    print("SSH connection closed.")


if __name__ == "__main__":
    main()

