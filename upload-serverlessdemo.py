import boto3
from botocore.client import Config
import StringIO
import zipfile
import mimetypes


def lambda_handler(event, context):
   s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
   serverlessdemo_bucket = s3.Bucket('demoserverlessgqv')
   serverlessbuild = s3.Bucket('demoserverlessbuild')
   serverless_zip = StringIO.StringIO()
   serverlessbuild.download_fileobj('serverlessdemobuild.zip',serverless_zip)
   with zipfile.ZipFile(serverless_zip) as mzip:
      for nm in mzip.namelist():
         obj = mzip.open(nm)
         serverlessdemo_bucket.upload_fileobj(obj, nm,ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
         serverlessdemo_bucket.Object(nm).Acl().put(ACL='public-read')
    
   print 'Terminado Ejecucion'

   return 'Terminado despliegue por lamnda'
