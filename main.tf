
# VPC Module
# This module creates a VPC with public and private subnets, a security group
# and an internet gateway. The VPC is tagged with the specified name for easy identification.

module "vpc" {
  source         = "./modules/vpc"
  vpc_cidr       = var.vpc_cidr
  vpc_name       = var.vpc_name
  public_subnet  = var.public_subnet
  private_subnet = var.private_subnet
}

# EC2 Module
# This module creates an EC2 instance with the specified parameter
# The EC2 instance is created in the public subnet and the provided security groups are attached
# The EC2 instance is also tagged with the specified name for easy identification


module "ec2" {
  source          = "./modules/ec2"
  ami_id          = var.ami_id
  instance_type   = var.instance_type
  key_name        = var.key_name
  subnet_id       = module.vpc.public_subnet_id
  security_groups = [module.vpc.default_sg_id]
  instance_name   = var.instance_name

}
  

# Generate Ansible inventory
# Ensure the inventory file is created in the ansible directory
# The inventory file will contain the public IPs of the EC2 instances
# and the path to the private key for SSH access

resource "local_file" "inventory" {
  filename = "${path.module}/../ansible/inventory.ini"
  content  = <<EOT
[ec2]
%{ for ip in module.ec2.public_ips ~}
${ip} ansible_user=ubuntu ansible_ssh_private_key_file=${var.private_key_path}
%{ endfor ~}
EOT
}

# Run Ansible automatically
# This resource runs an Ansible playbook to configure the EC2 instances
# It waits for the instances to be reachable via SSH before running the playbook
# The playbook is located in the ansible directory of the project


resource "null_resource" "run_ansible" {
  depends_on = [module.ec2, local_file.inventory]

  provisioner "local-exec" {
    command = <<EOT
      export ANSIBLE_HOST_KEY_CHECKING=False
      ansible -i ${path.module}/../ansible/inventory.ini all -m wait_for_connection -a "timeout=300"
      ansible-playbook -i ${path.module}/../ansible/inventory.ini ${path.module}/../ansible/site.yml
    EOT
  }
}