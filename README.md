# Nova Exporter

A Prometheus exporter which uses [Fairwinds Nova](https://github.com/FairwindsOps/nova) to report on the freshness of Helm deployments on Kubernetes
clusters.

This exporter scrapes data from Nova approximately once per hour, because it is a relatively slow and expensive operation (it accesses the
ArtifactHub API as well as your Kubernetes cluster).

It accesses whichever Kubernetes cluster is currently set in your context. If you run the script locally, it will operate on whatever cluster
is referenced in the output of `kubectl cluster-info`. When run in Kubernetes, it should automatically operate on the cluster it is running in.

It listens on port 8000. There are currently no configurable options for this exporter.

## Installing

There is a [Helm chart](https://github.com/djjudas21/charts/tree/main/charts/nova-exporter) available, which installs nova-exporter
and optionally enables a ServiceMonitor and a PrometheusRule for the Prometheus Operator.

```
helm repo add djjudas21 https://djjudas21.github.io/charts/
helm repo update djjudas21
helm install -n monitoring nova-exporter djjudas21/nova-exporter --set 'serviceMonitor.enabled=true' --set 'prometheusRules.enabled=true'
```

## Example output from Nova

When Nova is run in json output mode, each record looks like this. There is one record per Helm deployment.

```json
  {
    "release": "hammond",
    "chartName": "hammond",
    "namespace": "hammond",
    "description": "Self-hosted vehicle expense tracking system with support for multiple users",
    "home": "https://github.com/alfhou/hammond",
    "icon": "https://github.com/alfhou/hammond/raw/master/ui/src/assets/images/logo.png",
    "Installed": {
      "version": "0.3.1",
      "appVersion": "v0.0.2"
    },
    "Latest": {
      "version": "0.3.1",
      "appVersion": "v0.0.2"
    },
    "outdated": false,
    "deprecated": false,
    "helmVersion": "3",
    "overridden": false
  },
```

## Example output from the exporter

This exporter creates output in the following format. Each line represents one Helm deployment.
A value of `1.0` indicates that the deployment is up to date; a value of `0.0` indicates that there is a newer
version of the Helm chart available, and the deployment is outdated.

```
# HELP nova_release Nova releases
# TYPE nova_release gauge
nova_release{chartName="hammond",installed="0.3.1",latest="0.3.1",namespace="hammond",release="hammond"} 1.0
nova_release{chartName="smtp-relay",installed="0.4.0",latest="0.4.0",namespace="smtp",release="smtp"} 1.0
nova_release{chartName="democratic-csi",installed="0.13.5",latest="0.13.7",namespace="democratic-csi",release="truenas"} 0.0
nova_release{chartName="bookstack",installed="5.2.7",latest="5.2.8",namespace="bookstack",release="bookstack"} 0.0
nova_release{chartName="rook-ceph",installed="v1.11.2",latest="1.11.5",namespace="rook-ceph",release="rook-ceph"} 0.0
nova_release{chartName="rook-ceph-cluster",installed="v1.11.3",latest="1.5.1",namespace="rook-ceph",release="rook-ceph-cluster"} 1.0
nova_release{chartName="oauth2-proxy",installed="6.10.1",latest="6.12.0",namespace="oauth2-proxy",release="oauth2-proxy"} 0.0
nova_release{chartName="node-problem-detector",installed="2.3.4",latest="2.3.4",namespace="kube-system",release="node-problem-detector"} 1.0
nova_release{chartName="argo-cd",installed="5.32.0",latest="5.33.4",namespace="argocd",release="argocd"} 0.0
nova_release{chartName="kube-prometheus-stack",installed="45.27.1",latest="45.28.0",namespace="monitoring",release="prometheus-stack"} 0.0
nova_release{chartName="camerahub",installed="0.10.31",latest="0.10.21",namespace="camerahub-dev",release="camerahub-dev"} 1.0
nova_release{chartName="camerahub",installed="0.10.31",latest="0.10.21",namespace="camerahub-prod",release="camerahub"} 1.0
nova_release{chartName="gemini",installed="2.1.0",latest="2.1.0",namespace="gemini",release="gemini"} 1.0
nova_release{chartName="homer",installed="8.1.7",latest="8.1.7",namespace="homer",release="homer"} 1.0
```
