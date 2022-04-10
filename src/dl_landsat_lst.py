import ee
ee.Authenticate()
ee.Initialize()


class EarthEngineExport:

    def __init__(self, start_date, end_date, geometry):
        self.startdate = start_date
        self.enddate = end_date
        self.geometry = geometry
        self.reducers = ee.Reducer.median().combine(**{
            "reducer2": ee.Reducer.min(),
            "sharedInputs": True
        }).combine(**{
            "reducer2": ee.Reducer.max(),
            "sharedInputs": True
        })

    def maskL8sr(self, image):
        # Bits 3 and 4 are cloud shadow and cloud, respectively.
        cloudShadowBitMask = (1 << 3)
        cloudsBitMask = (1 << 4)
        qa = image.select('QA_PIXEL')
        mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0).And(
            qa.bitwiseAnd(cloudsBitMask).eq(0))

        return image.updateMask(mask)

    # Applies scaling factors.
    def applyScaleFactors(self, image):
        opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2)
        thermalBands = image.select('ST_B.*').multiply(0.00341802).add(149.0)
        return image.addBands(opticalBands, None, True).addBands(thermalBands, None, True)

    def filter_data(self):

        dataset = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')\
                    .filterDate(self.startdate, self.enddate)\
                    .filter(ee.Filter.lt('CLOUD_COVER', 50))\
                    .map(self.applyScaleFactors)\
                    .map(self.maskL8sr)\
                    .filterBounds(self.geometry)

        return dataset

    def timeSeries(self, image):

            stats = image.reduceRegion(**{
            "reducer": self.reducers,
            "geometry": self.geometry.geometry(),
            "scale": 30,
            "maxPixels": 1e13
            })
            
            ST_B10_median = ee.List([stats.get('ST_B10_median'), -9999])\
                              .reduce(ee.Reducer.firstNonNull())
            ST_B10_max = ee.List([stats.get('ST_B10_max'), -9999])\
                           .reduce(ee.Reducer.firstNonNull())
            ST_B10_min = ee.List([stats.get('ST_B10_min'), -9999])\
                           .reduce(ee.Reducer.firstNonNull())
            f = ee.Feature(None, {'ST_B10_max': ST_B10_max,\
                                  'ST_B10_median': ST_B10_median, \
                                  'ST_B10_min': ST_B10_min,\
                                  'date': ee.Date(image.get('system:time_start'))\
                                  .format('YYYY-MM-dd')})
            return f


    def run_main(self):
        dataset = self.filter_data()
        return ee.FeatureCollection(dataset.map(self.timeSeries))
    
    def export_collection(self, featureCol):      
        # Export the FeatureCollection to a KML file.
        task = ee.batch.Export.table.toDrive(**{
          'collection': featureCol,
            "description": f'LST_{self.startdate}',
            "folder": 'earthengine_bluesky',
            "fileNamePrefix": f'blr_lst_{self.startdate}',
            "fileFormat": 'CSV'
        })
        task.start()
        print(task.status(), end = '\n')
        return task

if __name__=='__main__':

    # Bengaluru geom as ee asset
    geometry = ee.FeatureCollection("projects/ee-amanbagrecha/assets/BLR_BBMP_SHP")
    task_status = dict()
    years = ['2019' ,'2020', '2021']

    for yr in years:
        
        ee_export = EarthEngineExport(f'{yr}-01-01', f'{yr}-06-30', geometry )
        feature_collection = ee_export.run_main()
        task_status[yr] = ee_export.export_collection(feature_collection)
