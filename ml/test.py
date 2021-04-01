def process_data(data):
    lines = []
    for l in data.split('\n'):
        if l != '': lines.append(l)
    for i, v in enumerate(lines):
        values = [int(c) for c in v.split(',')]
        assert(len(values) == 15)
        lines[i] = values
    return lines

process_data('1,2,3,4,5,6,7,8,9,10,11,12,13,14,15\n1,2,3,4,5,6,7,8,9,10,11,12,13,14,15\n1,2,3,4,5,6,7,8,9,10,11,12,13,14,15\n')