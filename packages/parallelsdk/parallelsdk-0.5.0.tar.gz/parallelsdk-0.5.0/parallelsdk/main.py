import os
import random
import numpy as np

from ParallelPyFrontend.parallelsdk.pllai_data_toolbox.data_toolbox import *
from ParallelPyFrontend.parallelsdk.pllai_data_toolbox.data_toolbox import *
from ParallelPyFrontend.parallelsdk.pllai_mp_toolbox.mp_toolbox import *
from ParallelPyFrontend.parallelsdk.pllai_mp_toolbox.mp_model import *
from ParallelPyFrontend.parallelsdk.pllai_routing_toolbox.routing_toolbox import *
from ParallelPyFrontend.parallelsdk.pllai_scheduling_toolbox.SchedulingModels.Employee import Employee
from ParallelPyFrontend.parallelsdk.pllai_scheduling_toolbox.SchedulingModels.Staff import Staff
from ParallelPyFrontend.parallelsdk.pllai_scheduling_toolbox.scheduling_toolbox import *
from ParallelPyFrontend.parallelsdk.client import *

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


def createVRPModel(vrp):
    np.random.seed(1)
    depot_loc = np.random.uniform(0.0, 10.0, size=(2,))
    vrp.AddDepot(depot_loc)
    delivery_loc = []
    for k in range(10):
        delivery = np.random.uniform(0.0, 10.0, size=(2,))
        delivery_loc.append(delivery)
        vrp.AddLocation(position=delivery, demand=random.randint(5, 10))

    # vrp.AddVehicle( name="vehicle_%d" %(1), load=0.0, capacity=300)
    for k in range(3):
        vrp.AddVehicle(name="vehicle_%d" % k, load=0.0, capacity=30)
    vrp.InferDistanceMatrix()
    return vrp


def createSchedulingModel(scheduler):
    model = scheduler.get_instance()
    team = Staff("Team", "575.123.4567", "TruckBest")
    mario = Employee("Mario", "M", "587.234.1543", "TruckBest", "Boston")
    john = Employee("John", "M", "878.232.5873", "TruckBest", "Boston")
    team.add_staff_member(mario, 100)
    team.add_staff_member(john, 100)
    team.add_shift_preference(1, 0, 10)
    model.set_schedule_num_days(5)
    model.set_shift_per_day(3)
    model.add_staff(team)


def createMPModel(model):
    inf = Infinity()
    x = model.IntVar(0.0, inf, 'x')
    y = model.IntVar(0.0, inf, 'y')
    # print(x)
    # print(y)
    c1 = model.Constraint(x + 7 * y <= 17.5)
    c2 = model.Constraint(x <= 3.5)
    model.Objective(x + 10 * y, maximize=True)


def createPythonFunctionTool(tool):
    python_fcn = tool.get_instance()
    python_fcn.add_entry_fcn_name("myFcn")
    python_fcn.add_entry_module_name("my_file")
    python_fcn.add_input_argument(3, "int")
    python_fcn.add_input_argument([3.14, 4.15], "double")
    #python_fcn.add_input_argument(3.14, "double")
    python_fcn.add_output_argument("double", False)
    python_fcn.add_output_argument("bool", True)

    # Add the path to the test folder
    path_str = str(os.path.join(os.path.dirname(__file__), "..", "test"))
    #path_str = "random_path"
    python_fcn.add_environment_path(path_str)
    return tool


def runConnection(optimizer):
    print("Connecting...")
    optimizer.connect()

    model = input("Run model [r(routing)/s(scheduling)/m(mp)/d(data)/n(none)]: ")
    if model == "n":
        pass
    elif model == "r":
        vrp = createVRPModel(BuildVRP('example'))
        optimizer.run_optimizer_synch(vrp)
        solution = vrp.get_solution()
        for route in solution:
            print("Route: " + str(route.get_route()))
            print("Total distance: " + str(route.get_total_distance()))
    elif model == "d":
        data_tool = createPythonFunctionTool(BuildPythonFunctionTool("fcn_tool"))
        optimizer.run_optimizer_synch(data_tool)
        output = data_tool.get_instance().get_output()
        print(output)
    else:
        pass

    val = input("Disconnect? [Y/n]: ")
    optimizer.disconnect()


def main():
    scheduler = BuildEmployeesScheduler('test')
    createSchedulingModel(scheduler)

    mp = MPModel('mip_example')
    createMPModel(mp)

    data_tool = BuildPythonFunctionTool("fcn_tool")
    createPythonFunctionTool(data_tool)

    print("Create a client...")
    optimizer = ParallelClient('127.0.0.1')
    val = input("Connect to back-end [Y/N]: ")
    if val == 'Y':
        runConnection(optimizer)


if __name__ == '__main__':
    main()
