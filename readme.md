# Maintenance Window Update Status

Objective: Deploy a dashboard to monitor the status of the Maintenance Window instance update, making it easier and faster to monitor and focus on resolving the issues that come up with the failed instances.

**Before starting:**
- Login to AWS with the profile
- Create a key **id_rsa**
- Update the credential file in providers.tf

### 1. Go to terraform folder and start the environment 
```
terraform init
terraform apply
```

### 2. Update the **patch_group_(...)** and **ec2_dns** variables on **variables.py** with the respective command ids and EC2 DNS.

### 3. Open the Instance an run the app
```
cd myapp
python3 app.py
```

### 4. Run the fetch_status.py script locally
```
python fetch_status.py
```

### 5. Open the page on port 8080

example: ec2-100-10-100-100.compute-1.amazonaws.com:8080/

### 6. After finishing the MW, run terraform destroy
```
terraform destroy
```

**Confirm the changes to be done before appplying**