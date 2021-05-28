def get_output_layers(net):
    """
        Arg:
            net: input Neural network
        return:
            Layer instances, and edges specify relationships between layers inputs and outputs.  Each network layer has unique integer id and unique string name inside its network. LayerId can store either layer name or layer id.  This class supports reference counting of its instances
    """
    layer_names = net.getLayerNames()

    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers