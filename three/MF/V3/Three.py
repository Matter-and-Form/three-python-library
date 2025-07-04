from MF.V3 import Task
from MF.V3.Settings.Advanced import Advanced as MF_V3_Settings_Advanced_Advanced
from MF.V3.Settings.Align import Align as MF_V3_Settings_Align_Align
from MF.V3.Settings.AutoFocus import AutoFocus as MF_V3_Settings_AutoFocus_AutoFocus
from MF.V3.Settings.BoundingBox import BoundingBox as MF_V3_Settings_BoundingBox_BoundingBox
from MF.V3.Settings.Camera import Camera as MF_V3_Settings_Camera_Camera
from MF.V3.Settings.Capture import Capture as MF_V3_Settings_Capture_Capture
from MF.V3.Settings.CaptureImage import CaptureImage as MF_V3_Settings_CaptureImage_CaptureImage
from MF.V3.Settings.CopyGroups import CopyGroups as MF_V3_Settings_CopyGroups_CopyGroups
from MF.V3.Settings.Export import Export as MF_V3_Settings_Export_Export
from MF.V3.Settings.Group import Group as MF_V3_Settings_Group_Group
from MF.V3.Settings.HeatMap import HeatMap as MF_V3_Settings_HeatMap_HeatMap
from MF.V3.Settings.I18n import I18n as MF_V3_Settings_I18n_I18n
from MF.V3.Settings.Import import Import as MF_V3_Settings_Import_Import
from MF.V3.Settings.Merge import Merge as MF_V3_Settings_Merge_Merge
from MF.V3.Settings.NewGroup import NewGroup as MF_V3_Settings_NewGroup_NewGroup
from MF.V3.Settings.Project import Project as MF_V3_Settings_Project_Project
from MF.V3.Settings.Projector import Projector as MF_V3_Settings_Projector_Projector
from MF.V3.Settings.Scan import Scan as MF_V3_Settings_Scan_Scan
from MF.V3.Settings.ScanData import ScanData as MF_V3_Settings_ScanData_ScanData
from MF.V3.Settings.ScanSelection import ScanSelection as MF_V3_Settings_ScanSelection_ScanSelection
from MF.V3.Settings.Scanner import Scanner as MF_V3_Settings_Scanner_Scanner
from MF.V3.Settings.Smooth import Smooth as MF_V3_Settings_Smooth_Smooth
from MF.V3.Settings.Software import Software as MF_V3_Settings_Software_Software
from MF.V3.Settings.Style import Style as MF_V3_Settings_Style_Style
from MF.V3.Settings.Turntable import Turntable as MF_V3_Settings_Turntable_Turntable
from MF.V3.Settings.Tutorials import Tutorials as MF_V3_Settings_Tutorials_Tutorials
from MF.V3.Settings.Viewer import Viewer as MF_V3_Settings_Viewer_Viewer
from MF.V3.Settings.Wifi import Wifi as MF_V3_Settings_Wifi_Wifi
from MF.V3.Tasks.AddMergeToProject import AddMergeToProject as MF_V3_Tasks_AddMergeToProject
from MF.V3.Tasks.Align import Align as MF_V3_Tasks_Align
from MF.V3.Tasks.AutoFocus import AutoFocus as MF_V3_Tasks_AutoFocus
from MF.V3.Tasks.BoundingBox import BoundingBox as MF_V3_Tasks_BoundingBox
from MF.V3.Tasks.CalibrateCameras import CalibrateCameras as MF_V3_Tasks_CalibrateCameras
from MF.V3.Tasks.CalibrateTurntable import CalibrateTurntable as MF_V3_Tasks_CalibrateTurntable
from MF.V3.Tasks.CalibrationCaptureTargets import CalibrationCaptureTargets as MF_V3_Tasks_CalibrationCaptureTargets
from MF.V3.Tasks.CameraCalibration import CameraCalibration as MF_V3_Tasks_CameraCalibration
from MF.V3.Tasks.CaptureImage import CaptureImage as MF_V3_Tasks_CaptureImage
from MF.V3.Tasks.ClearSettings import ClearSettings as MF_V3_Tasks_ClearSettings
from MF.V3.Tasks.CloseProject import CloseProject as MF_V3_Tasks_CloseProject
from MF.V3.Tasks.ConnectWifi import ConnectWifi as MF_V3_Tasks_ConnectWifi
from MF.V3.Tasks.CopyGroups import CopyGroups as MF_V3_Tasks_CopyGroups
from MF.V3.Tasks.DepthMap import DepthMap as MF_V3_Tasks_DepthMap
from MF.V3.Tasks.DetectCalibrationCard import DetectCalibrationCard as MF_V3_Tasks_DetectCalibrationCard
from MF.V3.Tasks.DownloadProject import DownloadProject as MF_V3_Tasks_DownloadProject
from MF.V3.Tasks.Export import Export as MF_V3_Tasks_Export
from MF.V3.Tasks.ExportFactoryCalibrationLogs import ExportFactoryCalibrationLogs as MF_V3_Tasks_ExportFactoryCalibrationLogs
from MF.V3.Tasks.ExportHeatMap import ExportHeatMap as MF_V3_Tasks_ExportHeatMap
from MF.V3.Tasks.ExportLogs import ExportLogs as MF_V3_Tasks_ExportLogs
from MF.V3.Tasks.ExportMerge import ExportMerge as MF_V3_Tasks_ExportMerge
from MF.V3.Tasks.FactoryReset import FactoryReset as MF_V3_Tasks_FactoryReset
from MF.V3.Tasks.FlattenGroup import FlattenGroup as MF_V3_Tasks_FlattenGroup
from MF.V3.Tasks.ForgetWifi import ForgetWifi as MF_V3_Tasks_ForgetWifi
from MF.V3.Tasks.HasCameras import HasCameras as MF_V3_Tasks_HasCameras
from MF.V3.Tasks.HasProjector import HasProjector as MF_V3_Tasks_HasProjector
from MF.V3.Tasks.HasTurntable import HasTurntable as MF_V3_Tasks_HasTurntable
from MF.V3.Tasks.HeatMap import HeatMap as MF_V3_Tasks_HeatMap
from MF.V3.Tasks.Import import Import as MF_V3_Tasks_Import
from MF.V3.Tasks.ListExportFormats import ListExportFormats as MF_V3_Tasks_ListExportFormats
from MF.V3.Tasks.ListGroups import ListGroups as MF_V3_Tasks_ListGroups
from MF.V3.Tasks.ListNetworkInterfaces import ListNetworkInterfaces as MF_V3_Tasks_ListNetworkInterfaces
from MF.V3.Tasks.ListProjects import ListProjects as MF_V3_Tasks_ListProjects
from MF.V3.Tasks.ListScans import ListScans as MF_V3_Tasks_ListScans
from MF.V3.Tasks.ListSettings import ListSettings as MF_V3_Tasks_ListSettings
from MF.V3.Tasks.ListWifi import ListWifi as MF_V3_Tasks_ListWifi
from MF.V3.Tasks.Merge import Merge as MF_V3_Tasks_Merge
from MF.V3.Tasks.MergeData import MergeData as MF_V3_Tasks_MergeData
from MF.V3.Tasks.MoveGroup import MoveGroup as MF_V3_Tasks_MoveGroup
from MF.V3.Tasks.NewGroup import NewGroup as MF_V3_Tasks_NewGroup
from MF.V3.Tasks.NewProject import NewProject as MF_V3_Tasks_NewProject
from MF.V3.Tasks.NewScan import NewScan as MF_V3_Tasks_NewScan
from MF.V3.Tasks.OpenProject import OpenProject as MF_V3_Tasks_OpenProject
from MF.V3.Tasks.PopSettings import PopSettings as MF_V3_Tasks_PopSettings
from MF.V3.Tasks.PushSettings import PushSettings as MF_V3_Tasks_PushSettings
from MF.V3.Tasks.Reboot import Reboot as MF_V3_Tasks_Reboot
from MF.V3.Tasks.RemoveGroups import RemoveGroups as MF_V3_Tasks_RemoveGroups
from MF.V3.Tasks.RemoveProjects import RemoveProjects as MF_V3_Tasks_RemoveProjects
from MF.V3.Tasks.RestoreFactoryCalibration import RestoreFactoryCalibration as MF_V3_Tasks_RestoreFactoryCalibration
from MF.V3.Tasks.RotateTurntable import RotateTurntable as MF_V3_Tasks_RotateTurntable
from MF.V3.Tasks.ScanData import ScanData as MF_V3_Tasks_ScanData
from MF.V3.Tasks.SetCameras import SetCameras as MF_V3_Tasks_SetCameras
from MF.V3.Tasks.SetGroup import SetGroup as MF_V3_Tasks_SetGroup
from MF.V3.Tasks.SetProject import SetProject as MF_V3_Tasks_SetProject
from MF.V3.Tasks.SetProjector import SetProjector as MF_V3_Tasks_SetProjector
from MF.V3.Tasks.Shutdown import Shutdown as MF_V3_Tasks_Shutdown
from MF.V3.Tasks.Smooth import Smooth as MF_V3_Tasks_Smooth
from MF.V3.Tasks.SplitGroup import SplitGroup as MF_V3_Tasks_SplitGroup
from MF.V3.Tasks.StartVideo import StartVideo as MF_V3_Tasks_StartVideo
from MF.V3.Tasks.StopVideo import StopVideo as MF_V3_Tasks_StopVideo
from MF.V3.Tasks.SystemInfo import SystemInfo as MF_V3_Tasks_SystemInfo
from MF.V3.Tasks.TransformGroup import TransformGroup as MF_V3_Tasks_TransformGroup
from MF.V3.Tasks.TurntableCalibration import TurntableCalibration as MF_V3_Tasks_TurntableCalibration
from MF.V3.Tasks.UpdateSettings import UpdateSettings as MF_V3_Tasks_UpdateSettings
from MF.V3.Tasks.UploadProject import UploadProject as MF_V3_Tasks_UploadProject
from typing import List


def list_network_interfaces(self) -> Task:

    """
     List available wifi networks.
    """
    list_network_interfaces_request = MF_V3_Tasks_ListNetworkInterfaces.Request(
        Index=0,
        Type="ListNetworkInterfaces"
    )
    list_network_interfaces_response = MF_V3_Tasks_ListNetworkInterfaces.Response(
        Index=0,
        Type="ListNetworkInterfaces"
    )
    task = Task(Index=0, Type="ListNetworkInterfaces", Input=list_network_interfaces_request, Output=list_network_interfaces_response)
    self.SendTask(task)
    return task


def list_wifi(self) -> Task:

    """
     List available wifi networks.
    """
    list_wifi_request = MF_V3_Tasks_ListWifi.Request(
        Index=0,
        Type="ListWifi"
    )
    list_wifi_response = MF_V3_Tasks_ListWifi.Response(
        Index=0,
        Type="ListWifi"
    )
    task = Task(Index=0, Type="ListWifi", Input=list_wifi_request, Output=list_wifi_response)
    self.SendTask(task)
    return task


def connect_wifi(self, ssid: str, password: str) -> Task:

    """
     Connect to a wifi network.
    """
    connect_wifi_request = MF_V3_Tasks_ConnectWifi.Request(
        Index=0,
        Type="ConnectWifi",
        Input=MF_V3_Settings_Wifi_Wifi(
            ssid=ssid,
            password=password,
        )
    )
    connect_wifi_response = MF_V3_Tasks_ConnectWifi.Response(
        Index=0,
        Type="ConnectWifi",
        Input=MF_V3_Settings_Wifi_Wifi(
            ssid=ssid,
            password=password,
        )
    )
    task = Task(Index=0, Type="ConnectWifi", Input=connect_wifi_request, Output=connect_wifi_response)
    self.SendTask(task)
    return task


def forget_wifi(self) -> Task:

    """
     Forget all wifi connections.
    """
    forget_wifi_request = MF_V3_Tasks_ForgetWifi.Request(
        Index=0,
        Type="ForgetWifi"
    )
    forget_wifi_response = MF_V3_Tasks_ForgetWifi.Response(
        Index=0,
        Type="ForgetWifi"
    )
    task = Task(Index=0, Type="ForgetWifi", Input=forget_wifi_request, Output=forget_wifi_response)
    self.SendTask(task)
    return task


def list_settings(self) -> Task:

    """
     Get scanner settings.
    """
    list_settings_request = MF_V3_Tasks_ListSettings.Request(
        Index=0,
        Type="ListSettings"
    )
    list_settings_response = MF_V3_Tasks_ListSettings.Response(
        Index=0,
        Type="ListSettings"
    )
    task = Task(Index=0, Type="ListSettings", Input=list_settings_request, Output=list_settings_response)
    self.SendTask(task)
    return task


def push_settings(self) -> Task:

    """
     Push the current scanner settings to the settings stack.
    """
    push_settings_request = MF_V3_Tasks_PushSettings.Request(
        Index=0,
        Type="PushSettings"
    )
    push_settings_response = MF_V3_Tasks_PushSettings.Response(
        Index=0,
        Type="PushSettings"
    )
    task = Task(Index=0, Type="PushSettings", Input=push_settings_request, Output=push_settings_response)
    self.SendTask(task)
    return task


def pop_settings(self, Input: bool = None) -> Task:

    """
      Pop and restore scanner settings from the settings stack.
    """
    pop_settings_request = MF_V3_Tasks_PopSettings.Request(
        Index=0,
        Type="PopSettings",
        Input=Input
    )
    pop_settings_response = MF_V3_Tasks_PopSettings.Response(
        Index=0,
        Type="PopSettings"
    )
    task = Task(Index=0, Type="PopSettings", Input=pop_settings_request, Output=pop_settings_response)
    self.SendTask(task)
    return task


def update_settings(self, advanced: MF_V3_Settings_Advanced_Advanced = None, camera: MF_V3_Settings_Camera_Camera = None, capture: MF_V3_Settings_Capture_Capture = None, i18n: MF_V3_Settings_I18n_I18n = None, projector: MF_V3_Settings_Projector_Projector = None, style: MF_V3_Settings_Style_Style = None, turntable: MF_V3_Settings_Turntable_Turntable = None, tutorials: MF_V3_Settings_Tutorials_Tutorials = None, viewer: MF_V3_Settings_Viewer_Viewer = None, software: MF_V3_Settings_Software_Software = None) -> Task:

    """
     Update scanner settings.
    """
    update_settings_request = MF_V3_Tasks_UpdateSettings.Request(
        Index=0,
        Type="UpdateSettings",
        Input=MF_V3_Settings_Scanner_Scanner(
            advanced=advanced,
            camera=camera,
            capture=capture,
            i18n=i18n,
            projector=projector,
            style=style,
            turntable=turntable,
            tutorials=tutorials,
            viewer=viewer,
            software=software,
        )
    )
    update_settings_response = MF_V3_Tasks_UpdateSettings.Response(
        Index=0,
        Type="UpdateSettings",
        Input=MF_V3_Settings_Scanner_Scanner(
            advanced=advanced,
            camera=camera,
            capture=capture,
            i18n=i18n,
            projector=projector,
            style=style,
            turntable=turntable,
            tutorials=tutorials,
            viewer=viewer,
            software=software,
        )
    )
    task = Task(Index=0, Type="UpdateSettings", Input=update_settings_request, Output=update_settings_response)
    self.SendTask(task)
    return task


def list_projects(self) -> Task:

    """
     List all projects.
    """
    list_projects_request = MF_V3_Tasks_ListProjects.Request(
        Index=0,
        Type="ListProjects"
    )
    list_projects_response = MF_V3_Tasks_ListProjects.Response(
        Index=0,
        Type="ListProjects"
    )
    task = Task(Index=0, Type="ListProjects", Input=list_projects_request, Output=list_projects_response)
    self.SendTask(task)
    return task


def download_project(self, Input: int) -> Task:

    """
     Download a project from the scanner.
    """
    download_project_request = MF_V3_Tasks_DownloadProject.Request(
        Index=0,
        Type="DownloadProject",
        Input=Input
    )
    download_project_response = MF_V3_Tasks_DownloadProject.Response(
        Index=0,
        Type="DownloadProject",
        Input=Input
    )
    task = Task(Index=0, Type="DownloadProject", Input=download_project_request, Output=download_project_response)
    self.SendTask(task)
    return task


def upload_project(self, buffer: bytes) -> Task:

    """
     Upload a project to the scanner.
    """
    upload_project_request = MF_V3_Tasks_UploadProject.Request(
        Index=0,
        Type="UploadProject"
    )
    upload_project_response = MF_V3_Tasks_UploadProject.Response(
        Index=0,
        Type="UploadProject"
    )
    task = Task(Index=0, Type="UploadProject", Input=upload_project_request, Output=upload_project_response)
    self.SendTask(task, buffer)
    return task


def new_project(self, Input: str = None) -> Task:

    """
     Create a new project.
    """
    new_project_request = MF_V3_Tasks_NewProject.Request(
        Index=0,
        Type="NewProject",
        Input=Input
    )
    new_project_response = MF_V3_Tasks_NewProject.Response(
        Index=0,
        Type="NewProject"
    )
    task = Task(Index=0, Type="NewProject", Input=new_project_request, Output=new_project_response)
    self.SendTask(task)
    return task


def open_project(self, Input: int) -> Task:

    """
     Open an existing project.
    """
    open_project_request = MF_V3_Tasks_OpenProject.Request(
        Index=0,
        Type="OpenProject",
        Input=Input
    )
    open_project_response = MF_V3_Tasks_OpenProject.Response(
        Index=0,
        Type="OpenProject",
        Input=Input
    )
    task = Task(Index=0, Type="OpenProject", Input=open_project_request, Output=open_project_response)
    self.SendTask(task)
    return task


def clear_settings(self) -> Task:

    """
     Clear scanner settings and restore the default values.
    """
    clear_settings_request = MF_V3_Tasks_ClearSettings.Request(
        Index=0,
        Type="ClearSettings"
    )
    clear_settings_response = MF_V3_Tasks_ClearSettings.Response(
        Index=0,
        Type="ClearSettings"
    )
    task = Task(Index=0, Type="ClearSettings", Input=clear_settings_request, Output=clear_settings_response)
    self.SendTask(task)
    return task


def close_project(self) -> Task:

    """
     Close the current open project.
    """
    close_project_request = MF_V3_Tasks_CloseProject.Request(
        Index=0,
        Type="CloseProject"
    )
    close_project_response = MF_V3_Tasks_CloseProject.Response(
        Index=0,
        Type="CloseProject"
    )
    task = Task(Index=0, Type="CloseProject", Input=close_project_request, Output=close_project_response)
    self.SendTask(task)
    return task


def copy_groups(self, sourceIndexes: List[int] = None, targetIndex: int = None, childPosition: int = None, nameSuffix: str = None, enumerate: bool = None) -> Task:

    """
     Copy a set of scan groups in the current open project.
    """
    copy_groups_request = MF_V3_Tasks_CopyGroups.Request(
        Index=0,
        Type="CopyGroups",
        Input=MF_V3_Settings_CopyGroups_CopyGroups(
            sourceIndexes=sourceIndexes,
            targetIndex=targetIndex,
            childPosition=childPosition,
            nameSuffix=nameSuffix,
            enumerate=enumerate,
        )
    )
    copy_groups_response = MF_V3_Tasks_CopyGroups.Response(
        Index=0,
        Type="CopyGroups",
        Input=MF_V3_Settings_CopyGroups_CopyGroups(
            sourceIndexes=sourceIndexes,
            targetIndex=targetIndex,
            childPosition=childPosition,
            nameSuffix=nameSuffix,
            enumerate=enumerate,
        ),
        Output=None
    )
    task = Task(Index=0, Type="CopyGroups", Input=copy_groups_request, Output=copy_groups_response)
    self.SendTask(task)
    return task


def remove_projects(self, Input: List[int] = None) -> Task:

    """
     Remove selected projects.
    """
    remove_projects_request = MF_V3_Tasks_RemoveProjects.Request(
        Index=0,
        Type="RemoveProjects",
        Input=Input
    )
    remove_projects_response = MF_V3_Tasks_RemoveProjects.Response(
        Index=0,
        Type="RemoveProjects"
    )
    task = Task(Index=0, Type="RemoveProjects", Input=remove_projects_request, Output=remove_projects_response)
    self.SendTask(task)
    return task


def list_groups(self) -> Task:

    """
     List the scan groups in the current open project.
    """
    list_groups_request = MF_V3_Tasks_ListGroups.Request(
        Index=0,
        Type="ListGroups"
    )
    list_groups_response = MF_V3_Tasks_ListGroups.Response(
        Index=0,
        Type="ListGroups",
        Output=None
    )
    task = Task(Index=0, Type="ListGroups", Input=list_groups_request, Output=list_groups_response)
    self.SendTask(task)
    return task


def list_scans(self) -> Task:

    """
     List the scans in the current open project.
    """
    list_scans_request = MF_V3_Tasks_ListScans.Request(
        Index=0,
        Type="ListScans"
    )
    list_scans_response = MF_V3_Tasks_ListScans.Response(
        Index=0,
        Type="ListScans"
    )
    task = Task(Index=0, Type="ListScans", Input=list_scans_request, Output=list_scans_response)
    self.SendTask(task)
    return task


def scan_data(self, index: int, mergeStep: MF_V3_Settings_ScanData_ScanData.MergeStep = None, buffers: List[MF_V3_Settings_ScanData_ScanData.Buffer] = None, metadata: List[MF_V3_Settings_ScanData_ScanData.Metadata] = None) -> Task:

    """
     Download the raw scan data for a scan in the current open project.
    """
    scan_data_request = MF_V3_Tasks_ScanData.Request(
        Index=0,
        Type="ScanData",
        Input=MF_V3_Settings_ScanData_ScanData(
            index=index,
            mergeStep=mergeStep,
            buffers=buffers,
            metadata=metadata,
        )
    )
    scan_data_response = MF_V3_Tasks_ScanData.Response(
        Index=0,
        Type="ScanData",
        Input=MF_V3_Settings_ScanData_ScanData(
            index=index,
            mergeStep=mergeStep,
            buffers=buffers,
            metadata=metadata,
        ),
        Output=None
    )
    task = Task(Index=0, Type="ScanData", Input=scan_data_request, Output=scan_data_response)
    self.SendTask(task)
    return task


def set_project(self, index: int = None, name: str = None) -> Task:

    """
     Apply settings to the current open project.
    """
    set_project_request = MF_V3_Tasks_SetProject.Request(
        Index=0,
        Type="SetProject",
        Input=MF_V3_Settings_Project_Project(
            index=index,
            name=name,
        )
    )
    set_project_response = MF_V3_Tasks_SetProject.Response(
        Index=0,
        Type="SetProject"
    )
    task = Task(Index=0, Type="SetProject", Input=set_project_request, Output=set_project_response)
    self.SendTask(task)
    return task


def set_group(self, index: int, name: str = None, color: List[float] = None, visible: bool = None, collapsed: bool = None, rotation: List[float] = None, translation: List[float] = None) -> Task:

    """
     Set scan group properties.
    """
    set_group_request = MF_V3_Tasks_SetGroup.Request(
        Index=0,
        Type="SetGroup",
        Input=MF_V3_Settings_Group_Group(
            index=index,
            name=name,
            color=color,
            visible=visible,
            collapsed=collapsed,
            rotation=rotation,
            translation=translation,
        )
    )
    set_group_response = MF_V3_Tasks_SetGroup.Response(
        Index=0,
        Type="SetGroup",
        Input=MF_V3_Settings_Group_Group(
            index=index,
            name=name,
            color=color,
            visible=visible,
            collapsed=collapsed,
            rotation=rotation,
            translation=translation,
        ),
        Output=None
    )
    task = Task(Index=0, Type="SetGroup", Input=set_group_request, Output=set_group_response)
    self.SendTask(task)
    return task


def new_group(self, parentIndex: int = None, baseName: str = None, color: List[float] = None, visible: bool = None, collapsed: bool = None, rotation: List[float] = None, translation: List[float] = None) -> Task:

    """
     Create a new scan group.
    """
    new_group_request = MF_V3_Tasks_NewGroup.Request(
        Index=0,
        Type="NewGroup",
        Input=MF_V3_Settings_NewGroup_NewGroup(
            parentIndex=parentIndex,
            baseName=baseName,
            color=color,
            visible=visible,
            collapsed=collapsed,
            rotation=rotation,
            translation=translation,
        )
    )
    new_group_response = MF_V3_Tasks_NewGroup.Response(
        Index=0,
        Type="NewGroup",
        Output=None
    )
    task = Task(Index=0, Type="NewGroup", Input=new_group_request, Output=new_group_response)
    self.SendTask(task)
    return task


def move_group(self, Input: List[int] = None) -> Task:

    """
     Move a scan group.
    """
    move_group_request = MF_V3_Tasks_MoveGroup.Request(
        Index=0,
        Type="MoveGroup",
        Input=Input
    )
    move_group_response = MF_V3_Tasks_MoveGroup.Response(
        Index=0,
        Type="MoveGroup",
        Output=None
    )
    task = Task(Index=0, Type="MoveGroup", Input=move_group_request, Output=move_group_response)
    self.SendTask(task)
    return task


def factory_reset(self) -> Task:

    """
     Reset the scanner to factory settings.
    """
    factory_reset_request = MF_V3_Tasks_FactoryReset.Request(
        Index=0,
        Type="FactoryReset"
    )
    factory_reset_response = MF_V3_Tasks_FactoryReset.Response(
        Index=0,
        Type="FactoryReset"
    )
    task = Task(Index=0, Type="FactoryReset", Input=factory_reset_request, Output=factory_reset_response)
    self.SendTask(task)
    return task


def flatten_group(self, Input: int) -> Task:

    """
     Flatten a scan group such that it only consists of single scans.
    """
    flatten_group_request = MF_V3_Tasks_FlattenGroup.Request(
        Index=0,
        Type="FlattenGroup",
        Input=Input
    )
    flatten_group_response = MF_V3_Tasks_FlattenGroup.Response(
        Index=0,
        Type="FlattenGroup",
        Input=Input,
        Output=None
    )
    task = Task(Index=0, Type="FlattenGroup", Input=flatten_group_request, Output=flatten_group_response)
    self.SendTask(task)
    return task


def split_group(self, Input: int) -> Task:

    """
     Split a scan group (ie. move its subgroups to its parent group).
    """
    split_group_request = MF_V3_Tasks_SplitGroup.Request(
        Index=0,
        Type="SplitGroup",
        Input=Input
    )
    split_group_response = MF_V3_Tasks_SplitGroup.Response(
        Index=0,
        Type="SplitGroup",
        Input=Input,
        Output=None
    )
    task = Task(Index=0, Type="SplitGroup", Input=split_group_request, Output=split_group_response)
    self.SendTask(task)
    return task


def transform_group(self, index: int, name: str = None, color: List[float] = None, visible: bool = None, collapsed: bool = None, rotation: List[float] = None, translation: List[float] = None) -> Task:

    """
     Apply a rigid transformation to a group.
    """
    transform_group_request = MF_V3_Tasks_TransformGroup.Request(
        Index=0,
        Type="TransformGroup",
        Input=MF_V3_Settings_Group_Group(
            index=index,
            name=name,
            color=color,
            visible=visible,
            collapsed=collapsed,
            rotation=rotation,
            translation=translation,
        )
    )
    transform_group_response = MF_V3_Tasks_TransformGroup.Response(
        Index=0,
        Type="TransformGroup",
        Input=MF_V3_Settings_Group_Group(
            index=index,
            name=name,
            color=color,
            visible=visible,
            collapsed=collapsed,
            rotation=rotation,
            translation=translation,
        ),
        Output=None
    )
    task = Task(Index=0, Type="TransformGroup", Input=transform_group_request, Output=transform_group_response)
    self.SendTask(task)
    return task


def remove_groups(self, Input: List[int] = None) -> Task:

    """
     Remove selected scan groups.
    """
    remove_groups_request = MF_V3_Tasks_RemoveGroups.Request(
        Index=0,
        Type="RemoveGroups",
        Input=Input
    )
    remove_groups_response = MF_V3_Tasks_RemoveGroups.Response(
        Index=0,
        Type="RemoveGroups",
        Output=None
    )
    task = Task(Index=0, Type="RemoveGroups", Input=remove_groups_request, Output=remove_groups_response)
    self.SendTask(task)
    return task


def bounding_box(self, selection: MF_V3_Settings_ScanSelection_ScanSelection, axisAligned: bool) -> Task:

    """
     Get the bounding box of a set of scan groups.
    """
    bounding_box_request = MF_V3_Tasks_BoundingBox.Request(
        Index=0,
        Type="BoundingBox",
        Input=MF_V3_Settings_BoundingBox_BoundingBox(
            selection=selection,
            axisAligned=axisAligned,
        )
    )
    bounding_box_response = MF_V3_Tasks_BoundingBox.Response(
        Index=0,
        Type="BoundingBox",
        Input=MF_V3_Settings_BoundingBox_BoundingBox(
            selection=selection,
            axisAligned=axisAligned,
        ),
        Output=None
    )
    task = Task(Index=0, Type="BoundingBox", Input=bounding_box_request, Output=bounding_box_response)
    self.SendTask(task)
    return task


def align(self, source: int, target: int, rough: MF_V3_Settings_Align_Align.Rough = None, fine: MF_V3_Settings_Align_Align.Fine = None) -> Task:

    """
     Align two scan groups.
    """
    align_request = MF_V3_Tasks_Align.Request(
        Index=0,
        Type="Align",
        Input=MF_V3_Settings_Align_Align(
            source=source,
            target=target,
            rough=rough,
            fine=fine,
        )
    )
    align_response = MF_V3_Tasks_Align.Response(
        Index=0,
        Type="Align",
        Input=MF_V3_Settings_Align_Align(
            source=source,
            target=target,
            rough=rough,
            fine=fine,
        ),
        Output=None
    )
    task = Task(Index=0, Type="Align", Input=align_request, Output=align_response)
    self.SendTask(task)
    return task


def smooth(self, selection: MF_V3_Settings_ScanSelection_ScanSelection = None, taubin: MF_V3_Settings_Smooth_Smooth.Taubin = None) -> Task:

    """
     Smooth a set of scans.
    """
    smooth_request = MF_V3_Tasks_Smooth.Request(
        Index=0,
        Type="Smooth",
        Input=MF_V3_Settings_Smooth_Smooth(
            selection=selection,
            taubin=taubin,
        )
    )
    smooth_response = MF_V3_Tasks_Smooth.Response(
        Index=0,
        Type="Smooth",
        Input=MF_V3_Settings_Smooth_Smooth(
            selection=selection,
            taubin=taubin,
        )
    )
    task = Task(Index=0, Type="Smooth", Input=smooth_request, Output=smooth_response)
    self.SendTask(task)
    return task


def heat_map(self, sources: List[int] = None, targets: List[int] = None, outlierDistance: float = None) -> Task:

    """
     Compute the point-to-mesh distances of a source mesh to a target mesh and visualize as a heat map.
    """
    heat_map_request = MF_V3_Tasks_HeatMap.Request(
        Index=0,
        Type="HeatMap",
        Input=MF_V3_Settings_HeatMap_HeatMap(
            sources=sources,
            targets=targets,
            outlierDistance=outlierDistance,
        )
    )
    heat_map_response = MF_V3_Tasks_HeatMap.Response(
        Index=0,
        Type="HeatMap",
        Input=MF_V3_Settings_HeatMap_HeatMap(
            sources=sources,
            targets=targets,
            outlierDistance=outlierDistance,
        ),
        Output=None
    )
    task = Task(Index=0, Type="HeatMap", Input=heat_map_request, Output=heat_map_response)
    self.SendTask(task)
    return task


def merge(self, selection: MF_V3_Settings_ScanSelection_ScanSelection = None, remesh: MF_V3_Settings_Merge_Merge.Remesh = None, simplify: MF_V3_Settings_Merge_Merge.Simplify = None, texturize: bool = None) -> Task:

    """
     Merge two or more scan groups.
    """
    merge_request = MF_V3_Tasks_Merge.Request(
        Index=0,
        Type="Merge",
        Input=MF_V3_Settings_Merge_Merge(
            selection=selection,
            remesh=remesh,
            simplify=simplify,
            texturize=texturize,
        )
    )
    merge_response = MF_V3_Tasks_Merge.Response(
        Index=0,
        Type="Merge",
        Input=MF_V3_Settings_Merge_Merge(
            selection=selection,
            remesh=remesh,
            simplify=simplify,
            texturize=texturize,
        ),
        Output=None
    )
    task = Task(Index=0, Type="Merge", Input=merge_request, Output=merge_response)
    self.SendTask(task)
    return task


def merge_data(self, index: int, mergeStep: MF_V3_Settings_ScanData_ScanData.MergeStep = None, buffers: List[MF_V3_Settings_ScanData_ScanData.Buffer] = None, metadata: List[MF_V3_Settings_ScanData_ScanData.Metadata] = None) -> Task:

    """
     Download the raw scan data for the current merge process.
    """
    merge_data_request = MF_V3_Tasks_MergeData.Request(
        Index=0,
        Type="MergeData",
        Input=MF_V3_Settings_ScanData_ScanData(
            index=index,
            mergeStep=mergeStep,
            buffers=buffers,
            metadata=metadata,
        )
    )
    merge_data_response = MF_V3_Tasks_MergeData.Response(
        Index=0,
        Type="MergeData",
        Input=MF_V3_Settings_ScanData_ScanData(
            index=index,
            mergeStep=mergeStep,
            buffers=buffers,
            metadata=metadata,
        ),
        Output=None
    )
    task = Task(Index=0, Type="MergeData", Input=merge_data_request, Output=merge_data_response)
    self.SendTask(task)
    return task


def add_merge_to_project(self) -> Task:

    """
     Add a merged scan to the current project.
    """
    add_merge_to_project_request = MF_V3_Tasks_AddMergeToProject.Request(
        Index=0,
        Type="AddMergeToProject"
    )
    add_merge_to_project_response = MF_V3_Tasks_AddMergeToProject.Response(
        Index=0,
        Type="AddMergeToProject",
        Output=None
    )
    task = Task(Index=0, Type="AddMergeToProject", Input=add_merge_to_project_request, Output=add_merge_to_project_response)
    self.SendTask(task)
    return task


def import_file(self, name: str = None, scale: float = None, unit: MF_V3_Settings_Import_Import.Unit = None, center: bool = None, groupIndex: int = None) -> Task:

    """
     Import a set of 3D meshes to the current open project.  The meshes must be archived in a ZIP file.
    """
    import_file_request = MF_V3_Tasks_Import.Request(
        Index=0,
        Type="Import",
        Input=MF_V3_Settings_Import_Import(
            name=name,
            scale=scale,
            unit=unit,
            center=center,
            groupIndex=groupIndex,
        )
    )
    import_file_response = MF_V3_Tasks_Import.Response(
        Index=0,
        Type="Import"
    )
    task = Task(Index=0, Type="Import", Input=import_file_request, Output=import_file_response)
    self.SendTask(task)
    return task


def list_export_formats(self) -> Task:

    """
     List all export formats.
    """
    list_export_formats_request = MF_V3_Tasks_ListExportFormats.Request(
        Index=0,
        Type="ListExportFormats"
    )
    list_export_formats_response = MF_V3_Tasks_ListExportFormats.Response(
        Index=0,
        Type="ListExportFormats"
    )
    task = Task(Index=0, Type="ListExportFormats", Input=list_export_formats_request, Output=list_export_formats_response)
    self.SendTask(task)
    return task


def export(self, selection: MF_V3_Settings_ScanSelection_ScanSelection = None, texture: bool = None, merge: bool = None, format: MF_V3_Settings_Export_Export.Format = None, scale: float = None, color: MF_V3_Settings_Export_Export.Color = None) -> Task:

    """
     Export a group of scans.
    """
    export_request = MF_V3_Tasks_Export.Request(
        Index=0,
        Type="Export",
        Input=MF_V3_Settings_Export_Export(
            selection=selection,
            texture=texture,
            merge=merge,
            format=format,
            scale=scale,
            color=color,
        )
    )
    export_response = MF_V3_Tasks_Export.Response(
        Index=0,
        Type="Export",
        Input=MF_V3_Settings_Export_Export(
            selection=selection,
            texture=texture,
            merge=merge,
            format=format,
            scale=scale,
            color=color,
        )
    )
    task = Task(Index=0, Type="Export", Input=export_request, Output=export_response)
    self.SendTask(task)
    return task


def export_heat_map(self, selection: MF_V3_Settings_ScanSelection_ScanSelection = None, texture: bool = None, merge: bool = None, format: MF_V3_Settings_Export_Export.Format = None, scale: float = None, color: MF_V3_Settings_Export_Export.Color = None) -> Task:

    """
     Export a mesh with vertex colors generated by the 'HeatMap' task.
    """
    export_heat_map_request = MF_V3_Tasks_ExportHeatMap.Request(
        Index=0,
        Type="ExportHeatMap",
        Input=MF_V3_Settings_Export_Export(
            selection=selection,
            texture=texture,
            merge=merge,
            format=format,
            scale=scale,
            color=color,
        )
    )
    export_heat_map_response = MF_V3_Tasks_ExportHeatMap.Response(
        Index=0,
        Type="ExportHeatMap",
        Input=MF_V3_Settings_Export_Export(
            selection=selection,
            texture=texture,
            merge=merge,
            format=format,
            scale=scale,
            color=color,
        )
    )
    task = Task(Index=0, Type="ExportHeatMap", Input=export_heat_map_request, Output=export_heat_map_response)
    self.SendTask(task)
    return task


def export_merge(self, selection: MF_V3_Settings_ScanSelection_ScanSelection = None, texture: bool = None, merge: bool = None, format: MF_V3_Settings_Export_Export.Format = None, scale: float = None, color: MF_V3_Settings_Export_Export.Color = None) -> Task:

    """
     Export a merged scan.
    """
    export_merge_request = MF_V3_Tasks_ExportMerge.Request(
        Index=0,
        Type="ExportMerge",
        Input=MF_V3_Settings_Export_Export(
            selection=selection,
            texture=texture,
            merge=merge,
            format=format,
            scale=scale,
            color=color,
        )
    )
    export_merge_response = MF_V3_Tasks_ExportMerge.Response(
        Index=0,
        Type="ExportMerge",
        Input=MF_V3_Settings_Export_Export(
            selection=selection,
            texture=texture,
            merge=merge,
            format=format,
            scale=scale,
            color=color,
        )
    )
    task = Task(Index=0, Type="ExportMerge", Input=export_merge_request, Output=export_merge_response)
    self.SendTask(task)
    return task


def export_logs(self, Input: bool = None) -> Task:

    """
     Export scanner logs.
    """
    export_logs_request = MF_V3_Tasks_ExportLogs.Request(
        Index=0,
        Type="ExportLogs",
        Input=Input
    )
    export_logs_response = MF_V3_Tasks_ExportLogs.Response(
        Index=0,
        Type="ExportLogs"
    )
    task = Task(Index=0, Type="ExportLogs", Input=export_logs_request, Output=export_logs_response)
    self.SendTask(task)
    return task


def export_factory_calibration_logs(self) -> Task:

    """
     Export factory calibration logs.
    """
    export_factory_calibration_logs_request = MF_V3_Tasks_ExportFactoryCalibrationLogs.Request(
        Index=0,
        Type="ExportFactoryCalibrationLogs"
    )
    export_factory_calibration_logs_response = MF_V3_Tasks_ExportFactoryCalibrationLogs.Response(
        Index=0,
        Type="ExportFactoryCalibrationLogs"
    )
    task = Task(Index=0, Type="ExportFactoryCalibrationLogs", Input=export_factory_calibration_logs_request, Output=export_factory_calibration_logs_response)
    self.SendTask(task)
    return task


def has_cameras(self) -> Task:

    """
     Check if the scanner has working cameras.
    """
    has_cameras_request = MF_V3_Tasks_HasCameras.Request(
        Index=0,
        Type="HasCameras"
    )
    has_cameras_response = MF_V3_Tasks_HasCameras.Response(
        Index=0,
        Type="HasCameras"
    )
    task = Task(Index=0, Type="HasCameras", Input=has_cameras_request, Output=has_cameras_response)
    self.SendTask(task)
    return task


def has_projector(self) -> Task:

    """
     Check if the scanner has a working projector.
    """
    has_projector_request = MF_V3_Tasks_HasProjector.Request(
        Index=0,
        Type="HasProjector"
    )
    has_projector_response = MF_V3_Tasks_HasProjector.Response(
        Index=0,
        Type="HasProjector"
    )
    task = Task(Index=0, Type="HasProjector", Input=has_projector_request, Output=has_projector_response)
    self.SendTask(task)
    return task


def has_turntable(self) -> Task:

    """
     Check if the scanner is connected to a working turntable.
    """
    has_turntable_request = MF_V3_Tasks_HasTurntable.Request(
        Index=0,
        Type="HasTurntable"
    )
    has_turntable_response = MF_V3_Tasks_HasTurntable.Response(
        Index=0,
        Type="HasTurntable"
    )
    task = Task(Index=0, Type="HasTurntable", Input=has_turntable_request, Output=has_turntable_response)
    self.SendTask(task)
    return task


def system_info(self, updateMajor: bool = None, updateNightly: bool = None) -> Task:

    """
     Get system information.
    """
    system_info_request = MF_V3_Tasks_SystemInfo.Request(
        Index=0,
        Type="SystemInfo",
        Input=MF_V3_Settings_Software_Software(
            updateMajor=updateMajor,
            updateNightly=updateNightly,
        )
    )
    system_info_response = MF_V3_Tasks_SystemInfo.Response(
        Index=0,
        Type="SystemInfo",
        Output=None
    )
    task = Task(Index=0, Type="SystemInfo", Input=system_info_request, Output=system_info_response)
    self.SendTask(task)
    return task


def camera_calibration(self) -> Task:

    """
     Get the camera calibration descriptor.
    """
    camera_calibration_request = MF_V3_Tasks_CameraCalibration.Request(
        Index=0,
        Type="CameraCalibration"
    )
    camera_calibration_response = MF_V3_Tasks_CameraCalibration.Response(
        Index=0,
        Type="CameraCalibration"
    )
    task = Task(Index=0, Type="CameraCalibration", Input=camera_calibration_request, Output=camera_calibration_response)
    self.SendTask(task)
    return task


def turntable_calibration(self) -> Task:

    """
     Get the turntable calibration descriptor.
    """
    turntable_calibration_request = MF_V3_Tasks_TurntableCalibration.Request(
        Index=0,
        Type="TurntableCalibration"
    )
    turntable_calibration_response = MF_V3_Tasks_TurntableCalibration.Response(
        Index=0,
        Type="TurntableCalibration"
    )
    task = Task(Index=0, Type="TurntableCalibration", Input=turntable_calibration_request, Output=turntable_calibration_response)
    self.SendTask(task)
    return task


def calibration_capture_targets(self) -> Task:

    """
     Get the calibration capture target for each camera calibration capture.
    """
    calibration_capture_targets_request = MF_V3_Tasks_CalibrationCaptureTargets.Request(
        Index=0,
        Type="CalibrationCaptureTargets"
    )
    calibration_capture_targets_response = MF_V3_Tasks_CalibrationCaptureTargets.Response(
        Index=0,
        Type="CalibrationCaptureTargets"
    )
    task = Task(Index=0, Type="CalibrationCaptureTargets", Input=calibration_capture_targets_request, Output=calibration_capture_targets_response)
    self.SendTask(task)
    return task


def calibrate_cameras(self) -> Task:

    """
     Calibrate the cameras.
    """
    calibrate_cameras_request = MF_V3_Tasks_CalibrateCameras.Request(
        Index=0,
        Type="CalibrateCameras"
    )
    calibrate_cameras_response = MF_V3_Tasks_CalibrateCameras.Response(
        Index=0,
        Type="CalibrateCameras"
    )
    task = Task(Index=0, Type="CalibrateCameras", Input=calibrate_cameras_request, Output=calibrate_cameras_response)
    self.SendTask(task)
    return task


def calibrate_turntable(self) -> Task:

    """
     Calibrate the turntable.
    """
    calibrate_turntable_request = MF_V3_Tasks_CalibrateTurntable.Request(
        Index=0,
        Type="CalibrateTurntable"
    )
    calibrate_turntable_response = MF_V3_Tasks_CalibrateTurntable.Response(
        Index=0,
        Type="CalibrateTurntable"
    )
    task = Task(Index=0, Type="CalibrateTurntable", Input=calibrate_turntable_request, Output=calibrate_turntable_response)
    self.SendTask(task)
    return task


def detect_calibration_card(self, Input: int) -> Task:

    """
     Detect the calibration card on one or both cameras.
    """
    detect_calibration_card_request = MF_V3_Tasks_DetectCalibrationCard.Request(
        Index=0,
        Type="DetectCalibrationCard",
        Input=Input
    )
    detect_calibration_card_response = MF_V3_Tasks_DetectCalibrationCard.Response(
        Index=0,
        Type="DetectCalibrationCard",
        Input=Input
    )
    task = Task(Index=0, Type="DetectCalibrationCard", Input=detect_calibration_card_request, Output=detect_calibration_card_response)
    self.SendTask(task)
    return task


def restore_factory_calibration(self) -> Task:

    """
     Restore factory calibration.
    """
    restore_factory_calibration_request = MF_V3_Tasks_RestoreFactoryCalibration.Request(
        Index=0,
        Type="RestoreFactoryCalibration"
    )
    restore_factory_calibration_response = MF_V3_Tasks_RestoreFactoryCalibration.Response(
        Index=0,
        Type="RestoreFactoryCalibration"
    )
    task = Task(Index=0, Type="RestoreFactoryCalibration", Input=restore_factory_calibration_request, Output=restore_factory_calibration_response)
    self.SendTask(task)
    return task


def start_video(self) -> Task:

    """
     Start the video stream.
    """
    start_video_request = MF_V3_Tasks_StartVideo.Request(
        Index=0,
        Type="StartVideo"
    )
    start_video_response = MF_V3_Tasks_StartVideo.Response(
        Index=0,
        Type="StartVideo"
    )
    task = Task(Index=0, Type="StartVideo", Input=start_video_request, Output=start_video_response)
    self.SendTask(task)
    return task


def stop_video(self) -> Task:

    """
     Stop the video stream.
    """
    stop_video_request = MF_V3_Tasks_StopVideo.Request(
        Index=0,
        Type="StopVideo"
    )
    stop_video_response = MF_V3_Tasks_StopVideo.Response(
        Index=0,
        Type="StopVideo"
    )
    task = Task(Index=0, Type="StopVideo", Input=stop_video_request, Output=stop_video_response)
    self.SendTask(task)
    return task


def set_cameras(self, selection: List[int] = None, autoExposure: bool = None, exposure: int = None, analogGain: float = None, digitalGain: int = None, focus: int = None) -> Task:

    """
     Apply camera settings to one or both cameras.
    """
    set_cameras_request = MF_V3_Tasks_SetCameras.Request(
        Index=0,
        Type="SetCameras",
        Input=MF_V3_Settings_Camera_Camera(
            selection=selection,
            autoExposure=autoExposure,
            exposure=exposure,
            analogGain=analogGain,
            digitalGain=digitalGain,
            focus=focus,
        )
    )
    set_cameras_response = MF_V3_Tasks_SetCameras.Response(
        Index=0,
        Type="SetCameras"
    )
    task = Task(Index=0, Type="SetCameras", Input=set_cameras_request, Output=set_cameras_response)
    self.SendTask(task)
    return task


def set_projector(self, on: bool = None, brightness: float = None, pattern: MF_V3_Settings_Projector_Projector.Pattern = None, image: MF_V3_Settings_Projector_Projector.Image = None, color: List[float] = None, buffer: bytes = None) -> Task:

    """
     Apply projector settings.
    """
    set_projector_request = MF_V3_Tasks_SetProjector.Request(
        Index=0,
        Type="SetProjector",
        Input=MF_V3_Settings_Projector_Projector(
            on=on,
            brightness=brightness,
            pattern=pattern,
            image=image,
            color=color,
        )
    )
    set_projector_response = MF_V3_Tasks_SetProjector.Response(
        Index=0,
        Type="SetProjector"
    )
    task = Task(Index=0, Type="SetProjector", Input=set_projector_request, Output=set_projector_response)
    self.SendTask(task, buffer)
    return task


def auto_focus(self, applyAll: bool, cameras: List[MF_V3_Settings_AutoFocus_AutoFocus.Camera] = None) -> Task:

    """
     Auto focus one or both cameras.
    """
    auto_focus_request = MF_V3_Tasks_AutoFocus.Request(
        Index=0,
        Type="AutoFocus",
        Input=MF_V3_Settings_AutoFocus_AutoFocus(
            applyAll=applyAll,
            cameras=cameras,
        )
    )
    auto_focus_response = MF_V3_Tasks_AutoFocus.Response(
        Index=0,
        Type="AutoFocus"
    )
    task = Task(Index=0, Type="AutoFocus", Input=auto_focus_request, Output=auto_focus_response)
    self.SendTask(task)
    return task


def rotate_turntable(self, Input: int) -> Task:

    """
     Rotate the turntable.
    """
    rotate_turntable_request = MF_V3_Tasks_RotateTurntable.Request(
        Index=0,
        Type="RotateTurntable",
        Input=Input
    )
    rotate_turntable_response = MF_V3_Tasks_RotateTurntable.Response(
        Index=0,
        Type="RotateTurntable",
        Input=Input
    )
    task = Task(Index=0, Type="RotateTurntable", Input=rotate_turntable_request, Output=rotate_turntable_response)
    self.SendTask(task)
    return task


def new_scan(self, camera: MF_V3_Settings_Camera_Camera = None, projector: MF_V3_Settings_Projector_Projector = None, turntable: MF_V3_Settings_Turntable_Turntable = None, capture: MF_V3_Settings_Capture_Capture = None, processing: MF_V3_Settings_Scan_Scan.Processing = None, alignWithScanner: bool = None, centerAtOrigin: bool = None) -> Task:

    """
     Capture a new scan.
    """
    new_scan_request = MF_V3_Tasks_NewScan.Request(
        Index=0,
        Type="NewScan",
        Input=MF_V3_Settings_Scan_Scan(
            camera=camera,
            projector=projector,
            turntable=turntable,
            capture=capture,
            processing=processing,
            alignWithScanner=alignWithScanner,
            centerAtOrigin=centerAtOrigin,
        )
    )
    new_scan_response = MF_V3_Tasks_NewScan.Response(
        Index=0,
        Type="NewScan"
    )
    task = Task(Index=0, Type="NewScan", Input=new_scan_request, Output=new_scan_response)
    self.SendTask(task)
    return task


def capture_image(self, selection: List[int] = None, codec: MF_V3_Settings_CaptureImage_CaptureImage.Codec = None, grayscale: bool = None) -> Task:

    """
     Capture a single Image.
    """
    capture_image_request = MF_V3_Tasks_CaptureImage.Request(
        Index=0,
        Type="CaptureImage",
        Input=MF_V3_Settings_CaptureImage_CaptureImage(
            selection=selection,
            codec=codec,
            grayscale=grayscale,
        )
    )
    capture_image_response = MF_V3_Tasks_CaptureImage.Response(
        Index=0,
        Type="CaptureImage",
        Input=MF_V3_Settings_CaptureImage_CaptureImage(
            selection=selection,
            codec=codec,
            grayscale=grayscale,
        )
    )
    task = Task(Index=0, Type="CaptureImage", Input=capture_image_request, Output=capture_image_response)
    self.SendTask(task)
    return task


def depth_map(self, camera: MF_V3_Settings_Camera_Camera = None, projector: MF_V3_Settings_Projector_Projector = None, turntable: MF_V3_Settings_Turntable_Turntable = None, capture: MF_V3_Settings_Capture_Capture = None, processing: MF_V3_Settings_Scan_Scan.Processing = None, alignWithScanner: bool = None, centerAtOrigin: bool = None) -> Task:

    """
     Capture a depth map.
    """
    depth_map_request = MF_V3_Tasks_DepthMap.Request(
        Index=0,
        Type="DepthMap",
        Input=MF_V3_Settings_Scan_Scan(
            camera=camera,
            projector=projector,
            turntable=turntable,
            capture=capture,
            processing=processing,
            alignWithScanner=alignWithScanner,
            centerAtOrigin=centerAtOrigin,
        )
    )
    depth_map_response = MF_V3_Tasks_DepthMap.Response(
        Index=0,
        Type="DepthMap"
    )
    task = Task(Index=0, Type="DepthMap", Input=depth_map_request, Output=depth_map_response)
    self.SendTask(task)
    return task


def reboot(self) -> Task:

    """
     Reboot the scanner.
    """
    reboot_request = MF_V3_Tasks_Reboot.Request(
        Index=0,
        Type="Reboot"
    )
    reboot_response = MF_V3_Tasks_Reboot.Response(
        Index=0,
        Type="Reboot"
    )
    task = Task(Index=0, Type="Reboot", Input=reboot_request, Output=reboot_response)
    self.SendTask(task)
    return task


def shutdown(self) -> Task:

    """
     Shutdown the scanner.
    """
    shutdown_request = MF_V3_Tasks_Shutdown.Request(
        Index=0,
        Type="Shutdown"
    )
    shutdown_response = MF_V3_Tasks_Shutdown.Response(
        Index=0,
        Type="Shutdown"
    )
    task = Task(Index=0, Type="Shutdown", Input=shutdown_request, Output=shutdown_response)
    self.SendTask(task)
    return task




