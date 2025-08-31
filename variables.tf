variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "ap-south-1"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "vpc_name" {
  description = "Name tag for the VPC"
  type        = string
}

variable "public_subnet" {
  description = "CIDR block for public subnet"
  type        = string
}

variable "private_subnet" {
  description = "CIDR block for private subnet"
  type        = string
}

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

variable "instance_name" {
  description = "Tag name for the EC2 instance"
  type        = string
}


variable "private_key_path" {
  description = "Path to private key file for Ansible SSH"
  type        = string
}

variable "ec2_count" {
  description = "Number of EC2 instances to create"
  type        = number
  default     = 1
  
}