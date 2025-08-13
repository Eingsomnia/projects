resource "proxmox_vm_qemu" "vm" {
  for_each = var.virtual_machines

  name        = each.key
  target_node = "dsm"
  onboot      = true

  clone = var.template_name
  vmid  = each.value.vmid
  cpu {
    cores = each.value.cpu_cores
    type  = "qemu64"
  }
  memory = each.value.memory
  scsihw = "virtio-scsi-single"

  disk {
    slot    = "scsi0"
    size    = "${each.value.hdd_size}G"
    type    = "disk"
    storage = "local-lvm"
  }
  disk {
    slot    = "ide0"
    type    = "cloudinit"
    storage = "local-lvm"
  }

  network {
    id     = 0
    model  = "virtio"
    bridge = "vmbr0"
  }

  os_type    = "cloud-init"
  ciuser     = var.ciuser
  cipassword = var.cipassword
  ipconfig0  = "ip=${each.value.ip}/24,gw=192.168.28.1"
  sshkeys    = var.ssh_key

  agent = 1
  boot  = "order=scsi0;ide0"

  serial {
    id   = 0
    type = "socket"
  }

  vga {
    type = "serial0"
  }
}