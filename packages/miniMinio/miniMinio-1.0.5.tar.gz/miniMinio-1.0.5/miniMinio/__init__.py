import datetime
import os
import shutil
import time

import xlrd
from loguru import logger
from minio import Minio, ResponseError

from miniMinio.utils import get_attributes_minio, get_attributes_local, get_attributes_single_local

exclude = {".minio.sys"}


def create_connection(hostname,
                      access_key=None,
                      secret_key=None,
                      secure=True, **kwargs):
    """

    :param hostname: string 'hostname:port' for Minio File server OR 'local' for local file server
    :param access_key: access key
    :param secret_key:
    :param secure:
    :return:
    """
    if hostname == "local" or hostname == "remote":
        return hostname
    else:
        client = Minio(hostname,
                       access_key=access_key,
                       secret_key=secret_key,
                       secure=secure)

    return client


def get_buckets(client, remote_dir=None):
    """
    :param client: Minio connection object, or 'local' for local filesystem. If remote, add in directory
    :return:
    """

    store = []
    if client == "local" or client == "remote":
        if client is "local":
            remote_dir = os.getcwd()
        for dirpath, dirs, filenames in os.walk(remote_dir, topdown=True):
            dirs[:] = set(dirs) - exclude
            for f in filenames:
                if f[0] == ".":
                    continue
                else:
                    path = os.path.abspath(os.path.join(dirpath, f))
                    store.append([path, datetime.datetime.strptime(time.ctime(os.path.getctime(path)),
                                                                   "%a %b %d %H:%M:%S %Y")])
    else:
        all_buckets = client.list_buckets()
        for bucket in all_buckets:
            store.append([bucket.name, bucket.creation_date])
    return store


def get_all_object_details_in_bucket(client, bucket_name=None, attributes=None,
                                     filter_object=("file", "folder"), filter_prefix = '', ext=None, **kwargs):
    """
    :param attributes: list - Desired attributes to return for every object
    :param client: Minio connection object
    :param bucket_name: str bucket name, or file path of root to start search from
    :param filter_object: tuple of str - 'file', 'folder'
    :param ext: tuple of str - desired extensions
    :return:
    """
    if ext is not None:
       ext = ["."+ex for ex in ext]
    if attributes is None:
        attributes = ["object_name", "last_modified"]
    store = []
    if client == "local" or client == "remote":
        if client is "local":
            bucket_name = os.getcwd()
        bucket_name = os.path.join(bucket_name, filter_prefix)
        for path, subdirs, files in os.walk(bucket_name, topdown=True):
            subdirs[:] = set(subdirs) - exclude
            if "file" in filter_object:
                # file or excel
                store = get_attributes_local(files, path, store, ext)
            if "folder" in filter_object:
                store = get_attributes_local(subdirs, path, store, ext)
    else:
        all_objects = client.list_objects(bucket_name, prefix=filter_prefix, recursive=True)
        for s3_object in all_objects:
            # Check if folder
            if (s3_object.is_dir) and ("folder" in filter_object):
                store = get_attributes_minio(attributes, s3_object, store)
                continue
            # Check if file
            elif (not s3_object.is_dir) and ("file" in filter_object):
                if ext is None:
                    store = get_attributes_minio(attributes, s3_object, store)
                else:
                    filename, filename_ext = os.path.splitext(s3_object.object_name)
                    if filename_ext in ext:
                        store = get_attributes_minio(attributes, s3_object, store)

    return store


def get_object_details_in_bucket(client, object_name, bucket_name=None, attributes=None, **kwargs):
    """

    :param client:
    :param object_name:
    :param bucket_name:
    :param attributes:
    :return:
    """
    store = []
    if attributes is None:
        attributes = ["object_name", "last_modified"]
    if client == "local" or client == "remote":
        path = object_name
        store = get_attributes_single_local(path, attributes)
    else:
        all_objects = client.list_objects(bucket_name, prefix='', recursive=True)
        for s3_object in all_objects:
            # Check if folder
            if object_name.lower() not in s3_object.object_name.lower():
                continue
            else:
                store = get_attributes_minio(attributes, s3_object, store)
    return store[0]


def get_object_path(client, bucket_name, filename):
    # TODO: Test
    # TODO: local
    store = []
    store_error = []
    counter = [0, 0]
    output = []
    all_objects = client.list_objects(bucket_name, prefix='', recursive=True)
    for s3_object in all_objects:
        # Check if folder
        if filename.lower() not in s3_object.object_name.lower():
            counter[1] += 1
            store_error.append(getattr(s3_object, 'object_name'))
        else:
            counter[0] += 1
            store.append(getattr(s3_object, 'object_name'))
    output.extend([store, store_error, counter])
    return output


def get_objects_in_bucket(client, bucket_name=None,
                              filter_object=("file", "folder"), filter_prefix = '', ext=None, **kwargs):
    """
    :param client: Minio connection object
    :param bucket_name: str bucket name, or file path of root to start search from
    :param filter_object: tuple of str - 'file', 'folder'
    :param ext: tuple of str - desired extensions
    :return:
    """
    if ext is not None:
       ext = ["."+ex for ex in ext]
    store = []
    if client == "local" or client == "remote":
        if client is "local":
            bucket_name = os.getcwd()
        bucket_name = os.path.join(bucket_name, filter_prefix)
        for path, subdirs, files in os.walk(bucket_name, topdown=True):
            subdirs[:] = set(subdirs) - exclude
            if "file" in filter_object:
                # file
                for file in files:
                    with open(os.path.join(path, file), "rb") as f:
                        store.append(f.read())
            if "folder" in filter_object:
                for subdir in subdirs:
                    with open(os.path.join(path, subdir), "rb") as f:
                        store.append(f.read())
    else:
        all_objects = client.list_objects(bucket_name, prefix=filter_prefix, recursive=True)
        for s3_object in all_objects:
            # Check if folder
            if (s3_object.is_dir) and ("folder" in filter_object):
                store.append(s3_object)
                continue
            # Check if file
            elif (not s3_object.is_dir) and ("file" in filter_object):
                if ext is None:
                    store.append(s3_object)
                else:
                    filename, filename_ext = os.path.splitext(s3_object.object_name)
                    if filename_ext in ext:
                        store.append(s3_object)
    return store


def get_single_object_from_bucket_to_file(client, object_name, dir_path, bucket_name=None, **kwargs):
    """
    :param client:
    :param bucket_name:
    :param object_name:
    :param dir_path: desired local path relative to the working directory
    :return: transfers files to dir_path
    """
    if client == "local" or client == "remote":
        shutil.copy2(object_name, dir_path)
    else:
        try:
            client.fget_object(bucket_name, object_name, dir_path)
        except ResponseError as err:
            logger.error(err)
    return


def get_single_object_content_bytes(client, object_name, bucket_name=None):
    """
    :param client:
    :param bucket_name:
    :param object_name:
    :return:
    """
    if client == "local" or client == "remote":
        in_file = open(object_name, "rb")
        data = in_file.read()
        return data
    else:
        result = []
        try:
            data = client.get_object(bucket_name, object_name)
            for d in data.stream(32 * 1024):
                result.append(d)
            return b''.join(result)
        except ResponseError as err:
            return err


def get_single_excel_file_content(client, excel_file_object, bucket_name=None, **kwargs):
    """
    :param client:
    :param bucket_name:
    :param excel_file_object:
    :return:
    """
    if client == "local" or client == "remote":
        return xlrd.open_workbook(excel_file_object)
    else:
        result = []
        try:
            data = client.get_object(bucket_name, excel_file_object)
            for d in data.stream(32 * 1024):
                result.append(d)
            return xlrd.open_workbook(file_contents=b''.join(result))
        except ResponseError as err:
            return err
