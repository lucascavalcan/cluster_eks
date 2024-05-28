data "tls_certificate" "eks_oidc_tls_certificate" {
  url = aws_eks_cluster.eks_cluster.identity[0].oidc[0].issuer
}

resource "aws_iam_openid_connect_provider" "eks_oidc" {
  client_id_list = [
    "sts.amazonaws.com"
  ]
  thumbprint_list = flatten([for cert in data.tls_certificate.eks_oidc_tls_certificate.certificates : cert.sha1_fingerprint])
  url             = data.tls_certificate.eks_oidc_tls_certificate.url
}