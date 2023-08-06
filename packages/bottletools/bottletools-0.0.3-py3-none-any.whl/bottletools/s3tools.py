import boto3
from io import StringIO

s3_resource = boto3.resource('s3')

def get_s3_data(key, bucket_name):
    """Returns full root path of file """
    s3_user_cluster_csv = s3_resource.Object(bucket_name, key)
    return s3_user_cluster_csv.get()['Body'].read().decode('utf-8')


def get_s3_data_path_stringio(key, bucket_name):
    return StringIO(get_s3_data(key, bucket_name))


def dump(bucket_name, export_file_name, string_to_write): 
    s3_resource.Object(bucket_name, export_file_name).put(Body=string_to_write)


def get_public_url(bucket_name, key, expire_sec):
    return boto3.client('s3').generate_presigned_url('get_object',Params={'Bucket': bucket_name,'Key': key}, ExpiresIn=expire_sec)