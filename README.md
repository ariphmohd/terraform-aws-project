# Terraform AWS VPC and EC2 Setup

This project provisions AWS infrastructure using Terraform. It creates:
- A VPC with one **public subnet** and one **private subnet**.
- An Internet Gateway and Route Table for the public subnet.
- A Security Group to allow SSH and HTTP/HTTPS traffic.
- An EC2 instance in the public subnet.

---

## 📂 Folder Structure

├── main.tf # Root module calling child modules
├── variables.tf # Root module variables
├── outputs.tf # Root outputs
├── dev.tfvars # Example variable file for dev environment
├── modules
│ ├── vpc
│ │ ├── main.tf # VPC, Subnets, IGW, Route tables, Security Group
│ │ ├── variables.tf # VPC input variables
│ │ └── outputs.tf # VPC outputs
│ └── ec2
│ ├── main.tf # EC2 instance creation
│ ├── variables.tf # EC2 input variables
│ └── outputs.tf # EC2 outputs
└── README.md



---

## 🔑 Prerequisites

1. **Install Terraform**: [Terraform Install Guide](https://developer.hashicorp.com/terraform/downloads)  
2. **Install AWS CLI** and configure credentials:  
   ```bash
   aws configure

Provide your AWS Access Key, Secret Key, Region.
Create an AWS Key Pair in your target region:

aws ec2 create-key-pair --key-name jenkinserver --query "KeyMaterial" --output text > jenkinserver.pem
chmod 400 jenkinserver.pem

Update the key name in dev.tfvars.
Edit the dev.tfvars file with your values:

# VPC Configuration
vpc_cidr        = "10.0.0.0/16"
public_subnet   = "10.0.1.0/24"
private_subnet  = "10.0.2.0/24"
project         = "demo"
environment     = "dev"

# EC2 Configuration
ami_id          = "ami-0c1a7f89451184c8b"   # Replace with valid AMI in your region
instance_type   = "t2.micro"
key_name        = "jenkinserver"            # Your AWS key pair name



terraform plan -var-file="prod.tfvars"
terraform apply -var-file="prod.tfvars"
