

from enum import Enum

class V3Task(str, Enum):

    """Create a new test scan"""
    NewTestScan = 'NewTestScan',

    """Download a file from the server workspace"""
    DownloadFile = 'DownloadFile',




    """Get filesystem capacity and availability""" 
    DiskSpace = 'DiskSpace',

    """Software installed version."""
    SoftwareVersionInstalled = 'SoftwareVersionInstalled',

    """Software available version""" 
    SoftwareVersionAvailable = 'SoftwareVersionAvailable',

    """Get a still image from each camera""" 
    StillImage = 'StillImage',

    """Get a stream image from each camera""" 
    StreamImage = 'StreamImage',

    """Get the camera calibration descriptor for the current focus values""" 
    CameraCalibration = 'CameraCalibration',

    """Get the turntable calibration descriptor""" 
    TurntableCalibration = 'TurntableCalibration',

    """Get the camera calibration capture targets""" 
    CalibrationCaptureTargets = 'CalibrationCaptureTargets',

    """Calibrate cameras""" 
    CalibrateCameras = 'CalibrateCameras',

    """Calibrate turntable""" 
    CalibrateTurntable = 'CalibrateTurntable',

    """Start video stream""" 
    StartVideo = 'StartVideo',

    """Stop video stream""" 
    StopVideo = 'StopVideo',

    """Apply camera settings cameras""" 
    SetCameras = 'SetCameras',

    """Apply projector settings""" 
    SetProjector = 'SetProjector',

    """Check if the server can connect to cameras""" 
    HasCameras = 'HasCameras',

    """Check if the server can connect to a projector""" 
    HasProjector = 'HasProjector',

    """Check if the server can connect to a turntable""" 
    HasTurntable = 'HasTurntable',

    """Auto focus the cameras""" 
    AutoFocus = 'AutoFocus',

    """Rotate the turntable""" 
    RotateTurntable = 'RotateTurntable',

    """Detect the calibration card""" 
    DetectCalibrationCard = 'DetectCalibrationCard',

    """Get the set of projects in the workspace""" 
    ListProjects = 'ListProjects',

    """Download a project from the scanner""" 
    DownloadProject = 'DownloadProject',

    """Upload a project to the scanner""" 
    UploadProject = 'UploadProject',

    """Set project properties""" 
    SetProject = 'SetProject',

    """Create a new project""" 
    NewProject = 'NewProject',

    """Open an existing project""" 
    OpenProject = 'OpenProject',

    """Close an opened project""" 
    CloseProject = 'CloseProject',

    """Remove selected projects from the workspace""" 
    RemoveProjects = 'RemoveProjects',

    """Clear the available project undo and redo actions""" 
    ClearProjectActions = 'ClearProjectActions',

    """List the available project undo and redo actions""" 
    ListProjectActions = 'ListProjectActions',

    """Undo a number of project actions""" 
    UndoProjectActions = 'UndoProjectActions',

    """Redo a number of project actions""" 
    RedoProjectActions = 'RedoProjectActions',

    """List the scans in the current project""" 
    ListScans = 'ListScans',

    """Get geometry data for a selected scan""" 
    ScanData = 'ScanData',

    """Capture and process a new scan""" 
    NewScan = 'NewScan',

    """List the groups in the current project.""" 
    ListGroups = 'ListGroups',

    """Set scan group properties.""" 
    SetGroup = 'SetGroup',

    """Create a scan group.""" 
    NewGroup = 'NewGroup',

    """Move a scan group.""" 
    MoveGroup = 'MoveGroup',

    """Flatten a scan group such that it only consists of single scans.""" 
    FlattenGroup = 'FlattenGroup',

    """Split a scan group (ie move its subgroups to its parent group).""" 
    SplitGroup = 'SplitGroup',

    """Remove scan groups.""" 
    RemoveGroups = 'RemoveGroups',

    """Apply a rigid transformation to a group.""" 
    TransformGroup = 'TransformGroup',

    """Get the bounding box of a set of scan groups.""" 
    BoundingBox = 'BoundingBox',

    """Align two scan groups.""" 
    Align = 'Align',

    """Align two scan groups.""" 
    Merge = 'Merge',

    """Get geometry data for a the current merged scan.""" 
    MergeData = 'MergeData',

    """Add a merged scan to the current project.""" 
    AddMergeToProject = 'AddMergeToProject',

    """List export formats and their supported geometry elements.""" 
    ListExportFormats = 'ListExportFormats',

    """Export a group of scan.""" 
    Export = 'Export',

    """Export a merged scan.""" 
    ExportMerge = 'ExportMerge',

    """Export a backend logs.""" 
    ExportLogs = 'ExportLogs',

    """Get the global settings.""" 
    ListSettings = 'ListSettings',

    """Get the global settings.""" 
    PushSettings = 'PushSettings',

    """Get the global settings.""" 
    PopSettings = 'PopSettings',

    """Save the global settings.""" 
    UpdateSettings = 'UpdateSettings',

    """Reboot the scanner."""
    Reboot = 'Reboot',

    """Shutdown the scanner.""" 
    Shutdown = 'Shutdown',

    """List the available Wifi networks.""" 
    ListWifi = 'ListWifi',

    """Connect to a specific Wifi network.""" 
    ConnectWifi = 'ConnectWifi',

    """Query the access point status.""" 
    AccessPointStatus = 'AccessPointStatus',

    """List the network interfaces.""" 
    ListNetworkInterfaces = 'ListNetworkInterfaces',

    """Remove Vertices.""" 
    RemoveVertices = 'RemoveVertices',

    """Disable ethernet connection.""" 
    DisableEthernet = 'DisableEthernet',

    """Disable wifi connection.""" 
    DisableWifi = 'DisableWifi',

    """Forget wifi connection."""
    ForgetWifi = 'ForgetWifi' 
