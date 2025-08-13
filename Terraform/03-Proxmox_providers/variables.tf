variable "pm_api_url" {
  type = string
}

variable "pm_api_token_id" {
  type = string
}

variable "pm_api_token_secret" {
  type = string
}

variable "pm_tls_insecure" {
  type = string
}

variable "template_name" {
  type = string
}

variable "proxmox_host" {
  description = "The IP address or FQDN of your Proxmox host."
  default     = "10.52.18.6"
}

# variable "target_node" {
#   description = "Target node"
# }

variable "ciuser" {
  type = string
}

variable "cipassword" {
  type = string
}

variable "ssh_key" {
  description = "The public SSH key to install on new VMs."
}

variable "virtual_machines" {
  description = "A map of virtual machines for the Wazuh cluster."
  type        = map(any)
  default = {
    "clickhouse-01" = {
      vmid      = 201
      ip        = "192.168.28.201"
      cpu_cores = 2
      memory    = 4096
      hdd_size  = 32

    },
    "clickhouse-02" = {
      vmid      = 202
      ip        = "192.168.28.202"
      cpu_cores = 2
      memory    = 4096
      hdd_size  = 32
    },

    "zookeeper-01" = {
      vmid      = 203
      ip        = "192.168.28.210"
      cpu_cores = 2
      memory    = 4096
      hdd_size  = 32
    },

    "zookeeper-02" = {
      vmid      = 204
      ip        = "192.168.28.211"
      cpu_cores = 2
      memory    = 4096
      hdd_size  = 32
    },
    "zookeeper-03" = {
      vmid      = 205
      ip        = "192.168.28.212"
      cpu_cores = 2
      memory    = 4096
      hdd_size  = 32
    }
  }
}