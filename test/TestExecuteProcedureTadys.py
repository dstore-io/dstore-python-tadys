#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import sys
import grpc
import BaseTestClass
import dstore.engine.procedures.engineProc_pb2 as engineProc_pb2
import dstore.engine.procedures.mi_GetCountries_pb2 as mi_GetCountries_pb2
import dstore.engine.procedures.mi_DatatypeTest_Ad_pb2 as mi_DatatypeTest_Ad_pb2
import dstore.engine.procedures.mi_GetUnits_pb2 as mi_GetUnits_pb2
from dstore.helper.ValuesHelper import ValuesHelper
from dstore.helper.DstoreMetadata import DstoreMetadata

class CennectionTadys(BaseTestClass.BaseTestClass):

    def testPublicProcedureUnauthorizedShouldSucceed(self):
        stub = engineProc_pb2.EngineProcStub(self.getUnauthorizedSecureChannel())
        country_id = -1
        for result in stub.mi_GetCountries(mi_GetCountries_pb2.Parameters()):
            if len(result.row) == 0:
                continue
            for message in result.row:
                country_id = message.country_id.value
                break
            if country_id:
                break
        self.assertEquals(1, country_id)

    def testAdminProcedureUnauthorizedShouldFail(self):
        stub = engineProc_pb2.EngineProcStub(self.getUnauthorizedSecureChannel())
        try:
            for result in stub.mi_DatatypeTest_Ad(mi_DatatypeTest_Ad_pb2.Parameters()):
                got_valid_result = True
        except grpc.RpcError:
            got_valid_result = False
        self.assertFalse(got_valid_result)

    def testAdminProcedureAuthorizedShouldSucceed(self):
        stub = engineProc_pb2.EngineProcStub(self.getAuthorizedSecureChannel())
        test_char = ''
        for result in stub.mi_DatatypeTest_Ad(mi_DatatypeTest_Ad_pb2.Parameters()):
            if len(result.row) == 0:
                continue
            for message in result.row:
                test_char = message.test_char.value.strip()
        self.assertEquals('test char', test_char)

    def testExecuteProcedureWithoutParameters(self):
        stub = engineProc_pb2.EngineProcStub(self.getAuthorizedSecureChannel())
        test_char = ''
        for result in stub.mi_DatatypeTest_Ad(mi_DatatypeTest_Ad_pb2.Parameters()):
            if len(result.row) == 0:
                continue
            for message in result.row:
                 test_char = message.test_char.value.strip()
        self.assertEquals('test char', test_char)

    def testExecuteProcedureWithParameters(self):
        stub = engineProc_pb2.EngineProcStub(self.getAuthorizedSecureChannel())
        params = mi_DatatypeTest_Ad_pb2.Parameters()
        params.get_result_set.value = True
        test_char = ''
        for result in stub.mi_DatatypeTest_Ad(params):
            if len(result.row) == 0:
                continue
            for message in result.row:
                test_char = message.test_char.value.strip()
        self.assertEquals('test char', test_char)

    def testExecuteProcedureWithGetOutputParameters(self):
        stub = engineProc_pb2.EngineProcStub(self.getAuthorizedSecureChannel())
        params = mi_DatatypeTest_Ad_pb2.Parameters()
        params.get_result_set.value = False
        params.set_output_params.value = True
        test_char = ''
        for result in stub.mi_DatatypeTest_Ad(params):
            test_char = result.test_char.value.strip()
        self.assertEquals('test char', test_char)

    def testGetAndProcessResultSet(self):
        stub = engineProc_pb2.EngineProcStub(self.getAuthorizedSecureChannel())
        expected_dict = {'test_text': 'test text',
                         'test_bit': True,
                         'test_integer': 17,
                         'test_datetime': datetime.datetime(2006, 5, 23, 17, 42, 59, 333000),
                         'test_decimal': -17.425923}
        result_dict = {}
        for result in stub.mi_DatatypeTest_Ad(mi_DatatypeTest_Ad_pb2.Parameters()):
            if len(result.row) == 0:
                continue
            for message in result.row:
                result_dict['test_text'] = message.test_text.value.strip()
                result_dict['test_bit'] = message.test_bit.value
                result_dict['test_integer'] = message.test_integer.value
                result_dict['test_datetime'] = ValuesHelper.buildNativeDatetimeValue(message.test_datetime.value)
                result_dict['test_decimal'] = ValuesHelper.buildNativeDecimalValue(message.test_decimal.value)
        self.assertDictEqual(expected_dict, result_dict)

    def testGetAndProcessMessagesAfterProcedureError(self):
        stub = engineProc_pb2.EngineProcStub(self.getAuthorizedSecureChannel())
        params = mi_GetUnits_pb2.Parameters()
        params.active.value = 3
        message_list = []
        try:
            for result in stub.mi_GetUnits(params):
                for message in result.message:
                    message_list.append(message)
        except grpc.RpcError as e:
            return_status = DstoreMetadata.buildTrailingMetadata(e.trailing_metadata())[DstoreMetadata.ENGINE_RETURN_STATUS_KEY]

        # The Return Status should be "-500" (invalid parameter).
        self.assertEquals('-500', return_status)

        # There should be a print message.
        self.assertGreater(len(message_list), 0)

        # And it should be the cause of the expected error.
        self.assertEquals("mi_GetUnits : parameter \"@Active\" is invalid", message_list[0].message)
