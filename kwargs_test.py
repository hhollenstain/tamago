KWARGS = { 'pc': 'platform',
           'psn': 'platform',
           'xbox': 'platform',
           'comp': 'mode',
           'competitive': 'mode',
           'qp': 'mode',
           'quickplay': 'mode',
}

KWARGS_DEFAULT =

def kwarg_generator(kwargs_map, args):
    kwargs = {}
    for arg in args:
        if arg in kwargs_map:
            kwargs[kwargs_map[arg]] = arg
        if arg.isdigit()
            kwargs['top'] = arg

    if 'top' not in kwargs:
        kwargs['top'] =
    return kwargs


def test_kwargs(kwargs):
    print(kwargs['mode'])
    print(kwargs['platform'])



test_args=['qp', 'pc',]

kwargs = kwarg_generator(KWARGS, test_args)

test_kwargs(kwargs)
