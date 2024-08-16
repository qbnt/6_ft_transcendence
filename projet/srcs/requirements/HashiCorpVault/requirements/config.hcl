ui = true
disable_mlock = "true"

storage "raft" {
  path    = "/data"
  node_id = "node1"
}

listener "tcp" {
  address = "[::]:8200"
  tls_disable = "false"
  tls_cert_file = "/requirements/certificate.pem"
  tls_key_file  = "/requirements/key.pem"
}

api_addr = "https://localhost:8200"
cluster_addr = "https://localhost:8201"