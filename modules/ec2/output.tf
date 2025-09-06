#This file defines the outputs for the EC2 instance module.
#It provides the instance ID and public IP address of the created EC2 instance.

output "instance_id" {
  value = aws_instance.this.id
}

output "public_ip" {
  value = aws_instance.this.public_ip
}

output "public_ips" {
  value = aws_instance.this[*].public_ip
}
