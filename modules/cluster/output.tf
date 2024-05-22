output "eks_vpc_config" {
    value = aws_eks_cluster.eks_cluster.vpc_config
}

output "oidc" {
  value = flatten([for cert in data.tls_certificate.eks_oidc_tls_certificate.certificates : cert.sha1_fingerprint])
}

output "cluster_name" {
  value = aws_eks_cluster.eks_cluster.id
}