from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import open
from future import standard_library

import os
import json
import smtplib
import tldextract
from email.mime.text import MIMEText
from urllib import parse as urlparse

import aiobotocore
from botocore.exceptions import ClientError

standard_library.install_aliases()


def send_email(
    sender,
    pwd,
    recipients,
    subject='Email from Python',
    body='',
    smtp='smtp.gmail.com:465',
):
    """Sends a text-only email to recipients; body can be str or filepath."""
    recipients = recipients if isinstance(recipients, list) else [recipients]
    body = open(body, 'rb').read() if os.path.isfile(body) else body
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'DdL <{}>'.format(sender)
    msg['To'] = ', '.join(recipients)
    smtp_obj = smtplib.SMTP_SSL(smtp)
    smtp_obj.ehlo()
    smtp_obj.login(sender, pwd)
    failures = smtp_obj.sendmail(sender, recipients, msg.as_string())
    smtp_obj.close()
    return failures


def extract_domain(url, with_subdomain=False):
    """Extract domain from url, needs a proper domain/suffix.

    with_subdomain=True
        Return a Fully Qualified Domain Name with suffix.
    with_subdomain=False
        Return only the registered domain with suffix.
    """
    assert isinstance(url, str) and url, f'Input "{url}" is not accepted'
    url = url.replace('\xa0', ' ').strip(' \n')
    if with_subdomain:
        fqdn = tldextract.extract(url).fqdn.lower()
        return fqdn[4:] if fqdn.startswith('www.') else fqdn
    else:
        return tldextract.extract(url).registered_domain.lower()


class S3io():
    """
    Interact with s3 using basic I/O functionality.

    Before initializing the class, one needs to have (implicitly) called

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    """

    def __init__(
        self,
        aiobotocore_client=None,
        aws_access_key_id=None,
        aws_secret_access_key=None,
        region_name='eu-central-1',
        **kwargs,
    ):
        self.loop = asyncio.get_event_loop()
        if aiobotocore_client is not None:
            self.s3 = aiobotocore_client
        else:
            client_config = {'service_name': 's3', 'region_name': region_name}
            aws_access_key_id = aws_access_key_id or os.environ.get('AWS_ACCESS_KEY_ID')  # noqa
            aws_secret_access_key = aws_secret_access_key or os.environ.get('AWS_SECRET_ACCESS_KEY')  # noqa
            if aws_access_key_id is not None:
                client_config.update({'aws_access_key_id': aws_access_key_id})
            if aws_secret_access_key is not None:
                client_config.update({'aws_secret_access_key': aws_secret_access_key})  # noqa
            self.s3 = aiobotocore.get_session(
                loop=self.loop,
            ).create_client(
                **client_config,
            )

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc_info):
        try:
            await self.s3.close()
        except AttributeError:
            pass

    @staticmethod
    def _parse_s3_path(s3_path):
        if not s3_path.startswith('s3://'):
            s3_path = 's3://' + s3_path.strip('/')
        parsed = urlparse.urlparse(s3_path)
        return parsed.netloc, parsed.path[1:]

    async def object_exists(self, s3_path):
        bucket, key = self._parse_s3_path(s3_path)
        try:
            # aiobotocore==0.10.2 needs 'region_name' in create_client
            await self.s3.head_object(Bucket=bucket, Key=key)
        except ClientError as e:
            if e.response['ResponseMetadata']['HTTPStatusCode'] == 404:
                return False
            else:
                raise
        else:
            return True

    async def read_bytes(self, s3_path):
        bucket, key = self._parse_s3_path(s3_path)
        response = await self.s3.get_object(Bucket=bucket, Key=key)
        async with response['Body'] as stream:
            return await stream.read()

    async def read_text(self, s3_path, encoding='utf-8'):
        body = await self.read_bytes(s3_path)
        return body.decode(encoding)

    async def read_json(self, s3_path):
        body = await self.read_text(s3_path, 'utf-8')
        return json.loads(body)

    async def write_object(self, body, s3_path, encoding='utf-8'):
        bucket, key = self._parse_s3_path(s3_path)
        if not isinstance(body, (bytes, str)):
            body = json.dumps(body, indent=2)
        if isinstance(body, str):
            body = body.encode(encoding)
        await self.s3.put_object(Bucket=bucket, Key=key, Body=body)

    async def delete_object(self, s3_path):
        bucket, key = self._parse_s3_path(s3_path)
        await self.s3.delete_object(Bucket=bucket, Key=key)

    async def copy_object(self, s3_path_old, s3_path_new):
        bucket, key = self._parse_s3_path(s3_path_new)
        source = os.path.join(*self._parse_s3_path(s3_path_old))
        try:
            await self.s3.copy_object(Bucket=bucket, Key=key, CopySource=source)
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                raise FileNotFoundError(s3_path_old)
            else:
                raise

    async def move_object(self, s3_path_old, s3_path_new):
        await self.copy_object(s3_path_old, s3_path_new)
        await self.delete_object(s3_path_old)

    async def list_objects(self, bucket, prefix=None, recursive=True):
        paginator = self.s3.get_paginator('list_objects_v2')
        config = {'Bucket': bucket}
        if prefix:
            config.update({'Prefix': prefix})
        if not recursive:
            config.update({'Delimiter': '/'})

        objects = []
        async for result in paginator.paginate(**config):
            for _object in result.get('Contents', []):
                objects.append(_object)
        return objects

    async def list_keys(
        self,
        bucket,
        prefix=None,
        suffix=None,
        recursive=True,
        date_sort=True,
        reverse=False,
    ):
        objects = await self.list_objects(bucket, prefix, recursive)
        if date_sort:
            objects = sorted(
                objects,
                key=lambda obj: int(obj['LastModified'].strftime('%s')),
                reverse=reverse,
            )
        return [
            o['Key'] for o in objects if not suffix or o['Key'].endswith(suffix)
        ]

    async def list_folders(
        self,
        bucket,
        prefix=None,
        recursive=True,
        date_sort=True,
        reverse=False,
    ):
        prefix = prefix.lstrip('/')
        keys = await self.list_keys(
            bucket=bucket,
            prefix=prefix,
            suffix=None,
            recursive=True,
            date_sort=date_sort,
            reverse=True,
        )
        prefix_is_folder = keys[0].replace(prefix, '', 1).startswith('/')
        if prefix_is_folder:
            prefix += '/'

        folders = []
        for key in keys:
            # remove prefix and filename from key
            components = key.replace(prefix, '', 1).split('/')[:-1]
            if components:
                components = components if recursive else [components[0]]
                subfolder = prefix + '/'.join(components)
                folders.append(subfolder) if subfolder not in folders else None
        return folders if reverse else folders[::-1]


async def main():
    async with S3io() as s3:
        print(await s3.list_folders('test-bucket', 'test/sub/folder/'))

if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
