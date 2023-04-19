# Example record from Nova
#  {
#    "release": "hammond",
#    "chartName": "hammond",
#    "namespace": "hammond",
#    "description": "Self-hosted vehicle expense tracking system with support for multiple users",
#    "home": "https://github.com/alfhou/hammond",
#    "icon": "https://github.com/alfhou/hammond/raw/master/ui/src/assets/images/logo.png",
#    "Installed": {
#      "version": "0.3.1",
#      "appVersion": "v0.0.2"
#    },
#    "Latest": {
#      "version": "0.3.1",
#      "appVersion": "v0.0.2"
#    },
#    "outdated": false,
#    "deprecated": false,
#    "helmVersion": "3",
#    "overridden": false
#  },

from prometheus_client import start_http_server, Gauge, REGISTRY, GC_COLLECTOR, PLATFORM_COLLECTOR, PROCESS_COLLECTOR
import time
import json

REGISTRY.unregister(GC_COLLECTOR)
REGISTRY.unregister(PLATFORM_COLLECTOR)
REGISTRY.unregister(PROCESS_COLLECTOR)

RELEASES_INFO = Gauge('nova_release', 'Nova releases', [
                        'release', 'chartName', 'namespace', 'installed', 'latest'])

def collect_metrics():
    while True:
        # run nova
        nova_output = run_nova()

        # parse results
        for obj in nova_output:
            uptodate = 1 if obj['outdated'] is False else 0

            RELEASES_INFO.labels(
                obj['release'],
				obj['chartName'],
                obj['namespace'],
                obj['Installed']['version'],
                obj['Latest']['version']
			).set(int(uptodate))

        time.sleep(60)

def run_nova():
    # This function should execute Nova to get output.
    # For now, we just test with saved output in a text file
    with open('nova-output.json', 'r') as file:
        python_obj = json.load(file)
    return python_obj


if __name__ == '__main__': 
    start_http_server(8000)
    collect_metrics()
