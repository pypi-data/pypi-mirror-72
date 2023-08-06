#!/usr/bin/env python3

import enum

from ..apis.base_api import BaseApi, DEFAULT_TIMEOUT
from ..apis.cmdid import PCProgramCmdId
from ..pb2 import cloudstorageurls_pb2
from ..pb2.cloudtranslate_pb2 import Platform
from ..pb2.codemao_controltts_pb2 import ControlTTSRequest, ControlTTSResponse
from ..pb2.codemao_getaudiolist_pb2 import GetAudioListRequest, GetAudioListResponse
from ..pb2.codemao_playaudio_pb2 import PlayAudioRequest, PlayAudioResponse
from ..pb2.codemao_playonlinemusic_pb2 import MusicRequest, MusicResponse
from ..pb2.codemao_stopaudio_pb2 import StopAudioRequest, StopAudioResponse
from ..pb2.pccodemao_message_pb2 import Message


@enum.unique
class TTSControlType(enum.Enum):
    """
    TTS控制类型

    播放/停止
    """
    START = 1  # 播放
    STOP = 0  # 停止


class PlayTTS(BaseApi):
    """播放/停止TTS api

    机器人播放合成的TTS语音

    control_type为STOP时，表示停止所有正在播放的TTS

    Args:
        is_serial (bool): 是否等待回复，默认True
        text (str): 播放的文本，不能为空或者None
        control_type (TTSControlType): 控制类型，默认START，开始播放
    """

    def __init__(self, is_serial: bool = True, text: str = None, control_type: TTSControlType = TTSControlType.START):
        assert text is not None and len(text), 'tts text should be available'
        self.__isSerial = is_serial
        self.__text = text
        self.__type = control_type.value

    async def execute(self):
        """
        执行控制TTS指令

        Returns:
            ControlTTSResponse:

        """
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = ControlTTSRequest()
        request.text = self.__text
        request.type = self.__type

        cmd_id = PCProgramCmdId.PLAY_TTS_REQUEST.value

        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            ControlTTSResponse:

        """
        if isinstance(message, Message):
            data = message.bodyData
            response = ControlTTSResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


@enum.unique
class AudioStorageType(enum.Enum):
    """
    音频存储类型

    阿里私有云/公网/机器人本地内置/机器人本地自定义

    """
    ALIYUN_PRIVATE = 1  # 阿里私有云
    NET_PUBLIC = 2  # 公网
    PRESET_LOCAL = 3  # 本地内置
    CUSTOMIZE_LOCAL = 4  # 本地自定义


class PlayAudio(BaseApi):
    """播放音频api

    机器人播放指定的音频

    Args:
        is_serial (bool): 是否等待回复，默认True
        url (str): 音频地址，当storage_type为ALIYUN_PRIVATE/NET_PUBLIC，url为音频文件网址；当storage_type为PRESET_LOCAL/CUSTOMIZE_LOCAL时，url为本地音频名称（本地音频名称可通过FetchAudioList接口获取）
        storage_type (AudioStorageType): 音频存储类型，默认ALIYUN_PRIVATE，阿里私有云
        volume (float): 音量大小，范围[0.0,1.0]，默认1.0

    """

    def __init__(self, is_serial: bool = True, url: str = None,
                 storage_type: AudioStorageType = AudioStorageType.ALIYUN_PRIVATE, volume: float = 1.0):

        assert url is not None and len(url), 'PlayAudio url should be available'
        assert 0 <= volume <= 1.0, 'PlayAudio volume should be in range[0,1]'
        self.__isSerial = is_serial
        self.__url = url
        self.__volume = volume
        self.__cloudStorageType = storage_type.value

    async def execute(self):
        """
        执行播放音频指令

        Returns:
            PlayAudioResponse:

        """
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        cloud = cloudstorageurls_pb2.CloudStorage()
        cloud.type = self.__cloudStorageType
        cloud.url.extend([self.__url])

        request = PlayAudioRequest()

        request.cloud.CopyFrom(cloud)
        request.volume = self.__volume

        cmd_id = PCProgramCmdId.PLAY_AUDIO_REQUEST.value

        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            PlayAudioResponse:

        """
        if isinstance(message, Message):
            data = message.bodyData
            response = PlayAudioResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class StopAllAudio(BaseApi):
    """停止所有音频api

    机器人停止所有正在播放的音频

    Args:
        is_serial (bool): 是否等待回复，默认True

    """

    def __init__(self, is_serial: bool = True):
        self.__isSerial = is_serial

    async def execute(self):
        """
        执行停止所有音频指令

        Returns:
            StopAudioResponse:

        """
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = StopAudioRequest()

        cmd_id = PCProgramCmdId.STOP_AUDIO_REQUEST.value

        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            StopAudioResponse:

        """
        if isinstance(message, Message):
            data = message.bodyData
            response = StopAudioResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


@enum.unique
class AudioSearchType(enum.Enum):
    """
    音频查询类型

    内置/自定义
    """
    INNER = 0  # 内置
    CUSTOM = 1  # 自定义


class FetchAudioList(BaseApi):
    """获取机器人的音频列表api

    获取存储在机器人rom或者sdcard中的音频列表

    Args:
        is_serial (bool): 是否等待回复，默认True
        search_type (AudioSearchType): 查询类型，默认INNER，即机器人内置;CUSTOM表示自定义，存放在sdcard中
    """

    def __init__(self, is_serial: bool = True, search_type: AudioSearchType = AudioSearchType.INNER):
        self.__isSerial = is_serial
        self.__searchType = search_type.value

    async def execute(self):
        """
        执行获取音频列表指令

        Returns:
            GetAudioListResponse:

        """
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = GetAudioListRequest()

        request.searchType = self.__searchType

        cmd_id = PCProgramCmdId.GET_AUDIO_LIST_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            GetAudioListResponse:

        """
        if isinstance(message, Message):
            data = message.bodyData
            response = GetAudioListResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class PlayOnlineMusic(BaseApi):
    """播放在线歌曲api

    机器人播放QQ音乐在线歌曲，需在app绑定机器人并授权

    Args:
        is_serial (bool): 是否等待回复，默认True
        name (str): 歌曲名称，不能为空或者None

    """

    def __init__(self, is_serial: bool = True, name: str = None):
        assert name is not None and len(name), 'PlayOnlineMusic name should be available'
        self.__isSerial = is_serial
        self.__name = name
        self.__platform = Platform.TENCENT

    async def execute(self):
        """
        执行播放在线歌曲指令

        Returns:
            MusicResponse:

        """
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = MusicRequest()

        request.platform = self.__platform
        request.name = self.__name

        cmd_id = PCProgramCmdId.PLAY_ONLINE_MUSIC_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            MusicResponse:

        """
        if isinstance(message, Message):
            data = message.bodyData
            response = MusicResponse()
            response.ParseFromString(data)
            return response
        else:
            return None
