#!/usr/bin/env python3
# based on https://github.com/ros2/ros2cli/blob/master/ros2param/ros2param/verb/dump.py

import argparse
import os
import rclpy
import sys
import yaml


from rclpy.parameter import PARAMETER_SEPARATOR_STRING
from rcl_interfaces.srv import ListParameters

from ros2cli.node.strategy import add_arguments
from ros2cli.node.strategy import NodeStrategy
from ros2cli.node.direct import DirectNode

from ros2node.api import get_absolute_node_name
from ros2node.api import get_node_names
from ros2node.api import has_duplicates
from ros2node.api import NodeNameCompleter
from ros2node.api import parse_node_name

from ros2param.api import call_get_parameters
from ros2param.api import get_value

def get_node_dictionary(args):

    with NodeStrategy(args) as node:
        node_names = get_node_names(node=node, include_hidden_nodes=True)

    if node_names:
        nodes_dict = {n.full_name:n for n in node_names}

        sorted_names = sorted(n.full_name for n in node_names)
        if has_duplicates(sorted_names):
            print('WARNING: Be aware that are nodes in the graph that share an exact name, '
                  'this can have unintended side effects.', file=sys.stderr)
        return nodes_dict, sorted_names

    else:
        return None

def get_parameter_value(node, node_name, param):
    response = call_get_parameters(
        node=node, node_name=node_name,
        parameter_names=[param])

    # requested parameter not set
    if not response.values:
        return '# Parameter not set'

    # extract type specific value
    return get_value(parameter_value=response.values[0])

def insert_dict(dictionary, key, value):
    split = key.split(PARAMETER_SEPARATOR_STRING, 1)
    if len(split) > 1:
        if not split[0] in dictionary:
            dictionary[split[0]] = {}
        insert_dict(dictionary[split[0]], split[1], value)
    else:
        dictionary[key] = value

def get_dict(dictionary, parameter):

    if parameter in dictionary:
        return {parameter: dictionary[parameter]}, dictionary[parameter]
    else:
        for key, value in dictionary:
            if isinstance(value, dict):
                param_dict, param_value = get_dict(value, parameter)
                if param_dict:
                    return {key: param}, param_value
                else:
                    return None, None

    return None, None


def get_param_values(target_node, args):

    with DirectNode(args) as node:
        # create client
        service_name = f'{target_node.full_name}/list_parameters'
        client = node.create_client(ListParameters, service_name)

        try:
            client.wait_for_service(timeout_sec=args.timeout_sec)

            if not client.service_is_ready():
                print(f"Could not reach '{service_name}'")
                return None

            print(f"  Requesting parameters for {target_node.full_name} ...")
            request = ListParameters.Request()
            future = client.call_async(request)

            # wait for response
            rclpy.spin_until_future_complete(node, future, timeout_sec=args.timeout_sec)


            # retrieve values
            if future.result() is not None:
                params_dict = {'ros__parameters': {}}
                response = future.result()
                for param_name in sorted(response.result.names):
                    pval = get_parameter_value(node, target_node.full_name, param_name)
                    insert_dict(params_dict['ros__parameters'], param_name, pval)
                return params_dict
            else:
                e = future.exception()
                if e:
                    raise e
                else:
                    print(f"  Failed to retrieve parameters for {target_node.full_name} !")
                    return None

        except Exception as exc:
            print(f"Failed to retrieve parameters for {target_node.full_name} !")
            print("   ", exc)
            return None


def validate_parameter_for_all_nodes(parameters, parameter):
    values = {}
    values['Not found'] = []

    for full_node_name, node in nodes_dict.items():
        if full_node_name in parameters and isinstance(parameters[full_node_name], dict):
            if 'ros__parameters' in parameters[full_node_name]:
                param_dict, param_value = get_dict(parameters[full_node_name]['ros__parameters'], args.parameter)
                if param_dict:
                    if param_value not in values:
                        values[param_value] = {}
                    values[param_value][full_node_name] = param_dict
                else:
                    values['Not found'].append(full_node_name)
            else:
                values['Not found'].append(full_node_name)
        else:
            values['Not found'].append(full_node_name)
    return values

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Get all parameters for deployed system",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--hidden',
        action='store_false',
        default=True,
        help=('Suppress hidden nodes'))
    parser.add_argument(
        '--directory',
        default="~/.ros",
        help=('Target output directory'))
    parser.add_argument(
        '--file',
        default="parameters.yaml",
        help=('Output file name'))
    parser.add_argument(
        '--timeout_sec',
        default=2.0,
        type=float,
        help=('Timeout (seconds)'))
    parser.add_argument(
        '--parameter',
        default='',
        help=('Parameter to validate'))


    # parse the command line arguments
    print(">",sys.argv,"<")
    args = parser.parse_args()

    print(args)

    print("Get node names ...")
    nodes_dict, sorted_nodes = get_node_dictionary(args)

    print(20*"=", "Nodes", 20*"=")
    print(*sorted_nodes, sep='\n')

    parameters = {}
    cnt = 0
    missing_params = []

    print("Get parameters for all nodes ...")
    for full_node_name, node in nodes_dict.items():
        # cnt+=1
        # if cnt > 3:
        #     print("Limit to 4 nodes for testing!")
        #     break
        params = get_param_values(node, args)
        if params:
            parameters[full_node_name] = params
        else:
            missing_params.append(full_node_name)

    print(20*"=", "Parameters", 20*"=")
    print(yaml.dump(parameters, default_flow_style=False))

    print(20*"=", "Missing All Parameters", 20*"=")
    print("\n".join(missing_params))

    if args.parameter != '':
        print(15*"=", f"Validate {args.parameter}", 15*"=", "\n")
        values_map = validate_parameter_for_all_nodes(parameters, args.parameter)
        print(yaml.dump(values_map, default_flow_style=False))

    if args.file and args.file != "":
        target_dir = os.path.expanduser(args.directory)
        yaml_output_file = os.path.join(target_dir, args.file)
        print(f"Writing all parameters to {yaml_output_file} ...")
        with open(yaml_output_file, 'wt') as yaml_file:
            yaml.dump(parameters, yaml_file, default_flow_style=False)

    print("Done!")
