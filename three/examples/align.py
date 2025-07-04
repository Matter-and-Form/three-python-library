#!/usr/bin/env python3
"""
Quick script to connect to MF THREE scanner, open a project, and run alignment.
"""

from three.scanner import Scanner
from three.MF.V3 import Task, TaskState
from three.MF.V3.Settings.Align import Align
from three.MF.V3.Descriptors.Project import Project
import time

def main():
    # Callback functions for handling scanner events
    def on_task(task: Task):
        """Handle task updates (progress, completion, errors)"""
        if task.Progress:
            print(f"Task {task.Type} - Progress: {task.Progress.current}/{task.Progress.total}")
        elif task.State == TaskState.Completed.value:
            print(f"Task {task.Type} completed successfully")
        elif task.State == TaskState.Failed.value:
            print(f"Task {task.Type} failed: {task.Error}")

    def on_message(message):
        """Handle general system messages"""
        print(f"Message received: {message}")

    def on_buffer(descriptor, buffer_data):
        """Handle buffer data (images, scans, etc.)"""
        print(f"Buffer received: {descriptor.Size} bytes")

    # Create scanner instance
    scanner = Scanner(
        OnTask=on_task,
        OnMessage=on_message,
        OnBuffer=on_buffer
    )

    try:
        # Connect to scanner (replace with your scanner's IP if not using Zeroconf)
        print("Connecting to scanner...")
        scanner.Connect("ws://matterandform.local:8081", timeoutSec=10)
        print("Connected successfully!")

        # List available projects
        print("\nListing projects...")
        projects_task = scanner.list_projects()
        
        if projects_task.Error:
            print(f"Error listing projects: {projects_task.Error}")
            return

        if not projects_task.Output or len(projects_task.Output) == 0:
            print("No projects found. Please create a project first.")
            return

        # Display available projects
        print("Available projects:")
        for i, project_data in enumerate(projects_task.Output):
            project = Project.Brief(**project_data)
            print(f"  {i}: {project.name} (Index: {project.index})")

        # Select the first project (or modify to select a specific one)
        selected_project_index = 16
        selected_project = Project.Brief(**projects_task.Output[selected_project_index])
        print(f"\nSelected project: {selected_project.name}")

        # Open the selected project
        print("Opening project...")
        open_task = scanner.open_project(selected_project.index)
        
        if open_task.Error:
            print(f"Error opening project: {open_task.Error}")
            return

        print("Project opened successfully!")

        list_groups = scanner.list_groups()
        for i, group_data in enumerate(list_groups.Output['groups']):
            group = Project.Group(**group_data)
            print(f"Group {i}: {group.name} (Index: {group.index})")

        
        # Run alignment on the project
        print("Starting alignment...")
        align_task = scanner.align(19, 14, rough=Align.Rough(method=Align.Rough.Method.Ransac))
        
        if align_task.Error:
            print(f"Error running alignment: {align_task.Error}")
            return

        print("Alignment completed successfully!")

    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Clean up connection
        if scanner.IsConnected():
            print("Disconnecting...")
            scanner.Disconnect()
            print("Disconnected.")

if __name__ == "__main__":
    main()