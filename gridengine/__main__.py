import argparse as _argparse
import os as _os
import colorama as _colorama

_parser = _argparse.ArgumentParser(prog='grid')
_parser.description = 'Generate a visualized grid from a blueprint. For producing a blueprint, see the blueprint module.'
_parser.add_help = True

_parser.add_argument('-i', '--interactive', action='store_true', help='Run an interactive session')
_parser.add_argument('-b', '--blueprint', dest='blueprint', type=str, default=None, help='Load a blueprint from a file')
_parser.add_argument('--ascii', action='store_true', help='Print the grid as ascii')
_parser.add_argument('-l', '--load', dest='load', type=str, default=None, help='Load a grid from a file')
_parser.add_argument('-t', '--terrain', action='store_true', default=True, help='Whether to generate terrain with the grid.')
_parser.add_argument('-ns', '--noise-scale', dest='noise_scale', type=int, default=100, help='Noise scale')
_parser.add_argument('-no', '--noise-octaves', dest='noise_octaves', type=int, default=6, help='Noise octaves')
_parser.add_argument('-nr', '--noise-roughness', dest='noise_roughness', type=float, default=0.5, help='Noise roughness')
_parser.add_argument('-r', '--rows', dest='rows',type=int, default=10, help='Number of rows in the grid')
_parser.add_argument('-c', '--columns', dest='columns',type=int, default=10, help='Number of columns in the grid')
_parser.add_argument('-s', '--size', dest='size',type=int, default=100, help='Size of each cell in the grid')
_parser.add_argument('-S', '--save', dest='save', action='store_true', help='Save the grid object to a file')
_parser.add_argument('-T', '--type', dest='type', type=str, default='png', help='Type of file to save the grid as')
_parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')

_args = _parser.parse_args()

from ._blueprint import _grid_blueprint as Blueprint
from ._grid import *
from ._utility import *

terrain_grids = f'{_os.getcwd()}{_os.sep}src{_os.sep}grid{_os.sep}terrain_grids{_os.sep}'
grids = f'{_os.getcwd()}{_os.sep}src{_os.sep}grid{_os.sep}grids{_os.sep}'
blueprints = f'{_os.getcwd()}{_os.sep}src{_os.sep}grid{_os.sep}blueprint{_os.sep}blueprints{_os.sep}'
saves_dir = '/devel/fresh/envs/grid-engine/src/grid/saves/'

if not _args.verbose:
    def print(*args):
        pass
if not _args.size or not _args.columns or not _args.rows:
    raise ValueError('Invalid cell size, row count or column count')

if _args.blueprint is not None:
    if not _os.listdir(f'{blueprints}').count(f'{_args.blueprint}.pkl'):
        raise FileNotFoundError(f'File {_args.blueprint} does not exist')
    print(f'Loading blueprint from {_args.blueprint} ...')
    try:
        blueprint = Blueprint.load_blueprint(f'{blueprints}{_args.blueprint}.pkl',  Blueprint.TerrainGridBlueprint)
    except Exception:
        blueprint = Blueprint.load_blueprint(f'{blueprints}{_args.blueprint}.pkl',  Blueprint.BaseGridBlueprint)
    print('Success! Blueprint loaded.')
else:
    if _args.rows*_args.columns > 1000000:
        print(f'{_colorama.Fore.RED}WARNING{_colorama.Fore.RESET}: The provided parameters will generate a grid composed of {_colorama.Fore.LIGHTWHITE_EX}{round((_args.rows*_args.columns)/1000000, 1)} million{_colorama.Fore.RESET} cells. \nThis will consume a significant amount of memory/resources/time. \nIf your system has a limited amount of memory this could cause it to hang or even crash. \nIf you understand the risks, continue by pressing {_colorama.Fore.LIGHTGREEN_EX}ENTER{_colorama.Fore.RESET}. Otherwise, press {_colorama.Fore.LIGHTRED_EX}CTRL+C{_colorama.Fore.RESET} to exit.')
        input()
    print(f'Generating blueprint with cell size {_args.size}, {_args.rows} rows and {_args.columns} columns. Total_cells: {_args.rows*_args.columns} ...')
    blueprint = Blueprint.TerrainGridBlueprint(_args.size, (_args.columns*_args.size, _args.rows*_args.size), noise_scale=_args.noise_scale, noise_octaves=_args.noise_octaves, noise_roughness=_args.noise_roughness)
    print(f'Success! Blueprint generated. Dimensions: {blueprint.grid_dimensions}')

print('Building grid from blueprint ...')
grid = Grid(blueprint=blueprint, with_terrain=True)
print('Success! Grid generated.')

if _args.save:
    print('Pickling grid ...')
    save_grid(grid=grid)
    print('Success!')
    print('Pickling blueprint ...')
    Blueprint.save_blueprint(blueprint=blueprint)
    print('Success!')
    
if _args.ascii:
    print('Writing ascii to file ...')
    with open(f'{saves_dir}{grid.grid_id[-5:]}/grid.txt', 'w') as f:
        rows = []
        string = ''
        for row in grid.rows:
            for cell in row:
                string += cell.terrain_char
            rows.append(string)
            string = ''
        f.write('\n'.join(rows))
    print('Success!')
    
cdata = extract_cell_data(grid)
grid_id = grid.grid_id[-5:]
height = grid.blueprint.grid_height
width = grid.blueprint.grid_width
delete_grid(grid)
    
generate_images((width, height), cdata, _args.size, grid_id)
    

