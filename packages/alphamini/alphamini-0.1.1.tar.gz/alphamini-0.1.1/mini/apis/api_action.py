#!/usr/bin/env python3

import enum

from ..apis.base_api import BaseApi, DEFAULT_TIMEOUT
from ..apis.cmdid import PCProgramCmdId
from ..pb2.codemao_changerobotvolume_pb2 import ChangeRobotVolumeRequest, ChangeRobotVolumeResponse
from ..pb2.codemao_controlrobotrecord_pb2 import ControlRobotRecordRequest, ControlRobotRecordResponse
from ..pb2.codemao_getactionlist_pb2 import GetActionListRequest, GetActionListResponse
from ..pb2.codemao_moverobot_pb2 import MoveRobotRequest, MoveRobotResponse
from ..pb2.codemao_playaction_pb2 import PlayActionRequest, PlayActionResponse
from ..pb2.codemao_playcustomaction_pb2 import PlayCustomActionRequest, PlayCustomActionResponse
from ..pb2.codemao_stopaction_pb2 import StopActionRequest, StopActionResponse
from ..pb2.codemao_stopcustomaction_pb2 import StopCustomActionRequest, StopCustomActionResponse
from ..pb2.pccodemao_message_pb2 import Message


class PlayAction(BaseApi):
    """执行动作api

    机器人执行一个指定名称的本地(内置/自定义)动作
    动作名称可用GetActionList获取

    Args:
        is_serial (bool): 是否等待回复，默认True
        action_name (str): 动作名称，不能为none或空字符串

    #PlayActionResponse.isSuccess : 是否成功

    #PlayActionResponse.resultCode : 返回码

    """

    def __init__(self, is_serial: bool = True, action_name: str = None):
        """执行动作api初始化
        """
        assert action_name is not None and len(action_name), 'PlayAction actionName should be available'
        self.__isSerial = is_serial
        self.__actionName = action_name

    async def execute(self):
        """发送执行动作指令

        Returns:
            PlayActionResponse:

        """
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = PlayActionRequest()
        request.actionName = self.__actionName

        cmd_id = PCProgramCmdId.PLAY_ACTION_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        """解析回复指令

        Args:
            message (Message):待解析的Message对象

        Returns:
            PlayActionResponse:

        """
        if isinstance(message, Message):
            data = message.bodyData
            response = PlayActionResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class StopAllAction(BaseApi):
    """停止所有动作api

    停止所有正在执行的动作

    Args
        is_serial (bool): 是否等待回复，默认True

    """

    def __init__(self, is_serial: bool = True):
        self.__isSerial = is_serial

    async def execute(self):
        """
        发送停止所有动作指令

        Returns:
            StopActionResponse:

        """
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = StopActionRequest()

        cmd_id = PCProgramCmdId.STOP_ACTION_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            StopActionResponse:

        """
        if isinstance(message, Message):
            data = message.bodyData
            response = StopActionResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


@enum.unique
class MoveRobotDirection(enum.Enum):
    """机器人移动方向
    """
    FORWARD = 3  # 向前
    BACKWARD = 4  # 向后
    LEFTWARD = 1  # 向左
    RIGHTWARD = 2  # 向右


class MoveRobot(BaseApi):
    """控制机器人移动api

    控制机器人往某个方向(MoveRobotDirection)移动n步

    Args:
        is_serial (bool): 是否等待回复，默认True
        direction (MoveRobotDirection): 机器人移动方向，默认FORWARD，向前移动
        step (int): 步数，默认1步

    #MoveRobotResponse.isSuccess : 是否成功　

    #MoveRobotResponse.code : 返回码

    """

    def __init__(self, is_serial: bool = True, direction: MoveRobotDirection = MoveRobotDirection.FORWARD,
                 step: int = 1):
        assert direction is not None and isinstance(direction,
                                                    MoveRobotDirection) > 0, 'direction should not be None,and should be Positive'
        assert step is not None and step > 0, 'step should not be None,and should be Positive'
        self.__isSerial = is_serial
        self.__direction = direction.value
        self.__step = step

    async def execute(self):
        """发送机器人移动指令

        Returns:
            MoveRobotResponse:

        """
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = MoveRobotRequest()
        request.direction = self.__direction
        request.step = self.__step

        cmd_id = PCProgramCmdId.MOVE_ROBOT_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            MoveRobotResponse:

        """
        if isinstance(message, Message):
            data = message.bodyData
            response = MoveRobotResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


@enum.unique
class RobotActionType(enum.Enum):
    """
    机器人动作类型

    内置：机器人内置的不可修改的动作文件

    自定义: 放置在sdcard/customize/action目录下可被开发者修改的动作文件

    """
    INNER = 0  # 内置
    CUSTOM = 1  # 自定义


class GetActionList(BaseApi):
    """获取机器人动作列表api

    获取存储在机器人本地(内置/自定义)的动作文件列表

    Args:
        is_serial (bool): 是否等待回复，默认True
        action_type (RobotActionType): 动作类型，默认为INNER，内置动作

    #GetActionListResponse.actionList : 动作列表

    #GetActionListResponse.isSuccess : 是否成功

    #GetActionListResponse.resultCode : 返回码

    """

    def __init__(self, is_serial: bool = True, action_type: RobotActionType = RobotActionType.INNER):
        assert action_type is not None and isinstance(action_type,
                                                      RobotActionType), 'action_type should not be available'
        self.__isSerial = is_serial
        self.__actionType = action_type.value

    async def execute(self):
        """发送获取机器人动作列表指令

        Returns:
            GetActionListResponse:

        """
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = GetActionListRequest()
        request.actionType = self.__actionType

        cmd_id = PCProgramCmdId.GET_ACTION_LIST.value

        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            GetActionListResponse:

        """
        if isinstance(message, Message):
            data = message.bodyData
            response = GetActionListResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class PlayCustomAction(BaseApi):
    """执行自定义动作api

    执行一个指定名称的自定义机器人动作
    动作名称可用GetActionList获取

    Args:
        is_serial (bool): 是否等待回复，默认True
        action_name (str): 自定义动作名称，不可为空或者None
    """

    def __init__(self, is_serial: bool = True, action_name: str = None):

        assert action_name is not None and len(action_name) > 0, 'PlayCustomAction actionName should be available'
        self.__isSerial = is_serial
        self.__actionName = action_name

    async def execute(self):
        """发送执行自定义动作指令

        Returns:
            PlayCustomActionResponse:

        """
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = PlayCustomActionRequest()
        request.actionName = self.__actionName

        cmd_id = PCProgramCmdId.PLAY_CUSTOM_ACTION_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            PlayCustomActionResponse:

        """

        if isinstance(message, Message):
            data = message.bodyData
            response = PlayCustomActionResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class StopCustomAction(BaseApi):
    """停止自定义动作api

    停止指定的自定义动作

    Args:
        is_serial (bool): 是否等待回复，默认True
        action_name (str): 自定义动作名称，不可为空或None

    """

    def __init__(self, is_serial: bool = True, action_name: str = None):
        assert action_name is not None and len(action_name) > 0, 'StopCustomAction actionName should be available'
        self.__isSerial = is_serial
        self.__actionName = action_name

    async def execute(self):
        """执行停止自定义动作指令

        Returns:
            StopCustomActionResponse:

        """
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = StopCustomActionRequest()
        request.actionName = self.__actionName

        cmd_id = PCProgramCmdId.STOP_CUSTOM_ACTION_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            StopCustomActionResponse:

        """

        if isinstance(message, Message):
            data = message.bodyData
            response = StopCustomActionResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class ChangeRobotVolume(BaseApi):
    """设置机器人音量api

    调整机器人音量

    Args:
        is_serial (bool): 是否等待回复，默认True
        volume (float): 音量，范围[0.0,1.0]，默认0.0

    #ChangeRobotVolumeResponse.isSuccess : 是否成功

    #ChangeRobotVolumeResponse.resultCode : 返回码

    """

    def __init__(self, is_serial: bool = True, volume: float = 0.0):
        assert 0.0 <= volume <= 1.0, 'ChangeRobotVolume volume should be in range[0.0,1.0]'
        self.__isSerial = is_serial
        self.__volume = volume

    async def execute(self):
        """发送设置机器人音量指令

        Returns:
            ChangeRobotVolumeResponse:

        """
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = ChangeRobotVolumeRequest()
        request.volume = self.__volume

        cmd_id = PCProgramCmdId.CHANGE_ROBOT_VOLUME_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            ChangeRobotVolumeResponse:

        """
        if isinstance(message, Message):
            data = message.bodyData
            response = ChangeRobotVolumeResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


@enum.unique
class RobotAudioRecordControlType(enum.Enum):
    """
    机器人录音控制类型
    """
    START_RECORD = 0  # 开始录音
    STOP_RECORD = 1  # 停止录音
    START_PLAY = 2  # 开始播放
    STOP_PLAY = 3  # 停止播放
    PAUSE_PLAY = 4  # 暂停播放
    CONTINUE_PLAY = 5  # 继续播放
    RENAME_FILE = 6  # 重命名文件


class ControlRobotAudioRecord(BaseApi):
    """控制机器人录音/播放api

    Args:
        is_serial (bool): 是否等待回复，默认True
        control_type (RobotAudioRecordControlType): 控制类型，默认START_RECORD，开始录音
        time_limit (int): 录音时长，单位ms，默认0
        file_name (str): 录音文件存储名称
        new_file_name (str): 重命名录音文件的名称

    """

    def __init__(self, is_serial: bool = True,
                 control_type: RobotAudioRecordControlType = RobotAudioRecordControlType.START_RECORD,
                 time_limit: int = 0, file_name: str = None,
                 new_file_name: str = None):
        # assert ptype >= 0, 'RobotAudioRecord type should be positive'
        self.__isSerial = is_serial
        self.__control_type = control_type.value
        self.__timeLimit = time_limit
        self.__id = file_name
        self.__newId = new_file_name

    async def execute(self):
        """发送控制录音指令

        Returns:
            ControlRobotRecordResponse:

        """
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = ControlRobotRecordRequest()
        request.type = self.__control_type
        request.timeLimit = self.__timeLimit
        request.id = self.__id
        request.newId = self.__newId

        cmd_id = PCProgramCmdId.CONTROL_ROBOT_AUDIO_RECORD.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            ControlRobotRecordResponse:

        """
        if isinstance(message, Message):
            data = message.bodyData
            response = ControlRobotRecordResponse()
            response.ParseFromString(data)
            return response
        else:
            return None
