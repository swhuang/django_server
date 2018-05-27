# -*- coding: utf-8 -*-
from rest_framework import serializers
from crm.models import ProductDetail
import datetime
import os
from periodic.tasks import ImportCSV
from django.db.utils import DataError
import logging
from crm.server_utils.customerField.Field import *
from easy_thumbnails.exceptions import InvalidImageFormatError
from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.files import ThumbnailerImageFieldFile
from rest_framework.settings import api_settings
import decimal
from django.utils.formats import localize_input

import zipfile


class ThumbnailImageField(serializers.ImageField):
    """
    从 easy_thumbnails.fields.ThumbnailerImageField 字段类型中解析出缩略图信息
    """

    def __init__(self, *args, **kwargs):
        self.size_alias = kwargs.pop('size_alias', 'large')
        kwargs['read_only'] = True
        super(ThumbnailImageField, self).__init__(*args, **kwargs)

    def to_representation(self, value):
        try:
            return value[self.size_alias].url
        except Exception:
            return None





class ProductSerializer(serializers.ModelSerializer):
    MainImage0 = PdImageField(source='image1', required=False)
    MainImage1 = PdImageField(source='image2', required=False)
    MainImage2 = PdImageField(source='image3', required=False)
    MainImage3 = PdImageField(source='image4', required=False)
    MainImage4 = PdImageField(source='image5', required=False)
    MainImage5 = PdImageField(source='image6', required=False)
    detailImages = PdImageField(required=False)
    createdDate = ModifiedDateTimeField(source='gmt_create', read_only=True)
    createdBy = serializers.CharField(read_only=True)
    lastModifiedBy = serializers.CharField(read_only=True)
    lastModified = serializers.DateTimeField(source='gmt_modified', read_only=True)
    sellingPrice = AmountField()
    diamondWeight = StrfloatField(required=False)

    class Meta:
        model = ProductDetail
        exclude = ('reserved', 'gmt_create','gmt_modified',
                   'image1', 'image2', 'image3', 'image4', 'image5', 'image6')
        #read_only_fields = ('productid', )
        write_only_fields = ('image1',)

    def create(self, validated_data):
        if validated_data.has_key('productid'):
            # update
            pid = validated_data.pop('productid', None)
            try:
                p = ProductDetail.objects.get(productid=pid)
            except ProductDetail.DoesNotExist:
                raise serializers.ValidationError(detail={"message": "无效的productid"})

            return self.update(p, validated_data)
        else:  # new
            validated_data[u'createdBy'] = self.context['request'].user.userid
            try:
                return super(ProductSerializer, self).create(validated_data)
            except Exception, e:
                raise serializers.ValidationError(detail={"message": e.message})


def ImportCSV(filedir):
    from crm.models import ProductDetail
    import os
    import csv
    import zipfile
    import logging
    from easy_thumbnails.files import get_thumbnailer
    #    csv_reader = csv.reader(open(file, encoding='utf-8'))
    CATEGORY = {}
    CATEGORY['ALL'] = 0
    CATEGORY['项链'] = 1
    CATEGORY['戒指'] = 2
    CATEGORY['手镯'] = 3
    CATEGORY['耳饰'] = 4
    CATEGORY['手链'] = 5
    CATEGORY['脚饰'] = 6
    CATEGORY['胸针&领针'] = 7
    CATEGORY['摆件'] = 8

    csvfile = None
    Imagefile = None

    for file in os.listdir(filedir):
        if file.split('.')[-1] == 'csv':
            csvfile = file
        elif file == 'Image.zip':
            Imagefile = file

    # init logging
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

    logging.basicConfig(filename=filedir + '.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

    with open(filedir+'/'+csvfile, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile)
        for i, row in enumerate(csv_reader):
            for ii, xi in enumerate(row):
                row[ii] = xi.decode('gbk')
            if i == 0:
                continue
            IsPub = '0'
            if row[15] == '1':
                IsPub = '1'

            if not CATEGORY.has_key(str(row[2])):
                logging.error("Category 没有:" + str(row[2]))

            param = {
                'title': row[1], 'category': CATEGORY[str(row[2])], 'brand': row[3], 'series': row[4],
                'certificate': row[5], 'goldType': row[6], 'goldContent': row[7], 'diamondWeight': float(row[8]),
                'size': row[9], 'sellingPrice': float(row[10]), 'rent': float(row[11]),
                'rentcycle': int(row[12]), 'model': row[0],
                'reletcycle': int(row[13]), 'deposit': float(row[14]), 'releaseStatus': IsPub, 'remark': row[16]
            }
            '''

            pd = ProductDetail(model=row[0], productname=row[1], category=CATEGORY[str(row[2])], brand=row[3],
                               series=row[4],
                               certificate=row[5], goldType=row[6], goldContent=row[7], diamondWeight=float(row[8]),
                               size=row[9], productprice=float(row[10]), rentalprice=float(row[11]),
                               rentcycle=int(row[12]),
                               reletcycle=int(row[13]), guarantee=float(row[14]), releaseStatus=IsPub, remark=row[16])
            pd.save()
            '''
            obj, created = ProductDetail.objects.update_or_create(model=row[0], defaults=param)

    logging.info(csvfile.name + " process compeleted!")

    if not Imagefile:
        logging.warn("No image file found!")
        return False

    azip = zipfile.ZipFile(filedir + '/' + Imagefile)
    os.makedirs(filedir + '/Image')
    azip.extractall(path=filedir + '/Image')
    for file in os.listdir(filedir + '/Image'):
        c_imgfile = file.split('[')
        try:
            pd = ProductDetail.objects.get(model=c_imgfile[0])
        except ProductDetail.DoesNotExist:
            logging.error(file + ":not found")
            continue
        else:
            # todo
            fp = open(filedir + '/Image/' + file)
            thubnailer = get_thumbnailer(fp, relative_name=file)
            pd.image2.save('test.png', thubnailer)
            if c_imgfile[-1][0] == '1':
                pd.image1.save(file, thubnailer, {'size': (200, 200),
                                                  'crop': True})  # = thubnailer.get_thumbnail({'size': (200, 200), 'crop': True})
            elif c_imgfile[-1][0] == '2':
                pd.image2.save(file, thubnailer, {'size': (200, 200), 'crop': True})
            elif c_imgfile[-1][0] == '3':
                pd.image3.save(file, thubnailer, {'size': (200, 200), 'crop': True})
            elif c_imgfile[-1][0] == '4':
                pd.image4.save(file, thubnailer, {'size': (200, 200), 'crop': True})
            elif c_imgfile[-1][0] == '5':
                pd.image5.save(file, thubnailer, {'size': (200, 200), 'crop': True})
            elif c_imgfile[-1][0] == '6':
                pd.image6.save(file, thubnailer, {'size': (200, 200), 'crop': True})
            elif c_imgfile[-1][0] == '0':
                pd.detailImages.save(file, thubnailer, {'size': (200, 200), 'crop': True})
            pd.save()
            fp.close()
            logging.info(file + " added")
    return True


class ProductFileSerializer(serializers.Serializer):
    OriFile = serializers.FileField(write_only=True)
    SixImage = serializers.FileField(write_only=True, required=False)

    class Meta:
        fields = ('OriFile', 'SixImage')

    def create(self, validated_data):
        # excel
        filedata = validated_data['OriFile']
        if filedata.name.split('.')[-1] != 'csv':
            raise serializers.ValidationError("excel文件格式错误 必须为csv")
        filedir = 'media/ImportData/' + datetime.datetime.now().strftime("IMPORT%y-%m-%d[%H:%M:%S]")
        if not os.path.exists(filedir):
            os.mkdir(filedir)
        dest = open(filedir + '/' + filedata.name, 'wb+')
        for chunk in filedata.chunks():
            dest.write(chunk)
        dest.close()

        # Image
        if validated_data.has_key('SixImage'):
            ImageData = validated_data['SixImage']

            if ImageData.name.split('.')[-1] != 'zip':
                raise serializers.ValidationError("图片压缩文件格式错误")
            ImageDest = open(filedir + '/' + 'Image.zip', 'wb+')
            for chunk in ImageData.chunks():
                ImageDest.write(chunk)
            ImageDest.close()

        try:
            ImportCSV(filedir=filedir)
        except DataError, e:
            raise serializers.ValidationError(e.args[1])
        except Exception, e:
            logger = logging.getLogger('django')
            logger.error(e)
            raise serializers.ValidationError(e.message)

        return filedata.name
