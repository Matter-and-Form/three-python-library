from MF.V3.Tasks.SetProjector import SetProjector, Projector
from MF.V3 import Task
from typing import List

def set_projector(scanner, on: bool, brightness: float, color: list) -> Task:
    """
    Sets the projector settings.

    Args:
        * on (bool): True to turn the projector on, False to turn it off.
        * brightness (float): The brightness of the projector, between 0.0 and 1.0.
        * color ([float]): The RGB color of the projector, as a list of three floats between 0.0 and 1.0.

    Returns:
        Task: The task object that was sent.
    """
    set_projector_request = SetProjector.Request(
        Index=0,
        Type="SetProjector",
        Input=Projector(on=on, brightness=brightness, color=color)
    )
    set_projector_response = SetProjector.Response(
        Index=0,
        Type="SetProjector"
    )
    
    task = Task(Index=0, Type="SetProjector", Input=set_projector_request, Output=set_projector_response)

    scanner.SendTask(task)
    
    return task