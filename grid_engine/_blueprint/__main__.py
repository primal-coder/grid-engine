from ._grid_blueprint import *

import os

import IPython

import json

import argparse

parser = argparse.ArgumentParser(prog='blueprint')
parser.description = 'Generate a blueprint for a grid.'
parser.add_help = True
parser.usage = 'blueprint [-h] [-i] [-l path/to/grid.json] [-t[-ns noise scale, -no noise octaves, -nr noise roughness] [-r number of rows] [-c number of columns] [-s cell size] [-o path/to/grid.json] [-v]'

parser.add_argument('-i', '--interactive', action='store_true', help='Run an interactive session')
parser.add_argument('-l', '--load', dest='load', type=str, default=None, help='Load a grid from a file')
parser.add_argument('-t', '--terrain', action='store_true', help='Whether to generate terrain with the grid.')
parser.add_argument('-ns', '--noise-scale', dest='noise_scale', type=int, default=100, help='Noise scale')
parser.add_argument('-no', '--noise-octaves', dest='noise_octaves', type=int, default=6, help='Noise octaves')
parser.add_argument('-nr', '--noise-roughness', dest='noise_roughness', type=float, default=0.5, help='Noise roughness')
parser.add_argument('-r', '--rows', dest='rows',type=int, default=10, help='Number of rows in the grid')
parser.add_argument('-c', '--columns', dest='columns',type=int, default=10, help='Number of columns in the grid')
parser.add_argument('-s', '--size', dest='size',type=int, default=100, help='Size of each cell in the grid')
parser.add_argument('-o', '--output', dest='output',type=str, default='grid.json', help='Output file name')
parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')

args = parser.parse_args()

if not args.verbose:
    def print(*args):
        pass

if args.output is not None:
    if not isinstance(args.output, str) or not args.output.endswith('.json'):
        raise ValueError('Output file name must be a string ending with .json')
    if not os.listdir(f'{os.getcwd()}{os.sep}blueprint{os.sep}blueprints').count(args.output):
        args.output = f'{os.getcwd()}{os.sep}blueprint{os.sep}blueprints{os.sep}{args.output}'
    else:
        raise FileExistsError(f'File {args.output} already exists')
else:
    args.output = f'{os.getcwd()}{os.sep}src{os.sep}blueprint{os.sep}blueprints{os.sep}grid.json'

if not args.size or not args.columns or not args.rows:
    raise ValueError('Invalid cell size, row count or column count')

if args.interactive:
    print('Running interactive session')
    print('Generating grid blueprint')
    blueprint = BaseGridBlueprint(args.size, (args.rows*args.size, args.columns*args.size))

print(f'Generating grid with size {args.size} cells, {args.rows} rows and {args.columns} columns')
if args.terrain:
    print(f'Generating terrain with noise scale {args.noise_scale}, noise octaves {args.noise_octaves} and noise roughness {args.noise_roughness} ...')
    blueprint = TerrainGridBlueprint(args.size, (args.rows*args.size, args.columns*args.size), args.noise_scale, args.noise_octaves, args.noise_roughness)
else:
    blueprint = BaseGridBlueprint(args.size, (args.rows*args.size, args.columns*args.size))
print(f'Success! Grid generated. Total cells: {len(blueprint.cell_list)}')
if args.interactive:
    print('Starting interactive session ...')
    IPython.start_ipython(argv=['--no-banner'], user_ns={'blueprint': blueprint})
    print('Interactive session ended')
    print('Exiting')
    exit()    
print('Serializing grid ...')
data = blueprint.__json__()
print('Writing grid ...')
json.dump(data, open(args.output, 'w'), indent=4)
print(f'Grid written to {args.output}')
print('Success!')
        