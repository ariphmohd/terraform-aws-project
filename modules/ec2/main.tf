resource "aws_instance" "this" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  key_name                    = var.key_name
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = var.security_groups
  associate_public_ip_address = true

  root_block_device {
    volume_size = var.disk_size
    volume_type = "gp3"
    delete_on_termination = true
  }
}
