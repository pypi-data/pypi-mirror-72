import pytest
import time

import os
from random import choice, randint, shuffle
from codenamize import codenamize
from datetime import datetime

from gutools.tools import flatten
from gutools.upytest import tempfolder, select_one

from brotation.brotation import *

# --------------------------------------------------
# logger
# --------------------------------------------------
from gutools.loggers import logger, \
    trace, exception, debug, info, warn, error
log = logger(__name__)


rot = dict()
for r, m, M in BackupRotator.RANGES:
    rot[r] = (m, M or 20)


@pytest.fixture
def random_level():
    return {r: randint(*args) for r, args in rot.items()}


@pytest.fixture
def dict_samples():
    result = dict()

    rkeys = list(rot.keys())
    # join = ['.', '-', '_']
    # ext = ['xz', '7z']
    join = ['-', ]
    ext = ['xz', ]
    for i in range(randint(1, 1)):
        name = codenamize(f"name-{i}", join=choice(join))
        n = randint(20, 40)
        s = result[name] = set()
        for _ in range(10**4):
            if len(s) >= n:
                break
            r = choice(rkeys)
            path = f"{name}.{choice(r)}{randint(*rot[r])}.{choice(ext)}"
            if extract_info(path):
                s.add(path)
            else:
                foo = 11
    return result


@pytest.fixture
def samples(dict_samples):
    result = list(flatten(dict_samples.values()))
    shuffle(result)
    return result


@pytest.fixture
def rotator(samples, tempfolder):
    for i, name in enumerate(samples):
        open(os.path.join(tempfolder, name), 'wt').write(f"file: {i}")

    return BackupRotator(tempfolder)


def test_rotation_info_maths(rotator):
    """*Check rotation info from paths.*  
    """
    # matching paterns
    data = {
        'flowmonitor.git.d6.7z': 'd6',
        'flowmonitor.git.w0.7z': 'w0',
        'flowmonitor.git.w11.7z': 'w11',
        'flowmonitor.git.w21.7z': 'w21',
        'flowmonitor.git.w41.7z': 'w41',
        'flowmonitor.git.w51.7z': 'w51',
        'flowmonitor.git.m11.7z': 'm11',
        'flowmonitor.git.m9.7z': 'm9',
        'flowmonitor.git.y17.xz': 'y17',

        # using 2 digits
        'womanly_speech.m01.xz': 'm1',
        'womanly_speech.m10.xz': 'm10',
    }
    for element, rot0 in data.items():
        d = rotator._parse(element)
        if d:
            rot = d['rot']
            value = d[rot]
            assert rot0 == f"{rot}{value}"
        else:
            raise RuntimeError(f"'{element}' don't match!")


def test_rotation_info_fails():
    """*Check rotation info when must fail.*  
    """

    # no matching paterns
    data = {
        'flowmonitor.git.y1.xz': 'year must have 2 digits',
        'flowmonitor.git.d7.7z': 'week day must belongs to [0-6]',
        'flowmonitor.git.m13.7z': 'month [1-12]',
        'flowmonitor.git.w60.7z': 'year week < 60',
        'flowmonitor.git.w54.7z': 'year week <= 53',
    }
    for path, fail in data.items():
        d = extract_info(path)
        if d:
            raise RuntimeError(f"{path} fails: {fail}, but returns {d}")


def test_rotator(rotator, random_level):
    """*Check shifting in iterate elements.*
    
    **TODO:** move to gutools library
    
    Iterate for the next item in Rotator until all changes 
    has made in the element by a single incremet in the *less significat*
    'digit'.
    
    """
    level = random_level
    max_changes = 0
    total_changes = len(rotator.ranges) - 1
    for _ in range(10**total_changes):
        if max_changes >= total_changes:
            break
        new_level = rotator.next_item(level)
        print(new_level)
        for i, (r, m, M) in enumerate(rotator.ranges):
            if level[r] == M:
                assert new_level[r] != level[r]
                max_changes = max(max_changes, i + 1)
            else:
                break
        level = new_level
    else:
        raise RuntimeError(f"Not all changes has been observed... review ranges definition")

    foo = 1


def _test_pushing_new_element(rotator, random_level):
    """*xxxxx.*
    
    **TODO:** move to gutools library
    
    xxxx
    
    """
    level = random_level
    elements = rotator.elements
    #key = choice(list(elements.keys()))

    keys, _ = select_one(elements)
    item = rotator.select_newest(keys[0])

    fqitem = rotator.fqitem(item, level)

    max_changes = 0
    total_changes = len(rotator.ranges)
    for _ in range(10**total_changes):
        if max_changes >= total_changes:
            break

        fqitem2 = rotator.next_item(fqitem)
        changes = rotator.rotations(fqitem2)
        if len(changes) > 1:
            foo = 1
        nchanges = 0
        for i, (r, m, M) in enumerate(rotator.ranges):
            if fqitem2[r] != fqitem[r]:
                nchanges += 1
        max_changes = max(max_changes, nchanges)
        # print(f"changes: {nchanges} - {fqitem2}")
        fqitem = fqitem2
    else:
        raise RuntimeError(f"Not all changes has been observed... review ranges definition")

    foo = 1


def test_full_rotation(rotator, samples, random_level):
    """*Simulate dialy rotation until a rotation moves to next year.*
    
    **TODO:** move to gutools library
    
    xxxx
    
    """
    level = random_level
    sample = choice(samples)

    item = rotator._parse(sample)
    fqitem = rotator.fqitem(item, **level)

    total_changes = len(rotator.ranges)
    full_cycles = 3
    tf = time.time() + 30  # timeout
    while time.time() < tf:
        # simulate one day step
        fqitem2 = rotator.next_item(fqitem)
        debug(f"{fqitem} --> {fqitem2}")

        #  get the changes BEFORE apply them
        changes = rotator.rotations(fqitem)
        #  check number of changes
        if len(changes) > 0:
            info(f"- {len(changes)} copy expected------------")
            for t in (changes):
                # t = rotator._rebuild(t)
                info(f"copy into: {t}")
            foo = 1

        # count number of changes in ranges for a single step
        if len(changes) >= total_changes:
            full_cycles -= 1
            if full_cycles <= 0:
                break

        # next iteration
        fqitem = fqitem2

    else:
        raise RuntimeError(f"Not all changes has been observed... review ranges definition")

    foo = 1


def test_apply_rotation(rotator, samples, random_level):
    """*Simulate dialy rotation until a rotation moves to next year.*
    
    **TODO:** move to gutools library
    
    xxxx
    
    """
    level = random_level
    sample = choice(samples)

    item = rotator._parse(sample)
    fqitem = rotator.fqitem(item, **level)

    total_changes = len(rotator.ranges)
    full_cycles = 3
    tf = time.time() + 30  # timeout

    # simulate one day step
    fqitem2 = rotator.next_item(fqitem)

    #  get the changes BEFORE apply them
    changes = rotator.rotations(fqitem)
    rotator.apply(changes)

    foo = 1
