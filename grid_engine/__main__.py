from grid_engine import Blueprint, Grid
import argparse
import os
import sys
import IPython
import colorama

print(f'{__name__} imported.')

print(f'{os.getcwd()}')

parser = argparse.ArgumentParser(prog='grid')
parser.description = 'Generate a visualized grid from a blueprint. For producing a blueprint, see the blueprint module.'
parser.add_help = True

parser.add_argument('-i', '--interactive', action='store_true', help='Run an interactive session')
parser.add_argument('-b', '--blueprint', dest='blueprint', type=str, default=None, help='Load a blueprint from a file')
parser.add_argument('--ascii', action='store_true', help='Print the grid as ascii')
parser.add_argument('-l', '--load', dest='load', type=str, default=None, help='Load a grid from a file')
parser.add_argument('-t', '--terrain', action='store_true', default=True, help='Whether to generate terrain with the grid.')
parser.add_argument('-ns', '--noise-scale', dest='noise_scale', type=int, default=455, help='Noise scale')
parser.add_argument('-no', '--noise-octaves', dest='noise_octaves', type=int, default=88, help='Noise octaves')
parser.add_argument('-nr', '--noise-roughness', dest='noise_roughness', type=float, default=0.63, help='Noise roughness')
parser.add_argument('-r', '--rows', dest='rows',type=int, default=768, help='Number of rows in the grid')
parser.add_argument('-c', '--columns', dest='columns',type=int, default=1280, help='Number of columns in the grid')
parser.add_argument('-s', '--size', dest='size',type=int, default=2, help='Size of each cell in the grid')
parser.add_argument('-S', '--save', dest='save', action='store_true', default=True, help='Save the grid object to a file')
parser.add_argument('-T', '--type', dest='type', type=str, default='png', help='Type of file to save the grid as')
parser.add_argument('-A', '--animate', dest='animate', action='store_true', default=True, help='Save the grid as an animated gif')
parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')

args = parser.parse_args()

saves_dir = f'{os.path.abspath(os.path.curdir)}grid_engine/_saves/'

if not args.verbose:
    def print(*args):
        pass
if not args.size or not args.columns or not args.rows:
    raise ValueError('Invalid cell size, row count or column count')

if args.blueprint is not None:
    if not os.listdir(f'{blueprints}').count(f'{args.blueprint}.pkl'):
        raise FileNotFoundError(f'File {args.blueprint} does not exist')
    print(f'Loading blueprint from {args.blueprint} ...')
    try:
        blueprint = Blueprint.load_blueprint(f'{blueprints}{args.blueprint}.pkl',  Blueprint.TerrainGridBlueprint)
    except Exception:
        blueprint = Blueprint.load_blueprint(f'{blueprints}{args.blueprint}.pkl',  Blueprint.BaseGridBlueprint)
    print('Success! Blueprint loaded.')
else:
    if args.rows*args.columns > 1000000:
        print(f'{colorama.Fore.RED}WARNING{colorama.Fore.RESET}: The provided parameters will generate a grid composed of {colorama.Fore.LIGHTWHITE_EX}{round((args.rows*args.columns)/1000000, 1)} million{colorama.Fore.RESET} cells. \nThis will consume a significant amount of memory/resources/time. \nIf you have limited amount of memory this could cause your system to hang or crash. \nIf you understand the risks, continue by pressing {colorama.Fore.LIGHTGREEN_EX}ENTER{colorama.Fore.RESET}. Otherwise, press {colorama.Fore.LIGHTRED_EX}CTRL+C{colorama.Fore.RESET} to exit.')
        input()
    print(f'Generating blueprint with cell size {args.size}, {args.rows} rows and {args.columns} columns. Total_cells: {args.rows*args.columns} ...')
    blueprint = Blueprint.TerrainGridBlueprint(cell_size=args.size, grid_dimensions=(args.columns*args.size, args.rows*args.size), noise_scale=args.noise_scale, noise_octaves=args.noise_octaves, noise_roughness=args.noise_roughness)
    print(f'Success! Blueprint generated. Dimensions: {blueprint.grid_dimensions}')

print('Building grid from blueprint ...')
grid = Grid.Grid(blueprint=blueprint, with_terrain=True)
print('Success! Grid generated.')

if args.save:
    print('Pickling grid ...')
    Grid.save_grid(grid=grid)
    print('Success!')
    print('Pickling blueprint ...')
    Blueprint.save_blueprint(blueprint=blueprint)
    print('Success!')
    
if args.ascii:
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
    
cdata = Grid.extract_cell_data(grid)
cell_size = grid.cell_size
grid_id = grid.grid_id[-5:]
height = grid.blueprint.grid_height
width = grid.blueprint.grid_width
del blueprint
del grid

from grid_engine import _utility as utility
    
utility.generate_images((width, height), cdata, cell_size, grid_id, animate=args.animate)
    

