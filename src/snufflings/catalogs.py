from pyrocko.snuffling import Snuffling, Param, Choice
from pyrocko.gui_util import EventMarker

from pyrocko import catalog


class CatalogSearch(Snuffling):
    '''
    <html>
    <head>
    <style type="text/css">
    body { margin-left:10px };
    </style>
    </head>
    <body>
        <h1 align="center">Catalog Search</h1>
    <p>
        Retrieve event data from online catalogs.
    </p>
        <b>Parameters:</b><br />
        <b>&middot; Catalog</b>  -  Online database to search for events.<br />
        <b>&middot; Min Magnitude</b>  -
        Only consider events with magnitude greater than chosen..<br />
    </p>
    <p>
        Data from the folowing catalogs can be retrieved:<br />
        &middot;
        <a href="http://geofon.gfz-potsdam.de/eqinfo/list.php">GEOFON</a><br />
        &middot;
        <a href="http://www.globalcmt.org/">Global CMT</a><br />
        &middot;
        <a href="http://earthquake.usgs.gov/regional/neic/">USGS</a><br />
        &middot;
        <a href="http://kinherd.org/quakes/KPS/">Kinherd</a><br />
    </p>
    <p>
        The USGS catalog allows to destinguish between 'Preliminary
        Determination of Epicenters' (PDE) and 'Quick Epicenters Determination'
        (PDE-Q). Latter one includes events of approximately the last six
        weeks. For detailed information about both catalog versions have a look
        at <a href="http://earthquake.usgs.gov/research/data/pde.php">'The
        Preliminary Determination of Epicenters (PDE) Bulletin'</a>.
    </p>
    </body>
    </html>
    '''

    def setup(self):

        self.catalogs = {
            'Geofon': catalog.Geofon(),
            'USGS/NEIC PDE': catalog.USGS('pde'),
            'USGS/NEIC US': catalog.USGS('us'),
            'Global-CMT': catalog.GlobalCMT(),
            'Kinherd': catalog.Kinherd(), }

        catkeys = sorted(self.catalogs.keys())
        self.set_name('Catalog Search')
        self.add_parameter(Choice('Catalog', 'catalog', catkeys[0], catkeys))
        self.add_parameter(Param('Min Magnitude', 'magmin', 0, 0, 10))
        self.set_live_update(False)

    def call(self):

        viewer = self.get_viewer()
        tmin, tmax = viewer.get_time_range()

        cat = self.catalogs[self.catalog]
        event_names = cat.get_event_names(
            time_range=(tmin, tmax),
            magmin=self.magmin)

        for event_name in event_names:
            event = cat.get_event(event_name)
            marker = EventMarker(event)
            self.add_markers([marker])


def __snufflings__():

    return [CatalogSearch()]
