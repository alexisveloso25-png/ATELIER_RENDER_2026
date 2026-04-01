terraform {
  required_providers {
    render = {
      source  = "render-oss/render"
      version = ">= 1.7.0"
    }
  }
}

provider "render" {
  api_key  = var.render_api_key
  owner_id = var.render_owner_id
}

variable "github_actor" {
  description = "GitHub username"
  type        = string
}

# 1. Service Flask (Backend)
resource "render_web_service" "flask_app" {
  name   = "flask-render-iac-${var.github_actor}"
  plan   = "free"
  region = "frankfurt"

  runtime_source = {
    image = {
      image_url = var.image_url
      tag       = var.image_tag
    }
  }

  env_vars = {
    "ENV" = {
      value = "production"
    },
    "DATABASE_URL" = {
      value = "postgresql://ma_db_flask_user:xyRR3jo1vh3sPDa17xxJ9QN2M1u3UnKK@dpg-d76h6olm5p6s73bmopn0-a/ma_db_flask"
    }
  }
}

# 2. Service Adminer (Gestion BDD) corrigé avec le nom canonique
resource "render_web_service" "adminer" {
  name   = "adminer-${var.github_actor}"
  plan   = "free"
  region = "frankfurt"

  runtime_source = {
    image = {
      image_url = "docker.io/library/adminer"
      tag       = "latest"
    }
  }
}
