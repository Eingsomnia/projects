#!/bin/bash

terraform fmt
terraform validate
terraform plan -var-file terraform.tfvars -out plan