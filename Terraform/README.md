# 🌐 Terraform + AWS Demo Infrastructure as a Code

> A lightweight infrastructure setup using Terraform to provision AWS resources – fully version-controlled, reproducible, and designed for practice & learning DevOps automation.

---

## 🚀 What’s Inside?

🧱 **Terraform IaC**  
Provision AWS infrastructure including:
- EC2 instance (with proper key pair)
- Security Groups

🔐 **Secrets-Safe**  
Provider credentials and secrets are kept clean using `.gitignore` and environment variables.

🧪 **Practice Focused**  
This repo is built as a personal lab for learning:
- Terraform basics
- Remote state management
- AWS provider and Docker Local config
- `.tfvars` and variable usage
- `.gitignore` best practices

---

## 🧠 Why I Built This

I’m learning Terraform and Infrastructure as Code (IaC), and this project helps me:

- Practice writing clean `.tf` files
- Get better at versioning infrastructure in Git
- Simulate real-world workflows

---

## 🛠 Usage

### 1. Clone the repo:

```bash
git https://github.com/Eingsomnia/projects.git
cd projects/Terraform/02-AWS_Web_instance