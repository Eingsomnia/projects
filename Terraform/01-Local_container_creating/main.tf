# provider "docker" {}

# resource "docker_container" "busybox" {
#   name       = var.container_name
#   image      = var.docker_image
#   tty        = true
#   stdin_open = true

#   ports {
#     internal = var.internal_ports
#     external = var.external_ports
#   }
# }