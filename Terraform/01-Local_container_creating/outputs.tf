output "container_name" {
  description = "Container name output"
  value       = docker_container.busybox.name
}

output "container_url" {
  description = "Container url output"
  value       = "http://localhost:${var.external_ports}"
}