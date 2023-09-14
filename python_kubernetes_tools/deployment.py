import kubernetes as k8s
import re
from time import sleep

def recreate_pods(api_client: k8s.client.ApiClient, namespace: str, name_pattern: str, verbose: bool = False)->dict[str, list[str]]:
  deployment_ns = namespace
  deployment_name_pattern = name_pattern

  appsv1_client = k8s.client.AppsV1Api(api_client)
  deployments = appsv1_client.list_namespaced_deployment(namespace=deployment_ns)
  
  deleted_pods = {}

  for deploy in deployments.items:
    if re.search(deployment_name_pattern, deploy.metadata.name):
      deleted_pods[deploy.metadata.name] = []
      
      label_selector_value = ",".join([ f"{k}={deploy.spec.selector.match_labels[k]}" for k in deploy.spec.selector.match_labels ])

      apiv1_client = k8s.client.CoreV1Api(api_client)
      pods = apiv1_client.list_namespaced_pod(namespace=deployment_ns, label_selector=label_selector_value)

      pod_names = [ pod.metadata.name for pod in pods.items ]
      
      if verbose: print(f"Deleting pods belonging to '{deploy.metadata.name}' deployment")
      for pod in pod_names:
        if verbose: print(f"  Deleting pod '{pod}'")
        deleted_pods[deploy.metadata.name].append(pod)
        apiv1_client.delete_namespaced_pod(namespace=deployment_ns, name=pod, grace_period_seconds=0)

        sleep(2)
        deployment_status = appsv1_client.read_namespaced_deployment_status(namespace=deployment_ns, name=deploy.metadata.name)
        while deployment_status.status.available_replicas != deployment_status.status.replicas:
          if verbose: print(f"    Waiting for '{deploy.metadata.name}' to be ready ...")
          sleep(5)
          deployment_status = appsv1_client.read_namespaced_deployment_status(namespace=deployment_ns, name=deploy.metadata.name)

  return deleted_pods
