resource "proxmox_vm_qemu" "vm" {
  for_each    = var.vms
  name        = each.key
  target_node = var.target_node
  clone       = var.template_name
  full_clone  = true
  os_type     = "cloud-init"

  cpu {
    cores   = each.value.cores
    sockets = each.value.sockets
  }

  memory = each.value.memory

  ipconfig0  = "ip=${each.value.ip},gw=${var.gateway}"
  ciuser     = var.ci_user
  cipassword = var.ci_password
  sshkeys    = file(var.ssh_pub_key)

  network {
    id     = 0
    model  = "virtio"
    bridge = var.network_bridge
  }

  disks {
    scsi {
      scsi0 {
        disk {
          storage = var.storage_pool
          size    = var.disk_size
        }
      }
    }

    ide {
      ide2 {
        cloudinit {
          storage = var.storage_pool
        }
      }
    }
  }
}