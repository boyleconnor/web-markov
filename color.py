MAX_BIAS = 1.0
MIN_BIAS = -1.0


def rgb(bias):
    '''Convert a bias to an rgb value.
    
    Source: https://stackoverflow.com/a/20792531
    '''
    '''
    ratio = 2 * (bias - MIN_BIAS) / (MAX_BIAS - MIN_BIAS)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
    return r, g, b
    '''
    if bias >= 0.0:
        r = 255
        g = int(255*(1-bias))
        b = int(255*(1-bias))
    else:
        r = int(255*(1+bias))
        g = int(255*(1+bias))
        b = 255
    return r, g, b


def colored_text(sequence, biases):
    '''Convert the tokens in sequence to colored text based on the corresponding pass
    '''
    if len(sequence) != len(biases):
        raise ValueError("Sequence and biases must be of same length!")


    text = ''
    for token, bias in zip(sequence, biases):
        r, g, b = rgb(bias)
        text += "\x1b[38;2;%d;%d;%dm%s\x1b[0m" % (r, g, b, token)

    return text



if __name__ == '__main__':
    # Basic tests for text coloring
    sequence = ('This text ', 'should be ', 'red. ', 'This text ', 'should be ', 'blue.', ' Now, white!')
    biases = (0.25, 0.5, 1.0, -0.25, -0.5, -1.0, 0.0)
    print(colored_text(sequence, biases))
