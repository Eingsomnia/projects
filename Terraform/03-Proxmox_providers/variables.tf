variable "pm_api_url"          { type = string }
variable "pm_api_token_id"     { type = string }
variable "pm_api_token_secret" { type = string }
variable "pm_tls_insecure"     { type = bool }

variable "target_node"   { type = string }
variable "template_name" { type = string }
variable "storage"       { type = string }

variable "ssh_key" { type = string }