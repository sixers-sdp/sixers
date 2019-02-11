import os
from django.conf import settings


map_path = os.path.join(settings.BASE_DIR, '..', 'map', 'map.dot')
with open(map_path) as f:
    map_text = f.read()
