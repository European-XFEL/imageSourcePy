# Import this file at the beginning of a sphinx conf.py to set some default
# settings

import sys
import os
import os.path

sys.path.append(os.path.abspath('/usr/src/app/breath-4.2.0'))

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'default'


# mock karathon and other modules commmonly used so that we don't have to
# compile it
class Mock(object):
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return Mock()

    @classmethod
    def __getattr__(cls, name):
        if name in ('__file__', '__path__'):
            return '/dev/null'
        elif name[0] == name[0].upper():
            mockType = type(name, (), {})
            mockType.__module__ = __name__
            return mockType
        else:
            return Mock()


MOCK_MODULES = ['karathon', 'IPython', 'eulexistdb', 'eulexistdb.exceptions',
                'traits', 'enthought', 'karabo', 'karabo.bound',
                'karabo.common', 'karabo.middlelayer', 'karabo.native',
                'karabo.middlelayer_api', 'karabo.bound_api',
                'karabo.project_db', 'karabo.gui', 'karabo.common.api',
                'karabo.common.scenemodel', 'karabo.common.scenemodel.api']
sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)


# mocking of decorators does not work
def KARABO_CLASSINFO(classid, version):
    def inner(func):
        return func
    return inner


# dot
graphviz_dot_args = ['-Kdot']
# circo dot fdp neato nop nop1 nop2 osage patchwork sfdp twopi


# add support for detailed developer configuration:
def setup(app):
    app.add_config_value('includeDevInfo', False, 'env')


# we add a custom function to work with intersphinx
import slumber


# the RTDHOST should be set to localhost if you only compile on RTD
# otherwise it needs to be set to the server hosting the internal RTD
RTDHOST = 'https://in.xfel.eu/readthedocs'
api = slumber.API(base_url='{}/api/v1/'.format(RTDHOST))
public_slugs = []
offset = 0
while True:
    # get the projects (by default they are limited)
    # so we increment the offset of the query until
    # it returns empty handed
    new_projs = api.project.get(offset=offset)['objects']
    if len(new_projs) == 0:
        break
    offset += len(new_projs)
    public_slugs.extend([proj['slug'] for proj in new_projs])

# the previous section will return all the *public* projects
# to add to the intersphinx mapping the protected projects we need to
# add them manually in the list below
protected_slugs = [
    'deployment-documentation',
    'sls-detectors',
    'scpi-base-class',
    'plc-framework',
    'plc-management-system'
]


def _insert(d, slug):
    d[slug.replace('-', '')] = \
     ('{}/docs/{}/en/latest'.format(RTDHOST, slug), None)


# defining some default RTD intersphinx place map elements
isphinx = {'python': ('http://python.readthedocs.io/en/latest/', None),
           'numpy': ('http://numpy.readthedocs.io/en/latest/', None)}


for slug in public_slugs + protected_slugs:
    _insert(isphinx, slug)

intersphinx_mapping = isphinx

extlinks = {'rtd': ('https://in.xfel.eu/readthedocs/docs/%s/en/latest/',
                    '')}
