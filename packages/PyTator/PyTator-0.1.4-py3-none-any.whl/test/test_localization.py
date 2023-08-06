import datetime
import random
import uuid
import time

import pytator
from ._common import assert_close_enough

def random_localization(project, box_type, video_obj, post=False):
    x = random.uniform(0.0, 1.0)
    y = random.uniform(0.0, 1.0)
    w = random.uniform(0.0, 1.0 - x)
    h = random.uniform(0.0, 1.0 - y)
    attributes = {
        'test_bool': random.choice([False, True]),
        'test_int': random.randint(-1000, 1000),
        'test_float': random.uniform(-1000.0, 1000.0),
        'test_enum': random.choice(['a', 'b', 'c']),
        'test_string': str(uuid.uuid1()),
        'test_datetime': datetime.datetime.now().isoformat(),
        'test_geopos': [random.uniform(-180.0, 180.0), random.uniform(-90.0, 90.0)],
    }
    out = {
        'x': x,
        'y': y,
        'width': w,
        'height': h,
        'project': project,
        'type': box_type,
        'media_id': video_obj['id'],
        'frame': random.randint(0, video_obj['num_frames'] - 1),
    }
    if post:
        out = {**out, **attributes}
    else:
        out['attributes'] = attributes
    return out

def test_localization_crud(url, token, project, video_type, video, box_type):
    tator = pytator.Tator(url, token, project)
    video_obj = tator.Media.get(pk=video)

    # These fields will not be checked for object equivalence after patch.
    exclude = ['project', 'type', 'media_id', 'id', 'meta', 'user']

    # Test bulk create.
    num_localizations = random.randint(2000, 10000)
    boxes = [
        random_localization(project, box_type, video_obj, post=True)
        for _ in range(num_localizations)
    ]
    status, response = tator.Localization.new(boxes)
    print(f"New localization response: {response}")
    assert status == 201

    # Test single create.
    box = random_localization(project, box_type, video_obj, post=True)
    status, response = tator.Localization.new([box])
    box_id = response['id'][0]
    assert status == 201

    # Patch single box.
    patch = random_localization(project, box_type, video_obj)
    status, response = tator.Localization.update(box_id, patch)
    print(f"Patch localization response: {response}")
    assert status == 200

    # Get single box.
    updated_box = tator.Localization.get(box_id)
    assert_close_enough(patch, updated_box, exclude)
    
    # Delete single box.
    status = tator.Localization.delete(box_id)
    assert status == 200

    # ES can be slow at indexing so wait for a bit.
    time.sleep(5)

    # Bulk update box attributes.
    bulk_patch = random_localization(project, box_type, video_obj)
    bulk_patch = {'attributes': bulk_patch['attributes']}
    params = {'media_id': video, 'type': box_type}
    status, response = tator.Localization.bulk_update(params, bulk_patch)
    assert status == 200

    # Verify all boxes have been updated.
    boxes = tator.Localization.filter(params)
    dataframe = tator.Localization.dataframe(params)
    assert(len(boxes)==len(dataframe))
    for box in boxes:
        assert_close_enough(bulk_patch, box, exclude)
    
    # Delete all boxes.
    status = tator.Localization.bulk_delete(params)
    assert status == 200
    time.sleep(1)

    # Verify all boxes are gone.
    boxes = tator.Localization.filter(params)
    assert boxes == []
