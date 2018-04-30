from django.test import TestCase

# Create your tests here.
def ImportingCSV(file):
    #from crm.models import ProductDetail
    import csv
#    csv_reader = csv.reader(open(file, encoding='utf-8'))
    with open(file, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile)
        for i, row in enumerate(csv_reader):
            if i == 0:
                print(row)
                continue
            IsPub = False
            if row[15] == '1':
                IsPub = True
            '''
            pd = ProductDetail(model=row[0], productname=row[1], category=row[2], brand=row[3], series=row[4],
                               certificate=row[5], goldType=row[6], goldContent=row[7], diamondWeight=row[8],
                               size=row[9], productprice=row[10], rentalprice=row[11], rentcycle=row[12],
                               reletcycle=row[13], guarantee=row[14], releaseStatus=IsPub, remark=row[16])
            pd.save()
            '''


if __name__ == '__main__':
    ImportingCSV('upload 20180428.csv')