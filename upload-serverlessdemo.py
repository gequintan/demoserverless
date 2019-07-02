import boto3
from botocore.client import Config
import StringIO
import zipfile
import mimetypes


def lambda_handler(event, context):
   sns = boto3.resource('sns')
   topic = sns.Topic('arn:aws:sns:us-east-2:725138479049:deployServerlesDemoTopic')
   location = {
      "bucketName": 'demoserverlessbuild',
      "objectKey": 'serverlessdemobuild.zip'
   }
   job = event.get("CodePipeline.job")
   if job:
      for artifact in job["data"]["inputArtifacts"]:
         if artifact["name"] == "BuildArtif":
             location = artifact["location"]["s3Location"]
   
   print "construyendo serverlesdemo dede" + str(location)
   s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
   serverlessdemo_bucket = s3.Bucket('demoserverlessgqv')
   serverlessbuild = s3.Bucket(location["bucketName"])
   serverless_zip = StringIO.StringIO()
   serverlessbuild.download_fileobj(location["objectKey"],serverless_zip)
   with zipfile.ZipFile(serverless_zip) as mzip:
      for nm in mzip.namelist():
         obj = mzip.open(nm)
         serverlessdemo_bucket.upload_fileobj(obj, nm,ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
         serverlessdemo_bucket.Object(nm).Acl().put(ACL='public-read')
    
   print 'Terminado Ejecucion'
   topic.publish(Subject="Despliege ServerlessContainerDemo",Message="Despliege de ServerlessContainerDemo Exitoso!!")
   if job:
      codepipeline = boto3.client('codepipeline')
      codepipeline.put_job_success_result(jobId=job["id"])

   return 'Terminado despliegue por lamnda'
