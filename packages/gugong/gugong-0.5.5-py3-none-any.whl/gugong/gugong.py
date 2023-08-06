#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# gugong
#

import time
import random
import pypinyin
from .proto import gugong_pb2 as ggpb
from .models.db import init_db, get_places, get_empires

class GuGong(object):

    # name of the object
    name = "故宫"

    # open-schema profile
    profile = {}

    # a list of places in Gugong
    places = []

    # a list of empires that lived at GuGong
    empires = []

    def __init__(self):
        super().__init__();

        if not self.profile and not self.places:
            self.load_data()
    
    # load the data into the main object
    def load_data(self):
        init_db()

        self.places = get_places()
        self.empires = get_empires()

    def _get_arch_type(self, arch_type):
        rets = []
        for place in self.places:
            if place.arch_type == arch_type:
                rets.append(place)
        return rets

    def get_gates(self):
        """
        get a list of gate as response
        """
        return self._get_arch_type(ggpb.MEN)

    def get_palaces(self):
        """
        get a list of palace as response
        """
        return self._get_arch_type(ggpb.GONG)

    def get_kiosks(self):
        """
        get a list of kiosk as response
        """
        return self._get_arch_type(ggpb.TING)

    def get_faq_answer(self, question):
        return {
            '你是谁？': '我是你的故宫小帮手。',
            '故宫什么时候成立的': '故宫是xxxx成立的。',
            '故宫有多大': '故宫长961多米，宽753多米。',
            '故宫里有御猫吗': '你去找找看？',
            '城门': '紫禁城有四座城门，南面为午门，北面为神武门，东面为东华门，西面为西华门。',
            '外朝': '外朝的中心为太和殿、中和殿、保和殿，统称三大殿',
            '内廷': '乾清宫、交泰殿、坤宁宫，统称后三宫',
            '故宫的入口在哪里？': '故宫目前只能从东华门进入。',
            '故宫里有餐厅么？': '故宫里有简餐，冰窖提供简餐。'
        }.get(question, '对不起，你的问题太难了。我暂时还帮不了你:(')

    # just kidding QA system here for fun.
    def ask(self, question):
        question = question.replace('?', '')
        print("你是想知道" + question + "吗？让我想一想", end='', flush=True)

        # AI假装在思考
        for i in range(random.randint(1, 3)):
            print('.', end='', flush=True)
            time.sleep(random.random())

        print('.', flush=True)

        return self.get_faq_answer(question)

    def du(self, query):
        return pypinyin.pinyin(query)
