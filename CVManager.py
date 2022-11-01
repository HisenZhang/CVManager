import os
import sys
import datetime
from yamldb import YamlDB
from deployer import DeployerFactory
from renderer import RendererFactory

if len(sys.argv) != 2:
    print('Usage: CVManager.py PATH_TO_PROFILE')
    sys.exit()

now = datetime.datetime.now(datetime.timezone.utc).isoformat()

profile = YamlDB(filename=sys.argv[1])
db = YamlDB(filename=os.path.join(
            profile['input.path'], profile['input.data']))

html_cache = str()

# pprint.pprint(db.experience)

output_types = profile['output.type']
renderers = RendererFactory(profile).createRenderers(output_types)
type_path = dict()
for type,renderer in renderers.items():
    type_path[type] = renderer.render(db,profile,now)


deployment = profile['deploy']
deployers = DeployerFactory(profile).createDeployers(deployment)
for dest,deployer in deployers.items():
    deployer.trashOldFiles(profile['output.filename'])
    deployer.deploy(profile,type_path)
