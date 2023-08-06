#!/usr/bin/env python3

import enum

from ..apis.base_api import BaseApi, DEFAULT_TIMEOUT
from ..apis.cmdid import PCProgramCmdId
from ..pb2.codemao_controlbehavior_pb2 import ControlBehaviorRequest, ControlBehaviorResponse
from ..pb2.codemao_controlmouthlamp_pb2 import ControlMouthRequest, ControlMouthResponse
from ..pb2.codemao_playexpression_pb2 import PlayExpressionRequest, PlayExpressionResponse
from ..pb2.codemao_setmouthlamp_pb2 import SetMouthLampRequest, SetMouthLampResponse
from ..pb2.pccodemao_message_pb2 import Message


@enum.unique
class RobotExpressionType(enum.Enum):
    """
    机器人表情类型

    内置/自定义
    """
    INNER = 0  # 内置表情
    CUSTOM = 1  # 自定义表情


class PlayExpression(BaseApi):
    """播放表情api

    Args:
        is_serial (bool): 是否等待回复，默认True
        express_name (str): 表情名称，不可为空或者None
        express_type (RobotExpressionType):表情类型，默认INNER,内置表情

    """

    def __init__(self, is_serial: bool = True, express_name: str = None,
                 express_type: RobotExpressionType = RobotExpressionType.INNER):
        assert express_name is not None and len(express_name), 'PlayExpression expressName should be available'
        self.__isSerial = is_serial
        self.__expressName = express_name
        self.__dirType = express_type.value

    async def execute(self):
        """
        执行播放表情指令

        Returns:
            PlayExpressionResponse:

        """
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = PlayExpressionRequest()
        request.expressName = self.__expressName
        request.dirType = self.__dirType

        cmd_id: int = PCProgramCmdId.PLAY_EXPRESSION_REQUEST.value

        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            PlayExpressionResponse:

        """
        if isinstance(message, Message):
            data = message.bodyData
            response = PlayExpressionResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


@enum.unique
class RobotBehaviorControlType(enum.Enum):
    """
    表现力控制类型

    开始/停止
    """
    START = 1  # 开始
    STOP = 0  # 停止


class ControlBehavior(BaseApi):
    """控制表现力api

    开始/停止表现力

    Args:
        is_serial (bool): 是否等待回复，默认True
        name (str): 表现力名称，不可为空或None
        control_type (RobotBehaviorControlType): 控制类型，默认START，表示开始执行
    """

    def __init__(self, is_serial: bool = True, name: str = None,
                 control_type: RobotBehaviorControlType = RobotBehaviorControlType.START):
        assert name is not None and len(name), 'ControlBehavior name should be available'
        self.__isSerial = is_serial
        self.__name = name
        self.__eventType = control_type.value

    async def execute(self):
        """
        执行表现力控制指令

        Returns:
            ControlBehaviorResponse:

        """
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = ControlBehaviorRequest()
        request.name = self.__name
        request.eventType = self.__eventType

        cmd_id = PCProgramCmdId.CONTROL_BEHAVIOR_REQUEST.value

        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            ControlBehaviorResponse:

        """
        if isinstance(message, Message):
            data = message.bodyData
            response = ControlBehaviorResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


@enum.unique
class MouthLampColor(enum.Enum):
    """
    嘴巴灯颜色

    红色/绿色/蓝色
    """
    RED = 1  # 红色
    GREEN = 2  # 绿色
    BLUE = 3  # 蓝色


@enum.unique
class MouthLampMode(enum.Enum):
    """
    嘴巴灯模式

    普通(常亮)/呼吸
    """
    NORMAL = 0  # 普通模式
    BREATH = 1  # 呼吸模式


class SetMouthLamp(BaseApi):
    """设置嘴巴灯api

    设置嘴巴灯的模式、颜色等参数

    当mode=NORMAL时，duration参数起作用，表示常亮多久时间

    当mode=BREATH，breath_duration参数起作用，表示多久呼吸一次

    Args:
        is_serial (bool): 是否等待回复，默认True
        mode (MouthLampMode): 嘴巴灯模式，默认NORMAL，普通(常亮)模式
        color (MouthLampColor): 嘴巴灯颜色，默认RED，红色
        duration (int): 持续时间，单位为毫秒，-1表示无限时间
        breath_duration (int):闪烁一次时长，单位为毫秒
    """

    def __init__(self, is_serial: bool = True, mode: MouthLampMode = MouthLampMode.NORMAL,
                 color: MouthLampColor = MouthLampColor.RED, duration: int = 0, breath_duration: int = 0):
        self.serial = is_serial
        self.__isSerial = self.serial
        self.__mode = mode.value
        self.__color = color.value
        self.__duration = duration
        self.__breathDuration = breath_duration

    async def execute(self):
        """
        执行设置设置嘴巴灯指令

        Returns:
            SetMouthLampResponse:

        """
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = SetMouthLampRequest()
        request.model = self.__mode
        request.color = self.__color
        request.duration = self.__duration
        request.breathDuration = self.__breathDuration

        cmd_id = PCProgramCmdId.SET_MOUTH_LAMP_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            SetMouthLampResponse:

        """
        if isinstance(message, Message):
            data = message.bodyData
            response = SetMouthLampResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class ControlMouthLamp(BaseApi):
    """控制嘴巴灯开关api

    打开/关闭嘴巴灯
    Args:
        is_serial (bool): 是否等待回复，默认True
        is_open (bool): 是否开启嘴巴灯 默认true，开启嘴巴灯
    """

    def __init__(self, is_serial: bool = True, is_open: bool = True):

        self.__isSerial = is_serial
        self.__isOpen = is_open

    async def execute(self):
        """
        执行控制嘴巴灯指令

        Returns:
            ControlMouthResponse:

        """
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = ControlMouthRequest()
        request.isOpen = self.__isOpen

        cmd_id = PCProgramCmdId.SWITCH_MOUTH_LAMP_REQUEST.value

        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            ControlMouthResponse:

        """
        if isinstance(message, Message):
            data = message.bodyData
            response = ControlMouthResponse()
            response.ParseFromString(data)
            return response
        else:
            return None
