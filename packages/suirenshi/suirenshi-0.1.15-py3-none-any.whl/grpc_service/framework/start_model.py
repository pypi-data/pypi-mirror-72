#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
# 
# File: start_model.py
# Project: framework
# Created Date: Wednesday, June 10th 2020, 9:52:45 pm
# Author: liruifeng02
# -----
# Last Modified: Wed Jul 01 2020
# Modified By: liruifeng02
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------
"""
import argparse
import grpc
import numpy as np
import os
import sys
import time
from concurrent import futures

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from framework import inference
from utils import simple_logger, authentication, utils
from pb import service_pb2, service_pb2_grpc

logging = simple_logger.get_simple_logger()

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def parse():
    """
    parse params
    Returns:

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("base_path", help="the base path of the relative path", type=str)
    parser.add_argument("model_id", help="find the pipe to read and write", type=int)
    parser.add_argument("cfg_path", help="cfg file to parse parameters", type=str)
    parser.add_argument("port_use", help="which port to use", type=int)
    parser.add_argument("model_use", help="which model to use", type=str)
    parser.add_argument("model_path", help="where model python file", type=str)
    parser.add_argument("model_module", help="model python file name", type=str)
    parser.add_argument("auth_path", help="where auth python file", type=str)
    parser.add_argument("auth_module", help="auth python file name", type=str)
    parser.add_argument("decrypt_method", help="decrypt model method name", type=str)

    args = parser.parse_args()
    return args


def start_model(args):
    """
    Start model
    Args:
        args:

    Returns:

    """
    logging.debug(
        'Model ID is {}, Model Use is {}, Port is {}'.format(args.model_id, args.model_use,
                                                             args.port_use))
    if args.auth_path is not None and args.auth_module is not None and args.decrypt_method is not None and \
        args.auth_path != "None" and args.auth_module != "None" and args.decrypt_method != "None":
        sys.path.append(os.path.join(args.base_path, args.auth_path))
        auth_module = __import__(args.auth_module)
        authentication.decrypt_model = getattr(auth_module, args.decrypt_method)
    logging.debug("[start model] authentication decrypto model: {}".format(authentication.decrypt_model))

    sys.path.append(args.model_path)
    model_module = __import__(args.model_module)
    model_class = getattr(model_module, args.model_use)
    model = model_class(args.model_id, args.cfg_path, args.base_path)
    if model_class is None:
        raise Exception('Unknown Model type: {}'.format(args.model_use))
    model_parent_class = [item.__name__ for item in model_class.__bases__]
    logging.debug("model class parent class: {}".format(model_parent_class))
    if 'BaseModel' in model_parent_class or \
        ('PaddleModel' not in model_parent_class and 'MmdetModel' not in model_parent_class):
        raise Exception("Yourself model must extend PaddleModel or MmdetModel, " + 
                        "if you want use other model please contact us")
    
    options = [('grpc.max_send_message_length', 521310100),
               ('grpc.max_receive_message_length', 521310100)]
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=1), options=options)
    service_pb2_grpc.add_InferenceServicer_to_server(inference.ModelInference(model), grpc_server)
    grpc_server.add_insecure_port('127.0.0.1:{}'.format(args.port_use))
    grpc_server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS * 24)
    except KeyboardInterrupt:
        grpc_server.stop(0)


if __name__ == "__main__":
    """
    main
    """
    args = parse()
    start_model(args)
