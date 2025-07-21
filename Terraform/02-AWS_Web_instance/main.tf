# resource "aws_security_group" "web_sg" {
#   name        = "${var.project_name}-sg"
#   description = "Allow HTTP and SSH"

#   ingress {
#     description = "HTTP"
#     from_port   = 80
#     to_port     = 80
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }

#   ingress {
#     description = "SSH"
#     from_port   = 22
#     to_port     = 22
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }

#   egress {
#     from_port   = 0
#     to_port     = 0
#     protocol    = "-1"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
# }

# resource "aws_instance" "web" {
#   ami           = "ami-07b575563ed0b0d0c"
#   instance_type = var.instance_type
#   key_name      = var.key_name

#   vpc_security_group_ids = [aws_security_group.web_sg.id]

#   tags = {
#     Name = var.project_name
#   }
# }