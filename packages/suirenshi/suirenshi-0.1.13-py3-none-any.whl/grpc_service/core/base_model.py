#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
"""
# This module provide
# Authors: suye(suye02@baidu.com)
# Date: 2020/6/11 3:05 下午
"""
import os
import json
import time
import numpy as np
import mmcv
from abc import abstractmethod
from collections import namedtuple
from paddle.fluid.core import AnalysisConfig
from paddle.fluid.core import create_paddle_predictor
from mmdet.apis import init_detector, inference_detector
from mmdet.models import build_detector
from mmdet.core import get_classes

from utils import simple_logger
from utils.utils import config_parser
from utils import authentication
import pickle

logging = simple_logger.get_simple_logger()


class BaseModel(object):
    """
    模型预测服务
    解析模型对应的配置文件
    包含了模型初始化、及启动物体检测
    """

    def __init__(self, model_id, cfg_path, base_path, delete_model_file):
        """
        Args:
            model_id: 模型ID
            cfg_path: 模型config路径
        """
        # 基本meta信息
        self.model_id = model_id
        self.cfg_path = cfg_path
        self.base_path = base_path
        # 加载配置文件
        self.cfg_dic = config_parser(self.cfg_path)
        self.model_name = 'model_{}'.format(str(model_id))
        self.model_cfg = self.cfg_dic[self.model_name]
        self.model_path = os.path.join(base_path, self.model_cfg['model_path'])
        self.config_path = os.path.join(base_path, self.model_cfg['config_path'])
        self.class_mapper = json.loads(self.model_cfg['class_mapper'])
        self.thresh_values = [float(x) for x in self.model_cfg['thresh_values'].split(',')]
        self.num_classes = int(self.model_cfg['num_classes'])
        self.result = None
        # runtime 初始化
        self.error_code = 0
        self.image_np = None
        # 启动模型
        self.model = None
        self._env_check()
        self._start_model()
        if delete_model_file:
            self.delete_model_file()

    def _start_model(self):
        """
        启动模型（抽象方法，必须改写）
        """
        raise Exception('This method must be defined by user')

    @abstractmethod
    def _env_check(self):
        """
        启动模型前检查环境中是否有正在占用gpu的程序或已启动的预测服务等，避免重复启动模型等误操作
        """

    def _inference(self):
        """
        需要用户实现的inference方法，结果需要写入类属性self.result
        self.result为namedtuple('Result', ['masks', 'bboxes', 'labels'])格式
        """
        raise Exception('This method must be defined by user')

    def inference(self, request):
        """
        传入图片numpy（此处删除了不必要字段model id，offset等，这些都可以抽到cfg中）
        调用_inference接口进行预测，结果写入类属性self.result
        Args:
            image_np: 图片numpy数组

        Returns:
        """
        self.request = request
        self.image_np = np.asarray(bytearray(request.encoded_image), dtype="uint8")
        self._preprocess()
        Result = namedtuple('Result', ['masks', 'bboxes', 'labels'])
        self.result = Result(masks=[], bboxes=[], labels=[])
        inference_start = time.time()
        self._inference()
        logging.debug('Inference Time: {:.3f}'.format(time.time() - inference_start))
        post_start = time.time()
        self._postprocess()
        logging.debug('Post Time: {:.3f}'.format(time.time() - post_start))

    def delete_model_file(self):
        """
        加载模型之后删除模型文件，默认删除self.model_path与self.config_path对应的文件
        如有其他模型文件请重写该方法删除相应模型文件
        """
        temp_path = os.path.join(os.path.dirname(self.model_path), 'temp')
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
        
        temp_file = open(os.path.join(temp_path, str(os.getpid())), 'w')
        temp_file.close()

    @abstractmethod
    def results_parser(self):
        """
        根据框架类型(paddle or mmdet)编写结果处理代码，统一存入 namedtuple('Result', ['masks', 'bboxes', 'labels'])
        """

    def _preprocess(self):
        """
        前处理
        Returns:

        """
        pass

    def _postprocess(self):
        """
        后处理
        Returns:
        """
        pass


class PaddleModel(BaseModel):
    """
    paddlepaddle base model
    """

    def __init__(self, model_id, cfg_path, base_path, delete_model_file):
        """初始化"""
        super().__init__(model_id, cfg_path, base_path, delete_model_file)
    
    def _start_model(self):
        """
        load model
        """
        if authentication.decrypt_model is None:
            model_config = AnalysisConfig(self.model_path, self.config_path)
        else:
            model_data = authentication.decrypt_model(self.model_path)
            param_data = authentication.decrypt_model(self.config_path)
            model_config = AnalysisConfig('', '')
            # 从内存中加载参数到config
            model_config.set_model_buffer(model_data, len(model_data), param_data, len(param_data))

            model_data.close()
            param_data.close()
        
        self.model = create_paddle_predictor(model_config)


class MmdetModel(BaseModel):
    """
    mmdetection base model
    """
    
    def __init__(self, model_id, cfg_path, base_path, delete_model_file):
        """初始化"""
        super().__init__(model_id, cfg_path, base_path, delete_model_file)
    
    def _start_model(self):
        """
        load model
        """
        if authentication.decrypt_model is None:
            self.model = init_detector(self.config_path, self.model_path, device='cuda:0')
        else:
            self.model = load_model()

    def load_model(self):
        """
        修改mmdetection的init_detector方法
        """
        if isinstance(self.config_path, str):
            config = mmcv.Config.fromfile(config)
        elif not isinstance(config, mmcv.Config):
            raise TypeError('config must be a filename or Config object, '
                            'but got {}'.format(type(config)))
        config.model.pretrained = None
        model = build_detector(config.model, test_cfg=config.test_cfg)
        if self.model_path is not None:
            checkpoint = load_checkpoint(model)
            if 'CLASSES' in checkpoint['meta']:
                model.CLASSES = checkpoint['meta']['CLASSES']
            else:
                logging.warn('Class names are not saved in the checkpoint\'s '
                            'meta data, use COCO classes by default.')
                model.CLASSES = get_classes('coco')
        model.cfg = config  # save the config in the model for convenience
        model.to('cuda:0')
        model.eval()
        return model

    def load_checkpoint(self, model):
        """
        修改mmdetection load_checkpoint方法
        """
        checkpoint_data = authentication.decrypt_model(self.model_path)
        checkpoint = pickle.load(checkpoint_data)
        # OrderedDict is a subclass of dict
        if not isinstance(checkpoint, dict):
            raise RuntimeError(f'No state_dict found in checkpoint file {self.model_path}')
        # get state_dict from checkpoint
        if 'state_dict' in checkpoint:
            state_dict = checkpoint['state_dict']
        else:
            state_dict = checkpoint
        # strip prefix of state_dict
        if list(state_dict.keys())[0].startswith('module.'):
            state_dict = {k[7:]: v for k, v in checkpoint['state_dict'].items()}
        # load state_dict
        mmcv.load_state_dict(model, state_dict, False, None)
        return checkpoint
