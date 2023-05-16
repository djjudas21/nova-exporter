"""
NOVA EXPORTER
Prometheus exporter for Fairwinds Nova
"""

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

import time
from json import loads, JSONDecodeError
import subprocess
from prometheus_client import start_http_server, Gauge, REGISTRY, GC_COLLECTOR, PLATFORM_COLLECTOR, PROCESS_COLLECTOR

REGISTRY.unregister(GC_COLLECTOR)
REGISTRY.unregister(PLATFORM_COLLECTOR)
REGISTRY.unregister(PROCESS_COLLECTOR)

RELEASES_INFO = Gauge('nova_release', 'Nova releases', [
                        'release', 'chartName', 'namespace', 'installed', 'latest'])

def collect_metrics():
    """
    Periodically collect the json output from Nova and mangle it
    into a Prometheus metrics format, ready to be served via http
    """
    while True:
        # run nova
        nova_output = run_nova()

        try:
            nova_output_json = loads(nova_output)
        except JSONDecodeError:
            nova_output_json = []

        # parse results
        for obj in nova_output_json:
            uptodate = 1 if obj['outdated'] is False else 0

            RELEASES_INFO.labels(
                obj['release'],
				obj['chartName'],
                obj['namespace'],
                obj['Installed']['version'],
                obj['Latest']['version']
			).set(int(uptodate))

        # Sleep for 1 hour between checking Nova again
        time.sleep(3600)

def run_nova():
    """
    Execute the Nova binary and capture the json output
    """

    try:
        result = subprocess.run(['nova', 'find'], capture_output=True, text=True, check=False).stdout
    except:
        print('Failed to run Nova')
    return result.strip()

if __name__ == '__main__':
    start_http_server(8000)
    collect_metrics()
