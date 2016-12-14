#!/usr/bin/env python
# -*- coding: utf-8 -*-
import BaseTestClass
from dstore.helper.ValuesHelper import ValuesHelper
import dstore.engine.engine_pb2 as engine_pb2


class CreateUniqueIDTadys(BaseTestClass.BaseTestClass):

    def testgetUniqueID(self):
        stub = engine_pb2.EngineStub(self.getAuthorizedSecureChannel())
        value = ValuesHelper.buildValue('norwegian blue parrot')
        unique_id = stub.createUniqueID(value)
        self.assertEquals(unique_id.ByteSize(), 38)