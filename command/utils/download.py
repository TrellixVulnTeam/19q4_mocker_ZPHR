import os
import requests
import tarfile


TMP_TAR_FILE = '/tmp/tmp.tar'
BLOBSUM_KEY = 'blobSum'


def get_dockerhub_authorization_header(image):
    request_token_url = \
        'https://auth.docker.io/token' \
        '?service=registry.docker.io' \
        '&scope=repository:library/' + image + ':pull'
    response = requests.get(request_token_url)
    token = response.json()['token']
    auth_header = {'Authorization': 'Bearer ' + token}
    return auth_header


def get_layers(image, auth_header):
    request_layers_url = \
        'https://registry.hub.docker.com/v2/library/' \
        + image + \
        '/manifests/latest'
    response = requests.get(request_layers_url, headers=auth_header)
    layers = response.json()['fsLayers']
    return layers


def get_single_layer(image, blobsum, auth_header):
    print('Downloading layer with ' + BLOBSUM_KEY + ': ' + blobsum)

    request_layer_url = \
        'https://registry-1.docker.io/v2/library/' \
        + image + \
        '/blobs/' + blobsum
    response = requests.get(request_layer_url, headers=auth_header)
    return response


def download_image_from_dockerhub(image, target_directory):
    auth_header = get_dockerhub_authorization_header(image)
    layers = get_layers(image, auth_header)

    for layer in layers:
        if BLOBSUM_KEY not in layer:
            continue

        with open(TMP_TAR_FILE, 'wb') as tmp_tar:
            response = get_single_layer(image, layer[BLOBSUM_KEY], auth_header)
            for chunk in response.iter_content(chunk_size=1024):
                tmp_tar.write(chunk)

        with tarfile.open(TMP_TAR_FILE) as tf:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tf, str(target_directory))

    os.remove(TMP_TAR_FILE)
