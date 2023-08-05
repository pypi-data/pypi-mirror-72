from copy import copy
from random import shuffle

import pm4py.objects.log.log as log_instance
from pm4py.objects.petri import semantics

import time
import datetime
import deprecation

@deprecation.deprecated(deprecated_in='1.3.0', removed_in='2.0.0', current_version='',
                        details='pm4py.algo.simulation is deprecated; use pm4py.simulation entrypoint instead')
def apply_playout(net, initial_marking, no_traces=100, max_trace_length=100):
    """
    Do the playout of a Petrinet generating a log

    Parameters
    ----------
    net
        Petri net to play-out
    initial_marking
        Initial marking of the Petri net
    no_traces
        Number of traces to generate
    max_trace_length
        Maximum number of events per trace (do break)
    """
    # assigns to each event an increased timestamp from 1970
    curr_timestamp = 10000000
    log = log_instance.EventLog()
    for i in range(no_traces):
        trace = log_instance.Trace()
        trace.attributes["concept:name"] = str(i)
        marking = copy(initial_marking)
        for j in range(100000):
            if not semantics.enabled_transitions(net, marking):
                break
            all_enabled_trans = semantics.enabled_transitions(net, marking)
            all_enabled_trans = list(all_enabled_trans)
            shuffle(all_enabled_trans)
            trans = all_enabled_trans[0]
            if trans.label is not None:
                event = log_instance.Event()
                event["concept:name"] = trans.label
                event["time:timestamp"] = datetime.datetime.fromtimestamp(curr_timestamp)
                trace.append(event)
                # increases by 1 second
                curr_timestamp = curr_timestamp + 1
            marking = semantics.execute(trans, net, marking)
            if len(trace) > max_trace_length:
                break
        if len(trace) > 0:
            log.append(trace)
    return log


def apply(net, initial_marking, parameters=None):
    """
    Do the playout of a Petrinet generating a log

    Parameters
    -----------
    net
        Petri net to play-out
    initial_marking
        Initial marking of the Petri net
    parameters
        Parameters of the algorithm:
            noTraces -> Number of traces of the log to generate
            maxTraceLength -> Maximum trace length
    """
    if parameters is None:
        parameters = {}
    no_traces = 100
    max_trace_length = 100
    if "noTraces" in parameters:
        no_traces = parameters["noTraces"]
    if "maxTraceLength" in parameters:
        max_trace_length = parameters["maxTraceLength"]

    return apply_playout(net, initial_marking, max_trace_length=max_trace_length, no_traces=no_traces)
