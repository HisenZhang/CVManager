import base64


def img2b64(imgpath):
    with open(imgpath, 'rb') as f:
        return base64.b64encode(f.read()).decode()


def intersect(a, b):
    return set(a).intersection(set(b))
