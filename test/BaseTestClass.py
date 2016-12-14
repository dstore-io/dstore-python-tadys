# -*- coding: utf-8 -*-
import unittest
import logging
import dstore.helper.misc
import configuration.constants as constants


class BaseTestClass(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(BaseTestClass, self).__init__(*args, **kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            filename=None,
                            filemode='w')

    def getUnauthorizedSecureChannel(self):
        return dstore.helper.misc.getChannel(constants.GRPC_SERVER,
                                             constants.GRPC_PORT,
                                             constants.GRPC_PEM_FILE)


    def getAuthorizedSecureChannel(self):
        return dstore.helper.misc.getChannel(constants.GRPC_SERVER,
                                             constants.GRPC_PORT,
                                             constants.GRPC_PEM_FILE,
                                             constants.GRPC_USERNAME,
                                             constants.GRPC_PASSWORD)
