#!/usr/bin/env python3.8

import rospy
import rospkg
from matplotlib import pyplot as plt
from time import time

from path_planning.states.waiting_state import WaitingState
from path_planning.states.stabilize_state import StabilizeState
from path_planning.states.go_to_depth import GoToDepthState
from path_planning.states.exit_code_state import ExitCodeState
from path_planning.states.data_logger import DataLogger
from path_planning.state_machines.sequential_state_machine import SequentialStateMachine
from path_planning.state_machines.parallel_state_machine import ParallelStateMachine
from path_planning.state_executor import StateExecutor
from path_planning.state_tree import Tree


def plot_depth_data(data):
    directory = rospkg.RosPack().get_path('path_planning')
    plt.plot(data['t'], data['z'])
    plt.xlabel('Time (s)')
    plt.ylabel('Depth (m)')
    plt.title('Depth Versus Time')
    plt.savefig(directory + '/depth-control-' + str(time()) + '.png')


if __name__ == "__main__":
    rospy.init_node("dive_test")

    target_depth = -6  # m

    dive_machine = SequentialStateMachine('dive', [WaitingState(20), StabilizeState(),
                                                   GoToDepthState(target_depth, tolerance=0.05,
                                                                  velocity_tolerance=0.01),
                                                   WaitingState(10), GoToDepthState(0), WaitingState(10), ExitCodeState(0)])
    data_logger = DataLogger('dive-test')
    data_logger.add_data_post_processing_func(plot_depth_data)

    dive_logging_machine = ParallelStateMachine('dive_logger', states=[dive_machine],
                                                daemon_states=[data_logger])

    Tree.create_flowchart(dive_logging_machine, 'dive-test')
    executor = StateExecutor(dive_logging_machine, rate=rospy.Rate(5))
    executor.run()
