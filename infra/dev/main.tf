locals {
  stage = var.stage
}

resource "aws_instance" "app_server" {
  ami           = "ami-0b36f01815a8c5ab1"
  instance_type = "t2.micro"
  key_name      = aws_key_pair.tf_key.key_name
  user_data     = <<-EOF
  	#!/usr/bin/bash
	sudo apt-get update -y
	sudo apt-get install ca-certificates curl
	sudo install -m 0755 -d /etc/apt/keyrings
	sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
	sudo chmod a+r /etc/apt/keyrings/docker.asc

	# Add the repository to Apt sources:
	echo \
	"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
	$(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
	sudo apt-get update
	sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
	sudo systemctl start docker
	sudo systemctl enable docker
	sudo docker -v
	sudo usermode -a -G docker $(whoami)
	newgrp docker
	docker run -d -p 80:80 --name nginx nginx:latest
  	EOF

  tags = {
    Name = "${local.stage}-application-server"
  }

}

resource "aws_key_pair" "tf_key" {
  key_name   = var.key_pair_name
  public_key = file("${path.module}/local-application-server.pub")
}


output "application_server_ip" {
  value = aws_instance.app_server.public_ip
}

output "application_server_username" {
  value = aws_instance.app_server.user_data
}
