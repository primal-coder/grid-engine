saves_dir = '/devel/fresh/envs/grid-engine/src/grid/saves/'

def generate_images(dimensions, cdata, cell_size, grid_id, animate=False):
    print('Generating grid image ...')
    print('Importing pillow ...')
    from PIL import Image, ImageDraw, ImageFilter
    import random
    print('Preparing raw image ...')
    image = Image.new('RGB', dimensions, (255, 255, 255))
    draw = ImageDraw.Draw(image)
    print('Counting cells ...')
    total = len(cdata)
    print(f'Total cells: {total}')
    cells = cdata
    print('Shuffling cells ...')
    random.shuffle(cells)
    if animate:
        frames = []
        for count in range(0, total, 100):
            for cell in zip(range(100), cells[count:count+100]):
                print(f'Drawing cells {count+1}-{min(count+100, total)} ... {round(((count+100)/total)*100)}%', end='\r')
                x = cell[0]
                y = cell[1]
                color = cell[2]
                draw.rectangle((x, y, x+(cell_size), y+(cell_size)), fill=color)
                
            frames.append(image.copy())

        print('Saving grid animation ...')
        frames[0].save(f'{saves_dir}{grid_id}/grid.gif', format='GIF', append_images=frames[1:], save_all=True, duration=1, loop=0)
    else:
        for i, cell in enumerate(cells):
            print(f'Drawing cells {round((i/total)*100)}%', end='\r')
            x = cell[0]
            y = cell[1]
            color = cell[2]
            draw.rectangle((x, y, x+(cell_size), y+(cell_size)), fill=color)
        image = image.filter(ImageFilter.EMBOSS)
        print('Cells drawn.')
    print('Saving grid image ...')
    image.save(f'{saves_dir}{grid_id}/grid.png')
    print(f'Grid ID: {grid_id}')