data "aws_vpc" "existing_vpc" {
  id = "VPC-ID"
}

data "aws_subnet" "existing_subnet" {
  id = "SUBNET-ID"
}

resource "aws_key_pair" "key_mw" {
  key_name   = "key_mw"
  public_key = file("~/.ssh/id_rsa.pub")
}

resource "aws_security_group" "sg_mw" {
  name_prefix = "sg_mw_"
  vpc_id = data.aws_vpc.existing_vpc.id
  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "instance_mw" {
  ami                    = "ami-06e46074ae430fba6"
  instance_type          = "t2.small"
  subnet_id              = data.aws_subnet.existing_subnet.id
  vpc_security_group_ids = [aws_security_group.sg_mw.id]
  key_name               = aws_key_pair.key_mw.key_name

  tags = {
    Name = "EC2 Maintenance Window Status"
  }
  connection {
    type        = "ssh"
    user        = "ec2-user"
    private_key = file("~/.ssh/id_rsa")
    timeout     = "5m"
    host        = self.public_ip
  }

  provisioner "file" {
    source      = "../script.sh"
    destination = "/tmp/script.sh"
  }
  provisioner "file" {
    source      = "../app.py"
    destination = "/tmp/app.py"
  }
  provisioner "file" {
    source      = "../templates/index.html"
    destination = "/tmp/index.html"
  }
  provisioner "file" {
    source      = "../static/styles/style.css"
    destination = "/tmp/style.css"
  }
  provisioner "file" {
    source      = "../static/scripts.js"
    destination = "/tmp/scripts.js"
  }
  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/script.sh",
      "sudo /tmp/script.sh",
    ]
  }

  lifecycle {
    ignore_changes = [subnet_id, vpc_security_group_ids]
  }
}