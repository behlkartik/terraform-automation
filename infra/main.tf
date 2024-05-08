module "dev" {
  source        = "./dev"
  stage         = "dev"
  key_pair_name = "dev-application-server"
}

module "prod" {
  source        = "./prod"
  stage         = "prod"
  key_pair_name = "prod-application-server"
}
