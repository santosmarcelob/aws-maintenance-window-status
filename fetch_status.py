'''
    MONITOR THE RUN COMMAND FOR THE SPECIFIED COMMAND IDS
    AND LOG THE STATUS OF EACH INSTANCE (SUCCESS, FAILED, IN PROGRESS)

    Last update May 19 2023 - Marcelo Santos

'''

from variables import *
import time
import subprocess
from datetime import datetime, timedelta

# While loop to run continuously
while(True):
    with open('log.txt', 'w') as f:
        f.truncate(0)

    # Command ids of the Run Command
    command_ids = [
        patch_group_1_command_id,
        patch_group_2_command_id,
        patch_group_3_command_id,
        patch_group_4_command_id 
    ]
    patch_groups = {0: 'First', 1: 'Second', 2: 'Third', 3: 'Forth'}
    for i, command_id in enumerate(command_ids):
        aws_cli_command = 'aws ssm list-command-invocations --command-id "{0}" --details --query "sort_by(CommandInvocations[?CommandPlugins[0].ResponseFinishDateTime!=null], &CommandPlugins[0].ResponseFinishDateTime)[*].{{InstanceName: InstanceName, Status: Status, ResponseStartDateTime: CommandPlugins[0].ResponseStartDateTime, ResponseFinishDateTime: CommandPlugins[0].ResponseFinishDateTime}}" --profile PROFILE_NAME --output text'.format(command_id)
        
        aws_cli_command2 = 'aws ssm list-command-invocations --command-id "{0}" --details --query "CommandInvocations[?CommandPlugins[0].ResponseFinishDateTime==null].{{InstanceName: InstanceName, Status: Status}}" --profile PROFILE_NAME --output text'.format(command_id)

        try:
            result = subprocess.run(aws_cli_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = result.stdout.decode('utf-8')

            array_var = [line.split('\t') for line in output.split('\n') if line]
            #inprogress
            result2 = subprocess.run(aws_cli_command2, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output2 = result2.stdout.decode('utf-8')

            array_var2 = [line2.split('\t') for line2 in output2.split('\n') if line2]

        except subprocess.CalledProcessError as e:
            error = e.stderr.decode('utf-8')
            print(f"Error: {error}")

        with open(f'log.txt', 'a') as f:
            n = 0
            y = 0
            while n < len(array_var):
                patch_group = patch_groups.get(i, '')
                # Check for success status
                command_host = array_var[n][0]

                command_finishdatetime = array_var[n][1]
                handler_finishtime_starting = command_finishdatetime.find("T")+1
                handler_finishtime_ending = command_finishdatetime.find("T")+6
                finishtime = datetime.strptime((command_finishdatetime[handler_finishtime_starting:handler_finishtime_ending]), '%H:%M')
                finishtime_cet = str((finishtime + timedelta(hours=5)).time())[0:5]

                command_startdatetime = array_var[n][2]
                handler_starttime_starting = command_startdatetime.find("T")+1
                handler_starttime_ending = command_startdatetime.find("T")+6
                starttime = datetime.strptime((command_startdatetime[handler_starttime_starting:handler_starttime_ending]), '%H:%M')
                starttime_cet = str((starttime + timedelta(hours=5)).time())[0:5]

                command_result = array_var[n][3].strip()
                
                # Check for success status
                try:
                    if command_result == "Success":
                        print("\nPatch Group: {0} | Result: {1} | Host: {2} | Start: {3} Done: {4}".format(patch_group, command_result, command_host, starttime_cet, finishtime_cet), file=f)
                        n += 1
                except:
                    pass
                # Check for failed status
                try:
                    if command_result == "Failed":
                        print("\nPatch Group: {0} | Result: {1} | Host: {2} | Start: {3} Done: {4}".format(patch_group, command_result, command_host, starttime_cet, finishtime_cet), file=f)
                        n += 1
                except:
                    pass
                
                while y < len(array_var2):
                    # Check for in progress status
                    try:
                        if array_var2[y][1].strip() == "InProgress":
                            print("\nPatch Group: {0} | Result: {1} | Host: {2}".format(patch_group, array_var2[n][1].strip(), array_var2[y][0]), file=f)
                            y += 1
                    except:
                        pass
    source_file = "log.txt"
    destination_host = ec2_dns
    destination_path = "~/myapp/"
    subprocess.run(["scp", "-i", "id_rsa", source_file, f"ec2-user@{destination_host}:{destination_path}"])

    # Sleep for 2 minutes - 120 seconds
    time.sleep(120)