#!/usr/bin/env python
# -*- coding: utf-8 -*-
import BaseTestClass
from dstore.helper.ValuesHelper import ValuesHelper
import dstore.engine.engine_service_pb2 as engine_service_pb2


class CreateUniqueIDTadys(BaseTestClass.BaseTestClass):

    def testGetUniqueID(self):
        stub = engine_service_pb2.EngineStub(self.getAuthorizedSecureChannel())
        value = ValuesHelper.buildValue('norwegian blue parrot')
        unique_id = stub.CreateUniqueID(value)
        self.assertEquals(unique_id.ByteSize(), 38)