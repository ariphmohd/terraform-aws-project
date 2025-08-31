
# VPC Module
module "vpc" {
  source         = "./modules/vpc"
  vpc_cidr       = var.vpc_cidr
  vpc_name       = var.vpc_name
  public_subnet  = var.public_subnet
  private_subnet = var.private_subnet
}

# EC2 Module
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