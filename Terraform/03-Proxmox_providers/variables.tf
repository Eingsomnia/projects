variable "pm_api_url" {}
variable "pm_api_token_id" {}
variable "pm_api_token_secret" {}

variable "template_name" {}
variable "target_node" {}

variable "storage_pool" {
  type    = string
  default = "local-lvm"
}

variable "network_bridge" {
  type    = string
  default = "vmbr0"
}
variable "disk_size" {
  type    = string
  default = "32G"
}

variable "gateway" {}

variable "ci_user" {}
variable "ci_password" {}
variable "ssh_pub_key" {
  type    = string
  default = "~/.ssh/id_rsa.pub"
}

variable "vms" {
  description = "VMs to create"
  type = map(object({
    ip      = string
    cores   = number
    sockets = number
    memory  = number
  }))
}