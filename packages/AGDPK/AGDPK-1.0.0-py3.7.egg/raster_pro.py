# -*- coding: utf-8 -*-
import os
import glob
import numpy as np
import imageio
from tqdm import tqdm
import time
from osgeo import gdal
from osgeo import osr
from osgeo import ogr
from osgeo.gdalconst import GA_Update


class GeoTiff:
    @staticmethod
    def to_img(img_format, gtif_path, save_path):
        gtifs = []
        if os.path.isdir(gtif_path):
            gtifs = glob.glob(gtif_path + r'\*.tif')
        elif os.path.isfile(gtif_path):
            if '.tif' in gtif_path or '.TIF' in gtif_path:
                gtifs.append(gtif_path)
        else:
            print('input path error.')
            exit(0)

        print('Geotiff convert to {0}:'.format(str.upper(img_format)))
        print(gtif_path)

        pbar = tqdm(total=len(gtifs))
        for gtif in gtifs:
            time.sleep(0.05)
            pbar.update(1)

            gtif_name = os.path.split(gtif)[-1]
            file_name = os.path.splitext(gtif_name)[0]
            src_ds = gdal.Open(gtif)
            if src_ds is None:
                # print('unable to open raster file:', gtif_name, '.')
                continue

            ncol = src_ds.RasterXSize
            nrow = src_ds.RasterYSize
            nband = src_ds.RasterCount
            data_uint8 = np.zeros((nrow, ncol, nband), dtype=np.uint8)
            for i in range(nband):
                srcband = src_ds.GetRasterBand(i + 1)
                data_origin = srcband.ReadAsArray(0, 0, ncol, nrow)
                if data_origin.dtype == np.uint8:
                    data_uint8[:, :, i] = data_origin
                else:
                    data_float = data_origin.astype(np.float)
                    data_unique = np.unique(data_float)
                    data_unique = data_unique.argsort()
                    # 取第二的最大最小值，防止黑边白边干扰
                    data_max = data_unique[-2]
                    data_min = data_unique[1]
                    data_float = (data_float - data_min) / (data_max - data_min) * 255
                    data_uint8 = data_float.astype(np.uint8)
            imageio.imwrite(os.path.join(save_path, file_name + '.' + img_format), data_uint8)
        pbar.close()

    @staticmethod
    def clip_by_size(clip_size, gtif_path, save_path):
        gtifs = []
        if os.path.isdir(gtif_path):
            gtifs = glob.glob(gtif_path + r'\*.tif')
        elif os.path.isfile(gtif_path):
            if '.tif' in gtif_path or '.TIF' in gtif_path:
                gtifs.append(gtif_path)
        else:
            print('input path error.')
            exit(0)

        print('Clip Geotiff with the size of ({0} * {1}) :'.format(clip_size[0], clip_size[1]))
        print(gtif_path)

        # Stop GDAL printing both warnings and errors to STDERR
        gdal.PushErrorHandler('CPLQuietErrorHandler')
        # Make GDAL raise python exceptions for errors (warnings won't raise an exception)
        gdal.UseExceptions()

        pbar = tqdm(total=len(gtifs))
        for gtif in gtifs:
            time.sleep(0.05)
            pbar.update(1)
            gtif_name = os.path.split(gtif)[-1]
            file_name = os.path.splitext(gtif_name)[0]
            src_ds = gdal.Open(gtif)
            if src_ds is None:
                # print('unable to open raster file:', gtif_name, '.')
                continue

            ncol = src_ds.RasterXSize
            nrow = src_ds.RasterYSize
            nband = src_ds.RasterCount

            src_data = []
            src_color = []
            for i in range(nband):
                srcband = src_ds.GetRasterBand(i + 1)
                src_data.append(srcband.ReadAsArray(0, 0, ncol, nrow))
                src_color.append(srcband.GetColorInterpretation())

            projection = src_ds.GetProjection()
            geotransform = src_ds.GetGeoTransform()

            dsize = clip_size
            dheight = int(nrow / dsize[0])
            dwidth = int(nrow / dsize[1])
            for i in range(dheight):
                for j in range(dwidth):
                    driver = gdal.GetDriverByName('GTiff')
                    out_ds = driver.Create(os.path.join(save_path, '{0}_{1}_{2}.tif'.format(file_name, str(i), str(j))), dsize[1], dsize[0], nband, gdal.GDT_Byte)

                    lux = geotransform[0] + j * dsize[1] * geotransform[1] + i * dsize[0] * geotransform[2]
                    luy = geotransform[3] + j * dsize[1] * geotransform[4] + i * dsize[0] * geotransform[5]
                    out_geom = (lux, geotransform[1], geotransform[2], luy, geotransform[4], geotransform[5])
                    out_ds.SetGeoTransform(out_geom)
                    out_ds.SetProjection(projection)

                    for k in range(nband):
                        out_data = src_data[k][(i * dsize[0]):((i + 1) * dsize[0]), (j * dsize[1]):((j + 1) * dsize[1])]
                        out_band = out_ds.GetRasterBand(k + 1)
                        out_band.WriteArray(out_data)
                        out_band.SetColorInterpretation(src_color[k])
                del out_ds
        pbar.close()

    @staticmethod
    def from_img_wf(epsg_code, img_format, wf_format, img_bands, img_path, wf_path, save_path):
        if not img_bands:
            img_bands = [0, 1, 2]

        imgs = []
        wf_dir = ''
        if os.path.isdir(img_path) and os.path.isdir(wf_path):
            imgs = glob.glob(img_path + r'\*.' + img_format)
            wf_dir = wf_path
        if os.path.isfile(img_path) and os.path.isdir(wf_path):
            if '.' + img_format in img_path and '.' + wf_format in wf_path:
                imgs.append(img_path)
                wf_dir = os.path.split(wf_path)[0]
        if not imgs:
            print('input path error.')
            exit(0)

        print('Creat GeoTiff with {0} and {1}:'.format(str.upper(img_format), str.upper(wf_format)))
        print(img_path)

        pbar = tqdm(total=len(imgs))
        for img in imgs:
            time.sleep(0.05)
            pbar.update(1)

            img_name = os.path.split(img)[-1]
            file_name = os.path.splitext(img_name)[0]
            wf_name = file_name + '.' + wf_format
            wf = os.path.join(wf_dir, wf_name)
            if not os.path.exists(wf):
                # print(wf_name, 'is not found.')
                continue

            img_data = imageio.imread(img)

            wf_paras = []
            with open(wf, 'r') as f:
                wf_para = f.readline()
                while wf_para:
                    wf_paras.append(float(wf_para))
                    wf_para = f.readline()
            geotransform = (wf_paras[4], wf_paras[0], wf_paras[1], wf_paras[5], wf_paras[2], wf_paras[3])

            driver = gdal.GetDriverByName('GTiff')
            new_raster = driver.Create(os.path.join(save_path, file_name + '.tif'), img_data.shape[1], img_data.shape[0], len(img_bands), gdal.GDT_Byte)
            new_raster.SetGeoTransform(geotransform)

            new_band = None
            for i in range(len(img_bands)):
                new_band = new_raster.GetRasterBand(i + 1)
                new_band.WriteArray(img_data[:, :, img_bands[i]])

            new_raster_srs = osr.SpatialReference()
            new_raster_srs.ImportFromEPSG(epsg_code)
            new_raster.SetProjection(new_raster_srs.ExportToWkt())
            new_band.FlushCache()
        pbar.close()

    @staticmethod
    def from_img_gtif(img_format, img_bands, img_path, gtif_path, save_path):
        if not img_bands:
            img_bands = [0, 1, 2]

        imgs = []
        gtif_dir = ''
        if os.path.isdir(img_path) and os.path.isdir(gtif_path):
            imgs = glob.glob(img_path + r'\*.' + img_format)
            gtif_dir = gtif_path
        if os.path.isfile(img_path) and '.' + img_format in img_path:
            if '.' + img_format in img_path and '.tif' in gtif_path:
                imgs.append(img_path)
                gtif_dir = os.path.split(gtif_path)[0]
        if not imgs:
            print('input path error.')
            exit(0)

        print('Creat GeoTiff with {0} and GeoTiff:'.format(str.upper(img_format)))
        print(img_path)

        pbar = tqdm(total=len(imgs))
        for img in imgs:
            time.sleep(0.05)
            pbar.update(1)

            img_name = os.path.split(img)[-1]
            file_name = os.path.splitext(img_name)[0]
            gtif_name = file_name + '.tif'
            gtif = os.path.join(gtif_dir, gtif_name)
            if not os.path.exists(gtif):
                # print(gtif_name, 'is not found.')
                continue

            img_data = imageio.imread(img)

            src_ds = gdal.Open(os.path.join(gtif_dir, gtif_name))
            if src_ds is None:
                # print('unable to open raster file:', gtif_name, '.')
                continue
            geotransform = src_ds.GetGeoTransform()
            projection = src_ds.GetProjection()

            driver = gdal.GetDriverByName('GTiff')
            new_raster = driver.Create(os.path.join(save_path, file_name + '.tif'), img_data.shape[1],
                                       img_data.shape[0], len(img_bands), gdal.GDT_Byte)
            new_raster.SetGeoTransform(geotransform)

            new_band = None
            for i in range(len(img_bands)):
                new_band = new_raster.GetRasterBand(i + 1)
                new_band.WriteArray(img_data[:, :, img_bands[i]])

            # new_raster_srs = osr.SpatialReference()
            # new_raster_srs.ImportFromEPSG(epsg_code)
            new_raster.SetProjection(projection)
            new_band.FlushCache()
        pbar.close()

    @staticmethod
    def set_nodata(nodata_val, gtif_path):
        gtifs = []
        if os.path.isdir(gtif_path):
            gtifs = glob.glob(gtif_path + r'\*.tif')
        elif os.path.isfile(gtif_path):
            if '.tif' in gtif_path or '.TIF' in gtif_path:
                gtifs.append(gtif_path)
        else:
            print('input path error.')
            exit(0)

        print('Set nodata value of Geotiff:')
        print(gtif_path)

        pbar = tqdm(total=len(gtifs))
        for gtif in gtifs:
            time.sleep(0.05)
            pbar.update(1)

            src_ds = gdal.Open(gtif, GA_Update)
            if src_ds is None:
                # print('unable to open raster file:', gtif_name)
                continue

            nband = src_ds.RasterCount
            for i in range(nband):
                src_band = src_ds.GetRasterBand(i + 1)
                # 注意黑边的数值,也可能是白边
                src_band.SetNoDataValue(nodata_val)
        pbar.close()

    @staticmethod
    def gtif_to_shp(gtif_path, save_path):
        gtifs = []
        if os.path.isdir(gtif_path):
            gtifs = glob.glob(gtif_path + r'\*.tif')
        elif os.path.isfile(gtif_path):
            if '.tif' in gtif_path or '.TIF' in gtif_path:
                gtifs.append(gtif_path)
        else:
            print('input path error.')
            exit(0)

        print('Convert Geotiff to ShapeFile:')
        print(gtif_path)

        # Stop GDAL printing both warnings and errors to STDERR
        gdal.PushErrorHandler('CPLQuietErrorHandler')
        # Make GDAL raise python exceptions for errors (warnings won't raise an exception)
        gdal.UseExceptions()

        pbar = tqdm(total=len(gtifs))
        for gtif in gtifs:
            time.sleep(0.05)
            pbar.update(1)

            gtif_name = os.path.split(gtif)[-1]
            file_name = os.path.splitext(gtif_name)[0]
            src_ds = gdal.Open(gtif)
            if src_ds is None:
                # print('unable to open gtif file:', gtif_name)
                continue

            print(src_ds.GetProjection())
            exit(0)
            srs = osr.SpatialReference(wkt=src_ds.GetProjection())
            src_band = src_ds.GetRasterBand(1)
            dst_layer_name = "POLYGONIZED_STUFF"
            driver = ogr.GetDriverByName("ESRI Shapefile")
            dst_ds = driver.CreateDataSource(os.path.join(save_path, file_name + '.shp'))
            dst_layer = dst_ds.CreateLayer(dst_layer_name, srs=srs)
            gdal.Polygonize(src_band, src_band, dst_layer, -1, [], callback=None)
        pbar.close()


if __name__ == '__main__':
    # GeoTiff.to_img('png', r'G:\GIS\Test\LC81320402017350LGN00', r'G:\GIS\Test')
    # GeoTiff.clip_by_size([1000, 1000], r'G:\GIS\Lake\Landsat8', r'G:\GIS\Lake\Landsat8\TIF')
    # GeoTiff.from_img_wf(3857, 'png', 'pgw', [], r'G:\GIS\Test', r'G:\GIS\Test', r'G:\GIS\Test')
    # GeoTiff.from_img_gtif('png', [0], r'G:\GIS\Lake\Landsat8\Segmentation\val\IMG', r'G:\GIS\Lake\Landsat8\TIF', r'G:\GIS\Lake\Landsat8\Segmentation\val\TIF')
    # GeoTiff.set_nodata(0, r'G:\GIS\Test')
    GeoTiff.gtif_to_shp(r'G:\GIS\Lake\Landsat8\Segmentation\val\TIF', r'G:\GIS\Lake\Landsat8\Segmentation\val\SHP')
    exit(0)
