import kubernetes as k8s
from os import path
import asyncio

k8s.config.load_kube_config(path.join(path.expanduser('~'), '.kube', 'config'))
k8s_client = k8s.client.ApiClient(
  configuration=k8s.client.Configuration.get_default_copy()
)

apiv1_client = k8s.client.CoreV1Api(k8s_client)
namespaces = apiv1_client.list_namespace()
for ns in namespaces.items:
  print(ns.metadata.name)
  pods = apiv1_client.list_namespaced_pod(namespace=ns.metadata.name)
  pod_delete_futures = []
  #for pod in pods.items:
  #  pod_delete_futures.append(
  #    apiv1_client.delete_namespaced_pod(
  #      name=pod.metadata.name,
  #      namespace=ns.metadata.name,
  #      async_req=True
  #    )
  #  )
