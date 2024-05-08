module "dev" {
  source        = "${path.module}/dev"
  stage         = "dev"
  key_pair_name = "dev-application-server"
}

module "prod" {
  source        = "${path.module}/prod"
  stage         = "prod"
  key_pair_name = "prod-application-server"
}
