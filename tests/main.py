import kubernetes as k8s
from os import path

import python_kubernetes_tools.deployment as deployment

#k8s.config.load_kube_config(path.join(path.expanduser('~'), '.kube', 'config'))
k8s.config.load_kube_config(path.join(path.expanduser('~'), 'github', 'iac-projects', 'pulumi', 'aws', 'eks-cluster', 'kubeconfig.yaml'))
k8s_client = k8s.client.ApiClient(
  configuration=k8s.client.Configuration.get_default_copy()
)

deleted_pods = deployment.recreate_pods(k8s_client, 'cloud-controllers', '^karpenter-.*$')
print(deleted_pods)
