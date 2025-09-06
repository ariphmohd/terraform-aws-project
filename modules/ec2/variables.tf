#This file defines the input variables for the EC2 instance module.
#These variables are used to configure the EC2 instance properties.
#The values for these variables are defined in the terraform.tfvars file.


variable "ami_id" {
  description = "AMI ID for the EC2 instance"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
}

variable "key_name" {
  description = "Key pair name for SSH access"
  type        = string
}

variable "subnet_id" {
  description = "Subnet ID to launch instance in"
  type        = string
}

variable "security_groups" {
  description = "List of security groups for the instance"
  type        = list(string)
}

variable "instance_name" {
  description = "Tag name for the EC2 instance"
  type        = string
}

variable "disk_size" {
  description = "Size of the root disk in GB"
  type        = number
  default     = 20
  
}

