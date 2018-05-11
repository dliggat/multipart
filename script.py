#!/usr/bin/env python

import argparse
import boto3
import logging
import math
import os
import sys

from filechunkio import FileChunkIO

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


PART_SIZE = 6 * 1024 ** 2  # 6 MiB chunk size.



def upload(bucket, file, key):
    """Perform a multipart upload"""

    # Notify S3 that we're starting a multipart upload. Retain the upload_id.
    client = boto3.client('s3')
    response = client.create_multipart_upload(Bucket=bucket, Key=key)
    upload_id = response['UploadId']
    logger.debug(response)
    source_size = os.stat(file).st_size
    part_count = int(math.ceil(source_size / float(PART_SIZE)))

    # Send the file parts with FileChunkIO to create a file-like object that represents a certain
    # byte range within the original file. At scale, this should be parallelized.
    parts = []
    for i in range(part_count):
        part_number = i + 1
        offset = PART_SIZE * i
        bytes = min(PART_SIZE, source_size - offset)
        logger.info('Sending part {} of {}'.format(part_number, part_count))

        with FileChunkIO(file, 'r', offset=offset, bytes=bytes) as fp:
            resp = client.upload_part(Body=fp.read(), Bucket=bucket, Key=key,
                                      PartNumber=part_number, UploadId=upload_id)
            logger.debug(resp)
            parts.append({'PartNumber': part_number, 'ETag': resp['ETag']})

    # Notify S3 that the multipart upload is complete.
    response = client.complete_multipart_upload(Bucket=bucket, Key=key, UploadId=upload_id,
                                                MultipartUpload={'Parts': parts})
    logger.debug(response)
    logger.info('Multipart upload of {} to s3://{} complete'.format(file, bucket))


def main(argv):
    parser = argparse.ArgumentParser(description='Multipart upload parser example')
    parser.add_argument('--bucket', action="store", required=True)
    parser.add_argument('--file', action="store", required=True)
    args = parser.parse_args()
    logger.info(args)
    key = os.path.basename(args.file)
    upload(args.bucket, args.file, key)


if __name__ == '__main__':
    main(sys.argv)
