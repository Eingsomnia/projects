---
- name: Ensure swap is off permanently
  ansible.builtin.command: swapoff -a
  when: ansible_swaptotal_mb > 0
  become: true

- name: Comment out swap in /etc/fstab
  ansible.builtin.replace:
    path: /etc/fstab
    regexp: '^([^#].*\\s+swap\\s+)'
    replace: '#\\1'
  become: true

- name: Enable IP forwarding
  ansible.builtin.sysctl:
    name: net.ipv4.ip_forward
    value: '1'
    state: present
    sysctl_set: yes
    reload: yes
  become: true

- name: Allow iptables to see bridged traffic
  ansible.builtin.copy:
    dest: /etc/modules-load.d/k8s.conf
    content: |
      br_netfilter
  become: true

- name: Ensure br_netfilter is loaded
  ansible.builtin.modprobe:
    name: br_netfilter
  become: true

- name: Set required sysctl params
  ansible.builtin.copy:
    dest: /etc/sysctl.d/k8s.conf
    content: |
      net.bridge.bridge-nf-call-ip6tables = 1
      net.bridge.bridge-nf-call-iptables = 1
  become: true

- name: Apply sysctl params
  ansible.builtin.command: sysctl --system
  become: true

- name: Install dependencies
  ansible.builtin.apt:
    name:
      - apt-transport-https
      - ca-certificates
      - curl
      - gnupg
      - lsb-release
    state: present
    update_cache: yes
  become: true

- name: Install containerd package
  ansible.builtin.apt:
    name: containerd
    state: present
    update_cache: true
  become: true

- name: Generate default containerd config.toml if missing
  ansible.builtin.shell: containerd config default > /etc/containerd/config.toml
  args:
    creates: /etc/containerd/config.toml
  become: true

- name: Set SystemdCgroup = true in containerd config
  ansible.builtin.replace:
    path: /etc/containerd/config.toml
    regexp: '^\s*SystemdCgroup = false'
    replace: 'SystemdCgroup = true'
  become: true

- name: Restart containerd
  ansible.builtin.systemd:
    name: containerd
    state: restarted
    enabled: true
  become: true

---
- name: Install HAProxy
  ansible.builtin.apt:
    name: haproxy
    state: present
    update_cache: yes
  become: true

- name: Configure HAProxy for Kubernetes API Load Balancing
  ansible.builtin.template:
    src: haproxy.cfg.j2
    dest: /etc/haproxy/haproxy.cfg
    owner: root
    group: root
    mode: '0644'
  notify: Restart HAProxy
  become: true

- name: Ensure HAProxy is enabled and started
  ansible.builtin.service:
    name: haproxy
    state: started
    enabled: true
  become: true

- name: Check if kubeconfig file exists
  ansible.builtin.stat:
    path: /etc/kubernetes/admin.conf
  register: admin_conf_result
  become: true

- name: Ensure .kube directory exists for systemadmin
  ansible.builtin.file:
    path: /home/systemadmin
    state: directory
    owner: systemadmin
    group: systemadmin
    mode: '0755'
  become: true

- name: Wait for .kube directory to be ready
  ansible.builtin.wait_for:
    path: /home/systemadmin/.kube
    state: present
    timeout: 5
  become: true

- name: Debug .kube dir exists or not
  ansible.builtin.stat:
    path: /home/systemadmin/.kube
  register: kube_dir_stat
  become: true

- name: 🪪 Copy kubeconfig for systemadmin if available
  ansible.builtin.copy:
    src: /etc/kubernetes/admin.conf
    dest: /home/systemadmin/.kube/config
    remote_src: true
    owner: systemadmin
    group: systemadmin
    mode: '0600'
  become: true
  when: admin_conf_result.stat.exists

- name: 🕸️ Wait for Kubernetes API to become available
  ansible.builtin.command: kubectl get nodes
  environment:
    KUBECONFIG: /home/systemadmin/.kube/config
  register: kubectl_ready
  retries: 20
  delay: 10
  until: kubectl_ready.rc == 0
  changed_when: false