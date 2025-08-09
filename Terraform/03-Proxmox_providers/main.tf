# Clickhouse Resources
resource "proxmox_vm_qemu" "clickhouse" {
    target_node = var.target_node
    desc = "Cloudinit Ubuntu"
    count = 2
    onboot = true

    clone = var.template_name

    agent = 0
    
    vmid = 500 + count.index

    os_type = "cloud-init"
    cores = 2
    sockets = 1
    numa = true
    vcpus = 0
    cpu = "host"
    memory = 2048
    name = "clickhouse-0${count.index + 1}"

    cloudinit_cdrom_storage = "local-lvm"
    scsihw   = "virtio-scsi-single" 
    bootdisk = "scsi0"

    disks {
        scsi {
            scsi0 {
                disk {
                  storage = var.storage
                  size = 50
                }
            }
        }
    }

    ipconfig0 = "ip=192.168.28.200${count.index + 1}/24,gw=192.168.28.1"
    ciuser = "systemadmin"
    nameserver = "clickhouse"
    sshkeys = var.ssh_key
}

# Zookeeper Resources

resource "proxmox_vm_qemu" "zookeeper" {
    target_node = var.target_node
    desc = "Cloudinit Ubuntu"
    count = 3
    onboot = true

    clone = var.template_name

    agent = 0

    vmid = 502 + count.index

    os_type = "cloud-init"
    cores = 2
    sockets = 1
    numa = true
    vcpus = 0
    cpu = "host"
    memory = 4096
    name = "zookeeper-0${count.index + 1}"

    cloudinit_cdrom_storage = "local-lvm"
    scsihw   = "virtio-scsi-single" 
    bootdisk = "scsi0"

    disks {
        scsi {
            scsi0 {
                disk {
                  storage = var.storage
                  size = 50
                }
            }
        }
    }

    ipconfig0 = "ip=192.168.28.202${count.index + 1}/24,gw=192.168.28.1"
    ciuser = "systemadmin"
    sshkeys = var.ssh_key
}