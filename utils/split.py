def erraticity(sequence_properties):
    sequence, properties = sequence_properties
    return properties['movement'] - abs(properties['net_bias'])

def neutrality(sequence_properties):
    sequence, properties = sequence_properties
    return len(sequence[0]) - properties['total_bias'] - abs(properties['net_bias'])
