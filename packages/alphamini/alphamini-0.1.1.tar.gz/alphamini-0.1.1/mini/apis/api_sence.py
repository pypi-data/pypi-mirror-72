#!/usr/bin/env python3

import enum

from ..apis.base_api import BaseApi, DEFAULT_TIMEOUT
from ..apis.cmdid import PCProgramCmdId
from ..pb2.codemao_faceanalyze_pb2 import FaceAnalyzeRequest, FaceAnalyzeResponse
from ..pb2.codemao_facedetect_pb2 import FaceDetectRequest, FaceDetectResponse
from ..pb2.codemao_facerecognise_pb2 import FaceRecogniseRequest, FaceRecogniseResponse
from ..pb2.codemao_getinfrareddistance_pb2 import GetInfraredDistanceRequest, GetInfraredDistanceResponse
from ..pb2.codemao_getregisterfaces_pb2 import GetRegisterFacesRequest, GetRegisterFacesResponse
from ..pb2.codemao_recogniseobject_pb2 import RecogniseObjectRequest, RecogniseObjectResponse
from ..pb2.codemao_takepicture_pb2 import TakePictureRequest, TakePictureResponse
from ..pb2.pccodemao_message_pb2 import Message


class FaceDetect(BaseApi):
    """检测人脸个数api

    Args:
        is_serial (bool): 是否等待回复，默认True
        timeout (int): 超时时间，必须大于0

    """

    def __init__(self, is_serial: bool = True, timeout: int = 0):
        assert timeout > 0, 'FaceDetect timeout should be positive'
        self.__isSerial = is_serial
        self.__timeout = timeout

    async def execute(self):
        """
        执行检测人脸个数指令

        Returns:
            FaceDetectResponse:

        """
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = FaceDetectRequest()
        request.timeout = self.__timeout

        cmd_id = PCProgramCmdId.FACE_DETECT_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            FaceDetectResponse:

        """
        if isinstance(message, Message):
            data = message.bodyData
            response = FaceDetectResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class FaceAnalysis(BaseApi):
    """性别分析api

    通过人脸识别，分析性别

    当多人存在摄像头前时，返回脸面积最大的那个

    Args:
        is_serial (bool): 是否等待回复，默认True
        timeout (int): 超时时间

    返回示例:FaceAnalyzeResponse{"age":24,"gender":99,"height":238,"width":238}

    age:年龄
    gender：[1,100],小于50为女性，大于50为男性
    height：人脸在摄像头画面中的高度
    width：人脸在摄像头画面中的宽度

    """

    def __init__(self, is_serial: bool = True, timeout: int = 0):
        assert timeout > 0, 'FaceAnalysis timeout should be positive'
        self.__isSerial = is_serial
        self.__timeout = timeout

    async def execute(self):
        """
        执行人脸性别分析指令

        Returns:
            FaceAnalyzeResponse:

        """
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = FaceAnalyzeRequest()
        request.timeout = self.__timeout

        cmd_id = PCProgramCmdId.FACE_ANALYSIS_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            FaceAnalyzeResponse:

        """
        if isinstance(message, Message):
            data = message.bodyData
            response = FaceAnalyzeResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


@enum.unique
class ObjectRecogniseType(enum.Enum):
    """
    物体识别类型

    水果/手势/花
    """
    FRUIT = 1  # 水果
    GESTURE = 2  # 手势
    FLOWER = 3  # 花


class ObjectRecognise(BaseApi):
    """物体识别api

    机器人通过摄像头识别相应的物体(水果/手势/花)

    Args:
        is_serial (bool): 是否等待回复，默认True
        object_type (ObjectRecogniseType): 物体识别类型，默认FRUIT，水果
        timeout (int): 超时时间
    """

    def __init__(self, is_serial: bool = True, object_type: ObjectRecogniseType = ObjectRecogniseType.FRUIT,
                 timeout: int = 10):
        assert timeout > 0, 'ObjectRecognise timeout should be positive'
        assert object_type is not None and object_type.value > 0, 'objectType should not be None,and should be positive'
        self.__isSerial = is_serial
        self.__objectType = object_type.value
        self.__timeout = timeout

    async def execute(self):
        """
        执行物体识别指令

        Returns:
            RecogniseObjectResponse:

        """
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = RecogniseObjectRequest()
        request.objectType = self.__objectType
        request.timeout = self.__timeout

        cmd_id = PCProgramCmdId.RECOGNISE_OBJECT_REQUEST.value

        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            RecogniseObjectResponse:

        """
        if isinstance(message, Message):
            data = message.bodyData
            response = RecogniseObjectResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class FaceRecognise(BaseApi):
    """人脸识别api

    机器人通过摄像头识别出所有的人脸信息

    Args:
        is_serial (bool): 是否等待回复，默认True
        timeout (int): 超时时间
    """

    def __init__(self, is_serial: bool = True, timeout: int = 10):
        assert timeout > 0, 'ObjectRecognise timeout should be positive'
        self.__isSerial = is_serial
        self.__timeout = timeout

    async def execute(self):
        """
        执行人脸识别指令

        Returns:
            FaceRecogniseResponse:

        """
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = FaceRecogniseRequest()
        request.timeout = self.__timeout

        cmd_id = PCProgramCmdId.FACE_RECOGNISE_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            FaceRecogniseResponse:

        """
        if isinstance(message, Message):
            data = message.bodyData
            response = FaceRecogniseResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


@enum.unique
class TakePictureType(enum.Enum):
    """
    拍照类型

    立即拍照/寻找人脸拍照
    """
    IMMEDIATELY = 0  # 立即拍照
    FINDFACE = 1  # 寻找人脸拍照


class TakePicture(BaseApi):
    """拍照api

    控制机器人拍照

    Args:
        is_serial (bool): 是否等待回复，默认True
        take_picture_type (TakePictureType): 拍照类型，默认IMMEDIATELY，立即拍照
    """

    def __init__(self, is_serial: bool = True, take_picture_type: TakePictureType = TakePictureType.IMMEDIATELY):
        self.__isSerial = is_serial
        self.__type = take_picture_type.value

    async def execute(self):
        """
        执行拍照指令

        Returns:
            TakePictureResponse:

        """
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = TakePictureRequest()
        request.type = self.__type

        cmd_id = PCProgramCmdId.TAKE_PICTURE_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            TakePictureResponse:

        """
        if isinstance(message, Message):
            data = message.bodyData
            response = TakePictureResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class GetInfraredDistance(BaseApi):
    """获取红外距离api

    获取距离机器人正面最近的障碍物的红外距离

    Args:
        is_serial (bool): 是否等待回复，默认True

    """

    def __init__(self, is_serial: bool = True):
        self.__isSerial = is_serial

    async def execute(self):
        """
        执行获取红外距离的指令

        Returns:
            GetInfraredDistanceResponse:

        """
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = GetInfraredDistanceRequest()

        cmd_id = PCProgramCmdId.GET_INFRARED_DISTANCE_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            GetInfraredDistanceResponse:

        """
        if isinstance(message, Message):
            data = message.bodyData
            response = GetInfraredDistanceResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class GetRegisterFaces(BaseApi):
    """获取已注册的人脸列表api

    获取机器人中已注册的人脸列表数据

    Args:
        is_serial (bool): 是否等待回复，默认True

    """

    def __init__(self, is_serial: bool = True):
        self.__isSerial = is_serial

    async def execute(self):
        """
        执行获取已注册人脸列表指令

        Returns:
            GetRegisterFacesResponse:

        """
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = GetRegisterFacesRequest()

        cmd_id = PCProgramCmdId.GET_REGISTER_FACES_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            GetRegisterFacesResponse:

        """
        if isinstance(message, Message):
            data = message.bodyData
            response = GetRegisterFacesResponse()
            response.ParseFromString(data)
            return response
        else:
            return None
