# -*- coding: utf-8 -*-
from rest_framework import serializers
from crm.models import ProductDetail
import datetime
import os
from periodic.tasks import ImportingCSV


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
    mainImage1 = ThumbnailImageField(source='image1', size_alias='medium')
    mainImage2 = ThumbnailImageField(source='image2', size_alias='medium')
    mainImage3 = ThumbnailImageField(source='image3', size_alias='medium')
    mainImage4 = ThumbnailImageField(source='image4', size_alias='medium')
    mainImage5 = ThumbnailImageField(source='image5', size_alias='medium')
    mainImage6 = ThumbnailImageField(source='image6', size_alias='medium')

    class Meta:
        model = ProductDetail
        exclude = ('reserved', 'gmt_create', 'gmt_modified', 'createdBy', 'lastModifiedBy')
        # read_only_fields = ('productid', )

    # def post(self):

    def create(self, validated_data):
        if validated_data.has_key('productid'):
            # update
            pid = validated_data.pop('productid')
            try:
                p = ProductDetail.objects.get(productid=pid)
            except ProductDetail.DoesNotExist:
                raise serializers.ValidationError(detail={"message": "无效的productid"})

            self.update(p, validated_data)
        else:  # new
            return self.save()


def ImportCSV(file):
    from crm.models import ProductDetail
    import csv
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

    with open(file, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile)
        for i, row in enumerate(csv_reader):
            for ii, xi in enumerate(row):
                row[ii] = xi.decode('gbk')
            if i == 0:
                print(row)
                continue
            IsPub = False
            if row[15] == '1':
                IsPub = True

            if not CATEGORY.has_key(str(row[2])):
                print "error!!"

            param = {
                'productname': row[1], 'category': CATEGORY[str(row[2])], 'brand': row[3], 'series': row[4],
                'certificate': row[5], 'goldType': row[6], 'goldContent': row[7], 'diamondWeight': float(row[8]),
                'size': row[9], 'productprice': float(row[10]), 'rentalprice': float(row[11]),
                'rentcycle': int(row[12]), 'model' : row[0],
                'reletcycle': int(row[13]), 'guarantee': float(row[14]), 'releaseStatus': IsPub, 'remark': row[16]
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
            obj, created = ProductDetail.objects.update_or_create(model=row[0] ,defaults=param)




class ProductFileSerializer(serializers.Serializer):
    OriFile = serializers.FileField(write_only=True)

    class Meta:
        fields = ('OriFile', 'username', 'password')

    def create(self, validated_data):
        filedata = validated_data['OriFile']
        filedir = 'media/ImportData/' + datetime.datetime.now().strftime("IMPORT%y-%m-%d[%H:%M:%S]")
        if not os.path.exists(filedir):
            os.mkdir(filedir)
        dest = open(filedir + '/' + filedata.name, 'wb+')
        for chunk in filedata.chunks():
            dest.write(chunk)
        dest.close()
        try:
            ImportCSV('upload 20180428.csv')
            # r = ImportingCSV.delay(filedir+'/'+filedata.name)
        except Exception, e:
            raise serializers.ValidationError(e.message)
        return filedata.name
