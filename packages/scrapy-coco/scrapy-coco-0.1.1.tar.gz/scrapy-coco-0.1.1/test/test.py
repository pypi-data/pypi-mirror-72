import os
import sys

sys.path.append('/home/m3ck0/dev/coco/coco')  # noqa

from coco.app import Application


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAN_DIR = os.path.join(BASE_DIR, 'manifests')

APP = Application(MAN_DIR)
APP()
