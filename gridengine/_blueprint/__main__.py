from ._grid_blueprint import *

import os as _os

import IPython as _IPython

import json as _json

import argparse as _argparse

_parser = _argparse.ArgumentParser(prog='blueprint')
_parser.description = 'Generate a blueprint for a grid.'
_parser.add_help = True
_parser.usage = 'blueprint [-h] [-i] [-l path/to/grid._json] [-t[-ns noise scale, -no noise octaves, -nr noise roughness] [-r number of rows] [-c number of columns] [-s cell size] [-o path/to/grid._json] [-v]'

_parser.add_argument('-i', '--interactive', action='store_true', help='Run an interactive session')
_parser.add_argument('-l', '--load', dest='load', type=str, default=None, help='Load a grid from a file')
_parser.add_argument('-t', '--terrain', action='store_true', help='Whether to generate terrain with the grid.')
_parser.add_argument('-ns', '--noise-scale', dest='noise_scale', type=int, default=100, help='Noise scale')
_parser.add_argument('-no', '--noise-octaves', dest='noise_octaves', type=int, default=6, help='Noise octaves')
_parser.add_argument('-nr', '--noise-roughness', dest='noise_roughness', type=float, default=0.5, help='Noise roughness')
_parser.add_argument('-r', '--rows', dest='rows',type=int, default=10, help='Number of rows in the grid')
_parser.add_argument('-c', '--columns', dest='columns',type=int, default=10, help='Number of columns in the grid')
_parser.add_argument('-s', '--size', dest='size',type=int, default=100, help='Size of each cell in the grid')
_parser.add_argument('-o', '--output', dest='output',type=str, default='grid._json', help='Output file name')
_parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')

_args = _parser.parse_args()

if not _args.verbose:
    def print(*args):
        pass

if _args.output is not None:
    if not isinstance(_args.output, str) or not _args.output.endswith('._json'):
        raise ValueError('Output file name must be a string ending with ._json')
    if not _os.listdir(f'{_os.getcwd()}{_os.sep}blueprint{_os.sep}blueprints').count(_args.output):
        _args.output = f'{_os.getcwd()}{_os.sep}blueprint{_os.sep}blueprints{_os.sep}{_args.output}'
    else:
        raise FileExistsError(f'File {_args.output} already exists')
else:
    _args.output = f'{_os.getcwd()}{_os.sep}src{_os.sep}blueprint{_os.sep}blueprints{_os.sep}grid._json'

if not _args.size or not _args.columns or not _args.rows:
    raise ValueError('Invalid cell size, row count or column count')

if _args.interactive:
    print('Running interactive session')
    print('Generating grid blueprint')
    blueprint = BaseGridBlueprint(_args.size, (_args.rows*_args.size, _args.columns*_args.size))

print(f'Generating grid with size {_args.size} cells, {_args.rows} rows and {_args.columns} columns')
if _args.terrain:
    print(f'Generating terrain with noise scale {_args.noise_scale}, noise octaves {_args.noise_octaves} and noise roughness {_args.noise_roughness} ...')
    blueprint = TerrainGridBlueprint(_args.size, (_args.rows*_args.size, _args.columns*_args.size), _args.noise_scale, _args.noise_octaves, _args.noise_roughness)
else:
    blueprint = BaseGridBlueprint(_args.size, (_args.rows*_args.size, _args.columns*_args.size))
print(f'Success! Grid generated. Total cells: {len(blueprint.cell_list)}')
if _args.interactive:
    print('Starting interactive session ...')
    _IPython.start_ipython(argv=['--no-banner'], user_ns={'blueprint': blueprint})
    print('Interactive session ended')
    print('Exiting')
    exit()    
print('Serializing grid ...')
data = blueprint.__json__()
print('Writing grid ...')
_json.dump(data, open(_args.output, 'w'), indent=4)
print(f'Grid written to {_args.output}')
print('Success!')
        