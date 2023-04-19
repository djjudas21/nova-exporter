import json

with open('nova-output.json', 'r') as file:
    python_obj = json.load(file)

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

for obj in python_obj:
	uptodate = 1 if obj['outdated'] is False else 0
	print(f"""nova_release{{release="{obj['release']}",chartName="{obj['chartName']}",namespace="{obj['namespace']}",installed="{obj['Installed']['version']}",latest="{obj['Latest']['version']}"}} {uptodate}""")
