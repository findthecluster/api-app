## Job to extract information from DynamoDB, write it into a CSV file and add it to S3.
import csv
import json
import decimal
import boto3
from botocore.exceptions import NoCredentialsError

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            return int(o)
        return super(DecimalEncoder, self).default(o)

def extract_and_transform():
    dynamo_db = boto3.resource('dynamodb')
    table = dynamodb.Table('survey-app-dump')

    items = table.scan()['Items']

    json_data = []

    for item in items:
        json_data.append(json.dumps(item, cls=DecimalEncoder))
    
    csv_file = open('toS3.csv', 'w') # Open the CSV file to write into

    csv_writer = csv.writer(csv_file)

    #Write the first line as the header row
    csv_writer.writerow(json_data[0].keys())

    # Write the data row by row
    for row in json_data:
        csv_writer.writerow(row.values())
    
def write_to_s3(csv_filename, bucket_name, target_filename):
    s3_bucket = boto3.resource('s3')
    try:
        s3_bucket.meta.client.upload_file(csv_filename, bucket_name, target_filename) 
    except NoCredentialsError:
        print('[ERROR]: Invalid AWS credentials')
    except FileNotFoundError:
        pass



if __name__ == '__main__':
    extract_and_transform()
    # TODO: Push the CSV file into S3
    write_to_s3('toS3.csv', 'bucket-name', 'data.csv') # TODO: Configure name of bucket 
    # TODO: Establish context to make this a job
    pass

