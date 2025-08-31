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
