import os
import re

from machetli import sas, tools

PLANNER_REPO = os.environ["DOWNWARD_REPO"]
PLANNER = os.path.join(PLANNER_REPO, "fast-downward.py")


def evaluate(state):
    with sas.temporary_file(state) as sas_filename:
        reference_command = [
            PLANNER, sas_filename, "--search", "astar(lmcut())", "--translate-options", "--relaxed",
        ]
        run_reference = tools.Run(
            reference_command, time_limit=20, memory_limit=3000)
        stdout, stderr, _ = run_reference.start()
        # with open("run1.log", "w") as log:
        #     log.write(stdout)
        # with open("run1.err", "w") as err:
        #     err.write(stderr)
        cost = tools.parse(stdout, r"Plan cost: (\d+)")

        mip_command = [
            PLANNER, sas_filename, "--search",
            "astar(operatorcounting([delete_relaxation_constraints("
            "use_time_vars=true, use_integer_vars=true)], "
            "use_integer_operator_counts=True), bound=0)",
        ]
        run_mip = tools.Run(
            mip_command, time_limit=20, memory_limit=3000)
        stdout, stderr, _ = run_mip.start()
        # with open("run2.log", "w") as log:
        #     log.write(stdout)
        # with open("run2.err", "w") as err:
        #     err.write(stderr)
        initial_h = tools.parse(stdout, r"Initial heuristic value .* (\d+)")

        if cost and initial_h:
            return cost != initial_h
        else:
            return False
