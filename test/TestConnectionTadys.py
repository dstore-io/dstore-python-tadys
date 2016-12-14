#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pprint
import unittest
import BaseTestClass
import dstore.elastic.elasticservice_pb2 as elasticservice_pb2
import dstore.elastic.item.item_pb2 as item_pb2
import dstore.engine.engine_pb2 as engine_pb2
import dstore.engine.procedures.engineProc_pb2 as engineProc_pb2
import dstore.engine.procedures.mi_DatatypeTest_Ad_pb2 as mi_DatatypeTest_Ad_pb2
from dstore.helper.ValuesHelper import ValuesHelper


class CennectionTadys(BaseTestClass.BaseTestClass):

    def testProcedureConnection(self):
        stub = engineProc_pb2.EngineProcStub(self.getAuthorizedSecureChannel())
        got_valid_result = False
        for result in stub.mi_DatatypeTest_Ad(mi_DatatypeTest_Ad_pb2.Parameters()):
            got_valid_result = True
        self.assertTrue(got_valid_result)

    def testEngineConnection(self):
        stub = engine_pb2.EngineStub(self.getAuthorizedSecureChannel())
        value = ValuesHelper.buildValue('norwegian blue parrot')
        unique_id = stub.createUniqueID(value)
        self.assertEquals(unique_id.ByteSize(), 38)

    @unittest.skip('Currently not implemented.')
    def testElasticServiceConnection(self):
        stub = elasticservice_pb2.ElasticServiceStub(self.getAuthorizedSecureChannel())
        got_valid_result = False
        for result in stub.itemSuggest(item_pb2):
            pprint.pprint(result)
            got_valid_result = True
        self.assertTrue(got_valid_result)
