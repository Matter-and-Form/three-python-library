import MF
import MF.V3
import MF.V3.Settings
import MF.V3.Settings.Advanced
import MF.V3.Settings.Align
import MF.V3.Settings.AutoFocus
import MF.V3.Settings.BoundingBox
import MF.V3.Settings.Camera
import MF.V3.Settings.Capture
import MF.V3.Settings.Export
import MF.V3.Settings.Group
import MF.V3.Settings.I18n
import MF.V3.Settings.Merge
import MF.V3.Settings.NewGroup
import MF.V3.Settings.Project
import MF.V3.Settings.Projector
import MF.V3.Settings.Scan
import MF.V3.Settings.ScanData
import MF.V3.Settings.ScanSelection
import MF.V3.Settings.Scanner
import MF.V3.Settings.Software
import MF.V3.Settings.Style
import MF.V3.Settings.Turntable
import MF.V3.Settings.Tutorials
import MF.V3.Settings.Viewer
import MF.V3.Settings.Wifi
import MF.V3.Tasks
import MF.V3.Tasks.AddMergeToProject
import MF.V3.Tasks.Align
import MF.V3.Tasks.AutoFocus
import MF.V3.Tasks.BoundingBox
import MF.V3.Tasks.CalibrateCameras
import MF.V3.Tasks.CalibrateTurntable
import MF.V3.Tasks.CalibrationCaptureTargets
import MF.V3.Tasks.CameraCalibration
import MF.V3.Tasks.CloseProject
import MF.V3.Tasks.ConnectWifi
import MF.V3.Tasks.DepthMap
import MF.V3.Tasks.DetectCalibrationCard
import MF.V3.Tasks.DownloadProject
import MF.V3.Tasks.Export
import MF.V3.Tasks.ExportLogs
import MF.V3.Tasks.ExportMerge
import MF.V3.Tasks.FlattenGroup
import MF.V3.Tasks.ForgetWifi
import MF.V3.Tasks.HasCameras
import MF.V3.Tasks.HasProjector
import MF.V3.Tasks.HasTurntable
import MF.V3.Tasks.ListExportFormats
import MF.V3.Tasks.ListGroups
import MF.V3.Tasks.ListNetworkInterfaces
import MF.V3.Tasks.ListProjects
import MF.V3.Tasks.ListScans
import MF.V3.Tasks.ListSettings
import MF.V3.Tasks.ListWifi
import MF.V3.Tasks.Merge
import MF.V3.Tasks.MergeData
import MF.V3.Tasks.MoveGroup
import MF.V3.Tasks.NewGroup
import MF.V3.Tasks.NewProject
import MF.V3.Tasks.NewScan
import MF.V3.Tasks.OpenProject
import MF.V3.Tasks.PopSettings
import MF.V3.Tasks.PushSettings
import MF.V3.Tasks.Reboot
import MF.V3.Tasks.RemoveGroups
import MF.V3.Tasks.RemoveProjects
import MF.V3.Tasks.RestoreFactoryCalibration
import MF.V3.Tasks.RotateTurntable
import MF.V3.Tasks.ScanData
import MF.V3.Tasks.SetCameras
import MF.V3.Tasks.SetGroup
import MF.V3.Tasks.SetProject
import MF.V3.Tasks.SetProjector
import MF.V3.Tasks.Shutdown
import MF.V3.Tasks.SplitGroup
import MF.V3.Tasks.StartVideo
import MF.V3.Tasks.StopVideo
import MF.V3.Tasks.SystemInfo
import MF.V3.Tasks.TransformGroup
import MF.V3.Tasks.TurntableCalibration
import MF.V3.Tasks.UpdateSettings
import MF.V3.Tasks.UploadProject
import importlib
import inspect
import json
import threading
import three
import three.MF
import three.MF.V3
import three.MF.V3.Buffer
import three.MF.V3.Three
import three.serialization
import time
import types
import typing
import websocket
from typing import Optional, Callable, Any, Union, List


class Scanner:
    def __init__(self, OnTask: Optional[Callable[[MF.V3.Task.Task], None]] = None, OnMessage: Optional[Callable[[str], None]] = None, OnBuffer: Optional[Callable[[Any, bytes], None]] = None): ...
    def Connect(self, URI: str, timeoutSec=5) -> bool:
        """Attempts to connect to the scanner using the specified URI and timeout.

        Args:
            * URI (str): The URI of the websocket server.
            * timeoutSec (int): Timeout in seconds, default is 5.

        Returns:
            bool: True if connection is successful, raises Exception otherwise.

        Raises:
            Exception: If connection fails within the timeout or due to an error."""
        ...
    def Disconnect(self) -> None:
        """Close the websocket connection."""
        ...
    def IsConnected(self) -> bool:
        """Checks if the scanner is currently connected.

        Returns:
            bool: True if connected, False otherwise."""
        ...
    def SendTask(self, task, buffer: bytes = None) -> Any:
        """Sends a task to the scanner.
        Tasks are general control requests for the scanner. (eg. Camera exposure, or Get Image)

        Creates a task, serializes it, and sends it via the websocket.

        Args:
            * task (Task): The task to send.
            * buffer (bytes): The buffer data to send, default is None.

        Returns:
            Any: The task object that was sent.

        Raises:
            AssertionError: If the connection is not established."""
        ...
    def add_merge_to_project(self) -> MF.V3.Task.Task:
        """Add a merged scan to the current project."""
        ...
    def align(self, source: int, target: int, rough: MF.V3.Settings.Align.Align.Rough = None, fine: MF.V3.Settings.Align.Align.Fine = None) -> MF.V3.Task.Task:
        """Align two scan groups."""
        ...
    def auto_focus(self, applyAll: bool, cameras: List[MF.V3.Settings.AutoFocus.AutoFocus.Camera] = None) -> MF.V3.Task.Task:
        """Auto focus one or both cameras."""
        ...
    def bounding_box(self, selection: MF.V3.Settings.ScanSelection.ScanSelection, axisAligned: bool) -> MF.V3.Task.Task:
        """Get the bounding box of a set of scan groups."""
        ...
    def calibrate_cameras(self) -> MF.V3.Task.Task:
        """Calibrate the cameras."""
        ...
    def calibrate_turntable(self) -> MF.V3.Task.Task:
        """Calibrate the turntable."""
        ...
    def calibration_capture_targets(self) -> MF.V3.Task.Task:
        """Get the calibration capture target for each camera calibration capture."""
        ...
    def camera_calibration(self) -> MF.V3.Task.Task:
        """Get the camera calibration descriptor."""
        ...
    def close_project(self) -> MF.V3.Task.Task:
        """Close the current open project."""
        ...
    def connect_wifi(self, ssid: str, password: str) -> MF.V3.Task.Task:
        """Connect to a wifi network."""
        ...
    def depth_map(self, camera: MF.V3.Settings.Camera.Camera = None, projector: MF.V3.Settings.Projector.Projector = None, turntable: MF.V3.Settings.Turntable.Turntable = None, capture: MF.V3.Settings.Capture.Capture = None, processing: MF.V3.Settings.Scan.Scan.Processing = None) -> MF.V3.Task.Task:
        """Capture a depth map."""
        ...
    def detect_calibration_card(self, Input: int) -> MF.V3.Task.Task:
        """Detect the calibration card on one or both cameras."""
        ...
    def download_project(self, Input: int) -> MF.V3.Task.Task:
        """Download a project from the scanner."""
        ...
    def export(self, selection: MF.V3.Settings.ScanSelection.ScanSelection = None, texture: bool = None, merge: bool = None, format: MF.V3.Settings.Export.Export.Format = None, scale: float = None) -> MF.V3.Task.Task:
        """Export a group of scans."""
        ...
    def export_logs(self, Input: bool = None) -> MF.V3.Task.Task:
        """Export scanner logs."""
        ...
    def export_merge(self, selection: MF.V3.Settings.ScanSelection.ScanSelection = None, texture: bool = None, merge: bool = None, format: MF.V3.Settings.Export.Export.Format = None, scale: float = None) -> MF.V3.Task.Task:
        """Export a merged scan."""
        ...
    def flatten_group(self, Input: int) -> MF.V3.Task.Task:
        """Flatten a scan group such that it only consists of single scans."""
        ...
    def forget_wifi(self) -> MF.V3.Task.Task:
        """Forget all wifi connections."""
        ...
    def has_cameras(self) -> MF.V3.Task.Task:
        """Check if the scanner has working cameras."""
        ...
    def has_projector(self) -> MF.V3.Task.Task:
        """Check if the scanner has a working projector."""
        ...
    def has_turntable(self) -> MF.V3.Task.Task:
        """Check if the scanner is connected to a working turntable."""
        ...
    def list_export_formats(self) -> MF.V3.Task.Task:
        """List all export formats."""
        ...
    def list_groups(self) -> MF.V3.Task.Task:
        """List the scan groups in the current open project."""
        ...
    def list_network_interfaces(self) -> MF.V3.Task.Task:
        """List available wifi networks."""
        ...
    def list_projects(self) -> MF.V3.Task.Task:
        """List all projects."""
        ...
    def list_scans(self) -> MF.V3.Task.Task:
        """List the scans in the current open project."""
        ...
    def list_settings(self) -> MF.V3.Task.Task:
        """Get scanner settings."""
        ...
    def list_wifi(self) -> MF.V3.Task.Task:
        """List available wifi networks."""
        ...
    def merge(self, selection: MF.V3.Settings.ScanSelection.ScanSelection = None, remesh: MF.V3.Settings.Merge.Merge.Remesh = None, simplify: MF.V3.Settings.Merge.Merge.Simplify = None, texturize: bool = None) -> MF.V3.Task.Task:
        """Merge two or more scan groups."""
        ...
    def merge_data(self, index: int, mergeStep: MF.V3.Settings.ScanData.ScanData.MergeStep = None, buffers: List[MF.V3.Settings.ScanData.ScanData.Buffer] = None, metadata: List[MF.V3.Settings.ScanData.ScanData.Metadata] = None) -> MF.V3.Task.Task:
        """Download the raw scan data for the current merge process."""
        ...
    def move_group(self, Input: List[int] = None) -> MF.V3.Task.Task:
        """Move a scan group."""
        ...
    def new_group(self, parentIndex: int = None, baseName: str = None, color: List[float] = None, visible: bool = None, collapsed: bool = None, rotation: List[float] = None, translation: List[float] = None) -> MF.V3.Task.Task:
        """Create a new scan group."""
        ...
    def new_project(self, Input: str = None) -> MF.V3.Task.Task:
        """Create a new project."""
        ...
    def new_scan(self, camera: MF.V3.Settings.Camera.Camera = None, projector: MF.V3.Settings.Projector.Projector = None, turntable: MF.V3.Settings.Turntable.Turntable = None, capture: MF.V3.Settings.Capture.Capture = None, processing: MF.V3.Settings.Scan.Scan.Processing = None) -> MF.V3.Task.Task:
        """Capture a new scan."""
        ...
    def open_project(self, Input: int) -> MF.V3.Task.Task:
        """Open an existing project."""
        ...
    def pop_settings(self, Input: bool = None) -> MF.V3.Task.Task:
        """Pop and restore scanner settings from the settings stack."""
        ...
    def push_settings(self) -> MF.V3.Task.Task:
        """Push the current scanner settings to the settings stack."""
        ...
    def reboot(self) -> MF.V3.Task.Task:
        """Reboot the scanner."""
        ...
    def remove_groups(self, Input: List[int] = None) -> MF.V3.Task.Task:
        """Remove selected scan groups."""
        ...
    def remove_projects(self, Input: List[int] = None) -> MF.V3.Task.Task:
        """Remove selected projects."""
        ...
    def restore_factory_calibration(self) -> MF.V3.Task.Task:
        """Restore factory calibration."""
        ...
    def rotate_turntable(self, Input: int) -> MF.V3.Task.Task:
        """Rotate the turntable."""
        ...
    def scan_data(self, index: int, mergeStep: MF.V3.Settings.ScanData.ScanData.MergeStep = None, buffers: List[MF.V3.Settings.ScanData.ScanData.Buffer] = None, metadata: List[MF.V3.Settings.ScanData.ScanData.Metadata] = None) -> MF.V3.Task.Task:
        """Download the raw scan data for a scan in the current open project."""
        ...
    def set_cameras(self, selection: List[int] = None, autoExposure: bool = None, exposure: int = None, analogGain: float = None, digitalGain: int = None, focus: int = None) -> MF.V3.Task.Task:
        """Apply camera settings to one or both cameras."""
        ...
    def set_group(self, index: int, name: str = None, color: List[float] = None, visible: bool = None, collapsed: bool = None, rotation: List[float] = None, translation: List[float] = None) -> MF.V3.Task.Task:
        """Set scan group properties."""
        ...
    def set_project(self, index: int = None, name: str = None) -> MF.V3.Task.Task:
        """Apply settings to the current open project."""
        ...
    def set_projector(self, on: bool = None, brightness: float = None, pattern: MF.V3.Settings.Projector.Projector.Pattern = None, image: MF.V3.Settings.Projector.Projector.Image = None, color: List[float] = None, buffer: bytes = None) -> MF.V3.Task.Task:
        """Apply projector settings."""
        ...
    def shutdown(self) -> MF.V3.Task.Task:
        """Shutdown the scanner."""
        ...
    def split_group(self, Input: int) -> MF.V3.Task.Task:
        """Split a scan group (ie. move its subgroups to its parent group)."""
        ...
    def start_video(self) -> MF.V3.Task.Task:
        """Start the video stream."""
        ...
    def stop_video(self) -> MF.V3.Task.Task:
        """Stop the video stream."""
        ...
    def system_info(self, updateMajor: bool = None, updateNightly: bool = None) -> MF.V3.Task.Task:
        """Get system information."""
        ...
    def transform_group(self, index: int, name: str = None, color: List[float] = None, visible: bool = None, collapsed: bool = None, rotation: List[float] = None, translation: List[float] = None) -> MF.V3.Task.Task:
        """Apply a rigid transformation to a group."""
        ...
    def turntable_calibration(self) -> MF.V3.Task.Task:
        """Get the turntable calibration descriptor."""
        ...
    def update_settings(self, advanced: MF.V3.Settings.Advanced.Advanced = None, camera: MF.V3.Settings.Camera.Camera = None, capture: MF.V3.Settings.Capture.Capture = None, i18n: MF.V3.Settings.I18n.I18n = None, projector: MF.V3.Settings.Projector.Projector = None, style: MF.V3.Settings.Style.Style = None, turntable: MF.V3.Settings.Turntable.Turntable = None, tutorials: MF.V3.Settings.Tutorials.Tutorials = None, viewer: MF.V3.Settings.Viewer.Viewer = None, software: MF.V3.Settings.Software.Software = None) -> MF.V3.Task.Task:
        """Update scanner settings."""
        ...
    def upload_project(self, buffer: bytes) -> MF.V3.Task.Task:
        """Upload a project to the scanner."""
        ...