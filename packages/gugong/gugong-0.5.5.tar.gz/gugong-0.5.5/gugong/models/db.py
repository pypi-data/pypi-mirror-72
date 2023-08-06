#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# db.py
#

import os
import json
from peewee import *
from ..proto import gugong_pb2 as ggpb


#
# init the DB in memory
# since the data size is really small
# leave the room for future scalability with the PostgreSQL compatibility
#
db = SqliteDatabase(':memory:')


class ArchType(Model):
    id = AutoField()
    name = CharField()

    class Meta:
        database = db


class Place(Model):
    id = AutoField()
    name = CharField(index=True)
    arch_type = IntegerField()

    class Meta:
        database = db


class Empire(Model):
    id = AutoField()
    name = CharField()
    temple_name = CharField()
    epoch_name = CharField()
    dynasty = CharField()
    years_in_position = IntegerField()

    class Meta:
        database = db


def init_db():
    db.create_tables([Place, ArchType, Empire])

    results = Empire.select()
    if not results:
        _init_arch_type()
        _init_empire()
        _init_place()


def _map_arch_type(arch_type_string):
    return {
        'bridge': ggpb.QIAO,
        'qiao': ggpb.QIAO,
        '桥': ggpb.QIAO,
        'garden': ggpb.HUAYUAN,
        'huayuan': ggpb.HUAYUAN,
        '花园': ggpb.HUAYUAN,
        'gate': ggpb.MEN,
        'men': ggpb.MEN,
        '门': ggpb.MEN,
        'guan': ggpb.GUAN,
        '馆': ggpb.GUAN,
        'hall': ggpb.DIAN,
        'dian': ggpb.DIAN,
        '殿': ggpb.DIAN,
        'kiosk': ggpb.TING,
        'ting': ggpb.TING,
        '亭': ggpb.TING,
        'lou': ggpb.LOU,
        '楼': ggpb.LOU,
        'palace': ggpb.GONG,
        'gong': ggpb.GONG,
        '宫': ggpb.GONG,
        'pavilion': ggpb.GE,
        'ge': ggpb.GE,
        '阁': ggpb.GE,
        'tang': ggpb.TANG,
        '堂': ggpb.TANG,
        'xuan': ggpb.XUAN,
        '轩': ggpb.XUAN,
        'zhai': ggpb.ZHAI,
        '斋': ggpb.ZHAI
    }.get(arch_type_string, ggpb.UNDEFINED_ARCH_TYPE)


def _map_orientation(orientation_string):
    return {
        'north': ggpb.NORTH,
        'south': ggpb.SOUTH,
        'east': ggpb.EAST,
        'west': ggpb.WEST
    }.get(orientation_string, ggpb.UNDEFINED_ORIENTATION)


def _init_arch_type():

    cwd, _ = os.path.split(__file__)
    DATA_PATH = os.path.join(cwd, "..", "data", "gugong.json")

    data_parsed = None
    with open(DATA_PATH, "r") as fd:
        data = fd.read()
        data_parsed = json.loads(data)

    if data_parsed is None:
        raise Exception("Data Parsing Error!!")

    arch_types = data_parsed['architecture_types']
    for arch_type in arch_types:
        at = ArchType(name=arch_type['name'])
        at.save()


def _init_place():

    cwd, _ = os.path.split(__file__)
    DATA_PATH = os.path.join(cwd, "..", "data", "gugong.json")

    data_parsed = None
    with open(DATA_PATH, "r") as fd:
        data = fd.read()
        data_parsed = json.loads(data)

    if data_parsed is None:
        raise Exception("Data Parsing Error!!")

    places = data_parsed['places']
    for place in places:
        p = Place(name=place['name'],
                  arch_type=_map_arch_type(place['arch_type']))
        p.save()


def _init_empire():

    cwd, _ = os.path.split(__file__)
    DATA_PATH = os.path.join(cwd, "..", "data", "gugong.json")

    data_parsed = None
    with open(DATA_PATH, "r") as fd:
        data = fd.read()
        data_parsed = json.loads(data)

    if data_parsed is None:
        raise Exception("Data Parsing Error!!")

    empires = data_parsed['empires']
    for empire in empires:
        emp = Empire(name=empire['name'],
                     temple_name=empire['temple_name'],
                     epoch_name=empire['epoch_name'],
                     dynasty=empire['dynasty'],
                     years_in_position=empire['years_in_position'])

        emp.save()


def get_places():
    results = Place.select()
    places = []
    for place in results:
        p = ggpb.Place(name=place.name, arch_type=place.arch_type)
        places.append(p)

    return places


def get_empires():
    results = Empire.select()
    empires = []
    for empire in results:
        emp = ggpb.Empire(name=empire.name, dynasty=empire.dynasty,
                          epoch_name=empire.epoch_name, temple_name=empire.temple_name)
        empires.append(emp)

    return empires
