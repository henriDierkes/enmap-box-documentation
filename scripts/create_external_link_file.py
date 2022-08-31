import pathlib
import re

import qgis.PyQt.QtCore
import qgis.PyQt.QtGui
import qgis.PyQt.QtWidgets
import qgis.core

DIR_REPO = pathlib.Path(__file__).parents[2]
DIR_SOURCE = DIR_REPO / 'doc' / 'source'
assert DIR_SOURCE.is_dir()

PATH_LINK_RST = DIR_SOURCE / 'dev_section/external_links.rst'

objects = []
for module in [
    qgis
    , qgis.core
    , qgis.gui
    , qgis.PyQt.QtCore
    , qgis.PyQt.QtWidgets
    , qgis.PyQt.QtGui
    , qgis.PyQt.QtWidgets
               ]:
    s = ""
    for key in module.__dict__.keys():
        if re.search('^(Qgs|Q)', key):
            objects.append(key)
objects = sorted(objects)

lines = """
.. autogenerated file. 

.. _PyCharm: https://www.jetbrains.com/pycharm/
.. _PyQtGraph: http://www.pyqtgraph.org/documentation/
.. _PyDev: https://www.pydev.org
.. _OSGeo4W: https://www.osgeo.org/projects/osgeo4w
.. _Bitbucket: https://bitbucket.org
.. _Git: https://git-scm.com/
.. _GitHub: https://github.com/
.. _GDAL: https://www.gdal.org
.. _QtWidgets: https://doc.qt.io/qt-5/qtwidgets-index.html
.. _QtCore: https://doc.qt.io/qt-5/qtcore-index.html
.. _QtGui: https://doc.qt.io/qt-5/qtgui-index.html
.. _QGIS: https://www.qgis.org
.. _qgis.gui: https://qgis.org/api/group__gui.html
.. _qgis.core: https://qgis.org/api/group__core.html
.. _Miniconda: https://docs.conda.io/en/latest/miniconda.html
.. _miniconda: https://docs.conda.io/en/latest/miniconda.html
.. _Numba: http://numba.pydata.org/
.. _Conda: https://docs.conda.io/en/latest/miniconda.html
.. _conda: https://docs.conda.io/en/latest/miniconda.html
.. _conda-forge: https://conda-forge.org/
.. _pip: https://pip.pypa.io/en/stable

.. # autogenerated singular forms 
"""

WRITTEN = []

rx_qgis = re.compile('^Qgs|Qgis.*')

for obj in objects:
    obj: str
    if obj in ['QtCore', 'QtGui', 'QtWidget']:
        continue
    print(obj)

    target = None
    if rx_qgis.match(obj):
        # https://qgis.org/api/classQgsProject.html
        target = "https://qgis.org/api/class{}.html".format(obj)
    elif obj.startswith('Q'):
        # https://doc.qt.io/qt-5/qwidget.html
        target = "https://doc.qt.io/qt-5/{}.html".format(obj.lower())
    else:
        continue

    singular = obj
    plural = obj + 's'

    line = None
    if singular.upper() not in WRITTEN:
        line = '.. _{}: {}'.format(singular, target)
        WRITTEN.append(singular.upper())

        if plural.upper() not in WRITTEN:
            line += '\n.. _{}: {}'.format(plural, target)
            WRITTEN.append(plural.upper())

    if line:
        lines += '\n' + line

with open(PATH_LINK_RST, 'w', encoding='utf-8') as f:
    f.write(lines)
