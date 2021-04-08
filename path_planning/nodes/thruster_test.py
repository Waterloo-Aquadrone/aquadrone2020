#!/usr/bin/env python3.8

import rospy

from path_planning.states.waiting_state import WaitingState
from path_planning.states.thruster_test_state import ThrusterTestState
from path_planning.states.exit_code_state import ExitCodeState
from path_planning.state_machines.sequential_state_machine import SequentialStateMachine
from path_planning.state_executor import StateExecutor
from path_planning.state_tree import Tree


if __name__ == "__main__":
    rospy.init_node("thruster_test")

    machine = SequentialStateMachine('thruster_test', [WaitingState(20),
                                                       ThrusterTestState(thruster_count=8,
                                                                         thrust_amplitude=8, thrust_period=5),
                                                       WaitingState(10)])

    Tree.create_flowchart(machine, 'thruster-test')
    executor = StateExecutor(machine, rate=rospy.Rate(5))
    executor.run()
