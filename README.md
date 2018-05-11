# Multipart Upload

This is an example of how to perform [S3 Multipart Upload](https://docs.aws.amazon.com/AmazonS3/latest/dev/mpuoverview.html) with Python. The procedure is as follows:

1. Inform S3 that a multipart upload is incoming with `create_multipart_upload`
2. Select a part_size (e.g. 6 MiB) and perform separate `upload_part` operations of a large file. This is done sequentially in this example, but at scale this should be parallelized.
3. Inform S3 that the upload is complete via `complete_multipart_upload`. S3 will assemble the parts into a single S3 object.


## Dependencies

This project assumes [`pipenv`](https://github.com/pypa/pipenv) is available on the system.

Install the dependencies and activate the shell:

```bash
pipenv install
pipenv shell
```

## Running the Example

Select a file larger than 6MiB and provide the full path for multipart upload. This should be run in an environment with access to [AWS credentials](https://docs.aws.amazon.com/cli/latest/topic/config-vars.html) and permissioned with write access to the chosen bucket.

```bash
./script.py --file /Users/dliggat/Downloads/large-file.txt --bucket dliggat-multi

# INFO:__main__:Namespace(bucket='dliggat-multi', file='/Users/dliggat/Downloads/large-file.txt')
# INFO:__main__:Sending part 1 of 7
# INFO:__main__:Sending part 2 of 7
# INFO:__main__:Sending part 3 of 7
# INFO:__main__:Sending part 4 of 7
# INFO:__main__:Sending part 5 of 7
# INFO:__main__:Sending part 6 of 7
# INFO:__main__:Sending part 7 of 7
# INFO:__main__:Multipart upload of /Users/dliggat/Downloads/large-file.txt to s3://dliggat-multi complete
```

