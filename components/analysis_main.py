from analyzer_interface import AnalyzerInterface
from storage import Project, Storage
from terminal_tools import (draw_box, open_directory_explorer, prompts,
                            wait_for_key)
from terminal_tools.inception import TerminalContext

from .analysis_web_server import analysis_web_server
from .export_outputs import export_outputs


def analysis_main(context: TerminalContext, storage: Storage, project: Project, analyzer: AnalyzerInterface):
  while True:
    with context.nest(draw_box(f"Analysis: {analyzer.name}", padding_lines=0)):
      action = prompts.list_input(
        "What would you like to do?",
        choices=[
          ("Open output directory", "open_output_dir"),
          ("Export outputs", "export_output"),
          ("Launch Web Server", "web_server"),
          ("(Back)", None),
        ],
      )

    if action is None:
      return

    if action == "open_output_dir":
      print("Starting file explorer")
      open_directory_explorer(
        storage._get_project_exports_root_path(project.id, analyzer.id)
      )
      wait_for_key(True)
      continue

    if action == "export_output":
      export_outputs(context, storage, project, analyzer)
      continue

    if action == "web_server":
      analysis_web_server(context, storage, project, analyzer)
      continue
