output "instance_dns" {
    description = "DNS of the instance"
    value = aws_instance.instance_mw.public_dns
}