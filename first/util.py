def lines(File):
    for line in File: yield line
    yield '\n'

def blocks(File):
    block = []
    for line in lines(File):
        if line.strip():
            block.append(line)
        elif block:
            yield ''.join(block).strip()
            block = []
