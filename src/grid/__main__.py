import argparse
import os
import IPython

parser = argparse.ArgumentParser(prog='grid')
parser.description = 'Generate a visualized grid from a blueprint. For producing a blueprint, see the blueprint module.'
parser.add_help = True

parser.add_argument('-i', '--interactive', action='store_true', help='Run an interactive session')
parser.add_argument('-b', '--blueprint', dest='blueprint', type=str, default=None, help='Load a blueprint from a file')
parser.add_argument('-l', '--load', dest='load', type=str, default=None, help='Load a grid from a file')
parser.add_argument('-t', '--terrain', action='store_true', default=True, help='Whether to generate terrain with the grid.')
parser.add_argument('-ns', '--noise-scale', dest='noise_scale', type=int, default=100, help='Noise scale')
parser.add_argument('-no', '--noise-octaves', dest='noise_octaves', type=int, default=6, help='Noise octaves')
parser.add_argument('-nr', '--noise-roughness', dest='noise_roughness', type=float, default=0.5, help='Noise roughness')
parser.add_argument('-r', '--rows', dest='rows',type=int, default=10, help='Number of rows in the grid')
parser.add_argument('-c', '--columns', dest='columns',type=int, default=10, help='Number of columns in the grid')
parser.add_argument('-s', '--size', dest='size',type=int, default=100, help='Size of each cell in the grid')
parser.add_argument('-S', '--save', dest='save', action='store_true', help='Save the grid object to a file')
parser.add_argument('-T', '--type', dest='type', type=str, default='png', help='Type of file to save the grid as')
parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')

args = parser.parse_args()

from .blueprint import *
from .grid import *

terrain_grids = f'{os.getcwd()}{os.sep}src{os.sep}grid{os.sep}terrain_grids{os.sep}'
grids = f'{os.getcwd()}{os.sep}src{os.sep}grid{os.sep}grids{os.sep}'
blueprints = f'{os.getcwd()}{os.sep}src{os.sep}grid{os.sep}blueprint{os.sep}blueprints{os.sep}'
saves_dir = '/devel/fresh/envs/grid-engine/src/grid/saves/'

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
    print(f'Generating blueprint with cell size {args.size}, {args.rows} rows and {args.columns} columns. Total_cells: {args.rows*args.columns} ...')
    blueprint = Blueprint.TerrainGridBlueprint(args.size, (args.columns*args.size, args.rows*args.size), noise_scale=args.noise_scale, noise_octaves=args.noise_octaves, noise_roughness=args.noise_roughness)
    print(f'Success! Blueprint generated. Dimensions: {blueprint.grid_dimensions}')

print('Building grid from blueprint ...')
grid = Grid(blueprint=blueprint, gen_terrain=True)
print('Success! Grid generated.')

if args.save:
    print('Saving grid ...')
    save_grid(grid=grid)
    print('Success!')
    print('Saving blueprint ...')
    Blueprint.save_blueprint(blueprint=blueprint)
    print('Success!')
    
print('Generating grid image ...')
print('Importing pillow ...')
from PIL import Image, ImageDraw
print('Success.')

print('Creating raw image ...')
image = Image.new('RGB', (grid.blueprint.grid_width, grid.blueprint.grid_height), (255, 255, 255))
print('Creating draw object ...')
draw = ImageDraw.Draw(image)
print('Drawing cells ...')
total = len(grid.cells.values())
for count, (cell, info) in enumerate(grid.blueprint.dictGrid.items(), start=1):
    print(f'Drawing cell {info["designation"]} ... {round((count/total)*100)}%', end='\r')
    x = info['coordinates'][0]
    y = info['coordinates'][1]
    color = grid.blueprint.dictTerrain[cell]['color']
    draw.rectangle((x, y, x+(args.size), y+(args.size)), fill=color)

# def capture_grid_as_image(grid: Grid, output_path: str):
#     window_width = grid.blueprint.grid_width
#     window_height = grid.blueprint.grid_height

#     # Create a larger window that can accommodate the entire grid
#     window = pyglet.window.Window(width=window_width, height=window_height)

#     @window.event
#     def on_draw():
#         window.clear()
#         grid.grid_batch.draw()

#         # Capture the grid as an image
#         image = pyglet.image.get_buffer_manager().get_color_buffer()
#         image.save(output_path)

#         # Close the window after capturing the image
#         pyglet.app.exit()

#     pyglet.app.run()

# Usage example
image.save(f'{saves_dir}{grid.grid_id[-5:]}/grid.png')

