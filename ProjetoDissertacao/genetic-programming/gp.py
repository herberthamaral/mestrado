import random

fmap = {
    '+': lambda *args: sum(args),
    '-': lambda x,y: x-y,
    '*': lambda x,y: x*y,
    '/': lambda x,y: x/y,
}
def execute(ftree, kwargs={}):
    if type(ftree) in (int, float):
        return ftree
    if type(ftree) in (str, unicode):
        return kwargs[ftree]
    if len(ftree) in [0,1]:
        if kwargs:
            return kwargs.values()[0]
        return None if not ftree else ftree[0]

    f = ftree[0]
    fargs = [execute(arg, kwargs) for arg in ftree[1:]]
    return fmap[f](*fargs)

def gen_random_tree(args):
    if len(args) == 1:
        return args[0]
    tree = [random.choice(fmap.keys())]
    leafes = [args[0], gen_random_tree(args[1:])]
    random.shuffle(leafes)
    tree.extend(leafes)
    return tree
