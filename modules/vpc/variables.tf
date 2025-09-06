#This file defines the input variables for the VPC module.
#These variables are used to configure the VPC properties.
#The values for these variables are defined in the terraform.tfvars file.


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
