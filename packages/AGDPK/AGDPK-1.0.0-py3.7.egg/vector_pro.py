# -*- coding: utf-8 -*-
import os
import glob
from tqdm import tqdm
import time
from osgeo import osr
from osgeo import ogr


class ShpPolygon:
    @staticmethod
    def to_gtif():
        exit(0)

    @staticmethod
    def merge_shp(shp_path, save_path):
        if not os.path.isdir(shp_path):
            print('input path error.')
            exit(0)
        shps = glob.glob(shp_path + r'\*.shp')

        print('Merge ShapeFiles:')
        print(shp_path)

        driver = ogr.GetDriverByName("ESRI Shapefile")
        out_ds = driver.CreateDataSource(save_path)

        fst_ds = ogr.Open(shps[0])
        # print(str(fst_ds.GetLayer().GetSpatialRef()))
        # exit(0)
        srs = osr.SpatialReference(wkt=str(fst_ds.GetLayer().GetSpatialRef()))
        # srs.ImportFromEPSG(epsg_code)
        dst_layername = "MERGED_STUFF"
        out_layer = out_ds.CreateLayer(dst_layername, srs=srs)

        new_fields = ["Name"]
        new_field = ogr.FieldDefn(new_fields[0], ogr.OFTString)
        out_layer.CreateField(new_field)

        pbar = tqdm(total=len(shps))
        for shp in shps:
            time.sleep(0.05)
            pbar.update(1)

            file_name = os.path.splitext(os.path.split(shp)[-1])[0]
            src_ds = ogr.Open(shp)
            src_layer = src_ds.GetLayer()
            for src_feat in src_layer:
                out_feat = ogr.Feature(out_layer.GetLayerDefn())
                out_feat.SetField("Name", file_name)
                for i in range(1, src_feat.GetFieldCount()):
                    new_field_name = src_feat.GetFieldDefnRef(i).GetName()
                    if new_field_name not in new_fields:
                        new_fields.append(new_field_name)
                        new_field_type = src_feat.GetFieldDefnRef(i).GetType()
                        new_field = ogr.FieldDefn(new_field_name, new_field_type)
                        out_layer.CreateField(new_field)
                        out_feat.SetField(new_field_name, src_feat.GetField(i))
                out_feat.SetGeometry(src_feat.GetGeometryRef().Clone())
                out_layer.CreateFeature(out_feat)
                out_layer.SyncToDisk()
        pbar.close()

    @staticmethod
    def calc_area(shp_path):
        shps = []
        if os.path.isdir(shp_path):
            shps = glob.glob(shp_path + r'\*.shp')
        elif os.path.isfile(shp_path):
            if '.shp' in shp_path:
                shps.append(shp_path)
        else:
            print('input path error.')
            exit(0)

        print('Calculate the area of features:')
        print(shp_path)

        pbar = tqdm(total=len(shps))
        for shp in shps:
            time.sleep(0.05)
            pbar.update(1)

            driver = ogr.GetDriverByName("ESRI Shapefile")
            src_ds = driver.Open(shp, 1)

            src_layer = src_ds.GetLayer()
            new_field = ogr.FieldDefn("Area", ogr.OFTReal)
            new_field.SetPrecision(2)
            src_layer.CreateField(new_field)
            for src_feat in src_layer:
                src_geom = src_feat.GetGeometryRef()
                src_feat.SetField("Area", src_geom.GetArea())
                src_layer.SetFeature(src_feat)
        pbar.close()

    @staticmethod
    def sum_numattr(filed_name, shp_path):
        if not os.path.isfile(shp_path):
            print('input path error.')
            exit(0)

        driver = ogr.GetDriverByName("ESRI Shapefile")
        src_ds = driver.Open(shp_path, 0)
        src_layer = src_ds.GetLayer()
        sum_val = 0
        for src_feat in src_layer:
            sum_val += src_feat.GetField(filed_name)

        return sum_val

    @staticmethod
    def mean_numattr(filed_name, shp_path):
        if not os.path.isfile(shp_path):
            print('input path error.')
            exit(0)

        driver = ogr.GetDriverByName("ESRI Shapefile")
        src_ds = driver.Open(shp_path, 0)
        src_layer = src_ds.GetLayer()
        sum_val = 0
        for src_feat in src_layer:
            sum_val += src_feat.GetField(filed_name)
        mean_val = sum_val / len(src_layer)

        return mean_val

    @staticmethod
    def max_numattr(filed_name, shp_path):
        if not os.path.isfile(shp_path):
            print('input path error.')
            exit(0)

        driver = ogr.GetDriverByName("ESRI Shapefile")
        src_ds = driver.Open(shp_path, 0)
        src_layer = src_ds.GetLayer()
        max_val = None

        for src_feat in src_layer:
            val = src_feat.GetField(filed_name)
            if max_val is None or val > max_val:
                max_val = val

        return max_val

    @staticmethod
    def min_numattr(filed_name, shp_path):
        if not os.path.isfile(shp_path):
            print('input path error.')
            exit(0)

        driver = ogr.GetDriverByName("ESRI Shapefile")
        src_ds = driver.Open(shp_path, 0)
        src_layer = src_ds.GetLayer()
        min_val = None

        for src_feat in src_layer:
            val = src_feat.GetField(filed_name)
            if min_val is None or val < min_val:
                min_val = val

        return min_val

    @staticmethod
    def remove_by_numattr(fl_cond, shp_path):
        shps = []
        if os.path.isdir(shp_path):
            shps = glob.glob(shp_path + r'\*.shp')
        elif os.path.isfile(shp_path):
            if '.shp' in shp_path:
                shps.append(shp_path)
        else:
            print('input path error.')
            exit(0)

        print('Remove features by number attribute:')
        print(shp_path)

        pbar = tqdm(total=len(shps))
        for shp in shps:
            time.sleep(0.05)
            pbar.update(1)

            driver = ogr.GetDriverByName("ESRI Shapefile")
            src_ds = driver.Open(shp, 1)

            src_layer = src_ds.GetLayer()
            fl_cond_str = ''
            if_first = True
            for sel_field, conds in fl_cond.items():
                if not if_first:
                    fl_cond_str += ' and '
                else:
                    if_first = False

                for cond in conds:
                    fl_cond_str += sel_field + ' ' + cond
                    if cond != conds[-1]:
                        fl_cond_str += ' and '
            src_layer.SetAttributeFilter(fl_cond_str)

            for src_feat in src_layer:
                src_layer.DeleteFeature(src_feat.GetFID())
                src_ds.ExecuteSQL('REPACK ' + src_layer.GetName())
        pbar.close()

    @staticmethod
    def remove_by_strattr(fl_cond, shp_path):
        shps = []
        if os.path.isdir(shp_path):
            shps = glob.glob(shp_path + r'\*.shp')
        elif os.path.isfile(shp_path):
            if '.shp' in shp_path:
                shps.append(shp_path)
        else:
            print('input path error.')
            exit(0)

        print('Remove features by number attribute:')
        print(shp_path)

        pbar = tqdm(total=len(shps))
        for shp in shps:
            time.sleep(0.05)
            pbar.update(1)

            driver = ogr.GetDriverByName("ESRI Shapefile")
            src_ds = driver.Open(shp, 1)

            src_layer = src_ds.GetLayer()
            fl_cond_str = ''
            if_first = True
            for sel_field, val_fixed in fl_cond.items():
                if not if_first:
                    fl_cond_str += ' and '
                else:
                    if_first = False

                for i in range(len(val_fixed)):
                    if i != 0:
                        fl_cond_str += ' and '
                    fl_cond_str += sel_field + ' = ' + "'" + str(val_fixed[0]) + "'"

            src_layer.SetAttributeFilter(fl_cond_str)

            for src_feat in src_layer:
                src_layer.DeleteFeature(src_feat.GetFID())
                src_ds.ExecuteSQL('REPACK ' + src_layer.GetName())
        pbar.close()

    @staticmethod
    def intersection(shp1_path, shp2_path, save_path):
        if shp1_path.rsplit('.', 1)[-1] != 'shp' or shp2_path.rsplit('.', 1)[-1] != 'shp':
            print('input path error.')
            exit(0)

        print('Intersect 2 shapefile:')
        print(shp1_path)
        print(shp2_path)

        driver = ogr.GetDriverByName("ESRI Shapefile")
        src1_ds = driver.Open(shp1_path, 0)
        src2_ds = driver.Open(shp2_path, 0)
        src1_layer = src1_ds.GetLayer()
        src2_layer = src2_ds.GetLayer()

        print('unite shapefile 1:')
        pbar = tqdm(total=len(src1_layer))
        src1_union = ogr.Geometry(ogr.wkbMultiPolygon)
        for src1_feat in src1_layer:
            time.sleep(0.05)
            pbar.update(1)

            geom = src1_feat.GetGeometryRef()
            src1_union = src1_union.Union(geom)
        pbar.close()

        print('unite shapefile 2:')
        pbar = tqdm(total=len(src2_layer))
        src2_union = ogr.Geometry(ogr.wkbMultiPolygon)
        for src2_feat in src2_layer:
            time.sleep(0.05)
            pbar.update(1)

            geom = src2_feat.GetGeometryRef()
            src2_union = src2_union.Union(geom)
        pbar.close()

        print('intersection is being executed ...')
        intersection = src1_union.Intersection(src2_union)

        out_ds = driver.CreateDataSource(save_path)
        srs = osr.SpatialReference(wkt=str(src1_layer.GetSpatialRef()))
        dst_layername = "INTERSECTION_STUFF"
        out_layer = out_ds.CreateLayer(dst_layername, srs=srs)
        out_feat = ogr.Feature(out_layer.GetLayerDefn())

        print('saving new data:')
        pbar = tqdm(total=intersection.GetGeometryCount())
        for geom in intersection:
            time.sleep(0.05)
            pbar.update(1)

            if geom.GetGeometryName() != 'POLYGON':
                continue
            out_feat.SetGeometry(geom)
            out_layer.CreateFeature(out_feat)
            out_layer.SyncToDisk()
        pbar.close()

    @staticmethod
    def union(shp1_path, shp2_path, save_path):
        if shp1_path.rsplit('.', 1)[-1] != 'shp' or shp2_path.rsplit('.', 1)[-1] != 'shp':
            print('input path error.')
            exit(0)

        print('Unite 2 shapefile')
        print(shp1_path)
        print(shp2_path)

        driver = ogr.GetDriverByName("ESRI Shapefile")
        src1_ds = driver.Open(shp1_path, 0)
        src2_ds = driver.Open(shp2_path, 0)
        src1_layer = src1_ds.GetLayer()
        src2_layer = src2_ds.GetLayer()

        print('unite shapefile 1:')
        pbar = tqdm(total=len(src1_layer))
        src1_union = ogr.Geometry(3)
        for src1_feat in src1_layer:
            time.sleep(0.05)
            pbar.update(1)

            geom = src1_feat.GetGeometryRef()
            src1_union = src1_union.Union(geom)
        pbar.close()

        print('unite shapefile 2:')
        pbar = tqdm(total=len(src2_layer))
        src2_union = ogr.Geometry(3)
        for src2_feat in src2_layer:
            time.sleep(0.05)
            pbar.update(1)

            geom = src2_feat.GetGeometryRef()
            src2_union = src2_union.Union(geom)
        pbar.close()

        print('Union is being executed ...')
        union = src1_union.Union(src2_union)

        out_ds = driver.CreateDataSource(save_path)
        srs = osr.SpatialReference(wkt=str(src1_layer.GetSpatialRef()))
        dst_layername = "UNION_STUFF"
        out_layer = out_ds.CreateLayer(dst_layername, srs=srs)
        out_feat = ogr.Feature(out_layer.GetLayerDefn())

        print('saving new data:')
        pbar = tqdm(total=union.GetGeometryCount())
        for geom in union:
            time.sleep(0.05)
            pbar.update(1)

            if geom.GetGeometryName() != 'POLYGON':
                continue
            out_feat.SetGeometry(geom)
            out_layer.CreateFeature(out_feat)
            out_layer.SyncToDisk()
        pbar.close()


if __name__ == '__main__':
    # ShpPolygon.merge_shp(r'G:\GIS\Lake\Landsat8\Segmentation\val\SHP', r'G:\GIS\Lake\Landsat8\Segmentation\val\SHP\Union\merge.shp')
    # ShpPolygon.calc_area(r'G:\GIS\Nepal\GoogleBing\Segmentation\val\SHP')
    # ShpPolygon.remove_by_numattr({'Area': ['< 100']}, r'G:\GIS\Nepal\GoogleBing\Segmentation\val\SHP\union.shp')
    # ShpPolygon.remove_by_strattr({'Name': ['1', '3']}, r'G:\GIS\Test\SHP')
    ShpPolygon.union(r'G:\GIS\Lake\Landsat8\Segmentation\val\SHP\Union\merge.shp', r'G:\GIS\Lake\Landsat8\Segmentation\val\SHP\Union\merge.shp', r'G:\GIS\Lake\Landsat8\Segmentation\val\SHP\Union\merge2.shp')
    # ShpPolygon.intersection(r'G:\GIS\Test\SHP\1.shp', r'G:\GIS\Test\SHP\mask.shp', r'G:\GIS\Test\SHP\GeoProcessing\union.shp')
    # print(ShpPolygon.sum_numattr('Area', r'G:\GIS\Nepal\GoogleBing\Segmentation\val\SHP\intersection.shp'))
    # print(ShpPolygon.mean_numattr('Area', r'G:\GIS\Nepal\GoogleBing\Truth\val\SHP\val.shp'))
    # print(ShpPolygon.max_numattr('Area', r'G:\GIS\Nepal\GoogleBing\Truth\val\SHP\val.shp'))
    # print(ShpPolygon.min_numattr('Area', r'G:\GIS\Nepal\GoogleBing\Truth\val\SHP\val.shp'))
    exit(0)
