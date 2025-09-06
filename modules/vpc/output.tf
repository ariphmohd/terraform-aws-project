#This file defines the outputs for the VPC module.
#It provides the VPC ID, public and private subnet IDs, and the default security group ID.


output "vpc_id" {
  value = aws_vpc.this.id
}

output "public_subnet_id" {
  value = aws_subnet.public.id
}

output "private_subnet_id" {
  value = aws_subnet.private.id
}


output "default_sg_id" {
  value = aws_security_group.default.id
}
