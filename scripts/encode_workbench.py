import argparse
from pathlib import Path

from PIL import Image


def encode(source, target, fps=24):
    files = sorted(source.glob('[0-9][0-9][0-9][0-9].png'))
    if len(files) != 288:
        raise ValueError(f'Expected 288 frames in {source}, found {len(files)}.')
    frames = [Image.open(file).convert('RGBA') for file in files]
    durations = [round((i+1)*1000/fps)-round(i*1000/fps) for i in range(len(frames))]
    target.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(target, save_all=True, append_images=frames[1:], duration=durations,
                   loop=0, format='WEBP', quality=90, method=4, minimize_size=True)
    frames[132].save(target.with_name(target.stem+'-still.webp'), format='WEBP', lossless=True, exact=True, method=3)
    frames[132].save(target.with_suffix('.png'), optimize=True)
    with Image.open(target) as image:
        if image.n_frames < 2 or image.convert('RGBA').getchannel('A').getextrema()[0] != 0:
            raise ValueError('Output must be animated and transparent.')
    print(f'{target.name}: {target.stat().st_size/1024:.0f} KiB, 12 s, {len(frames)} frames')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('target', type=Path)
    args = parser.parse_args()
    encode(args.source, args.target)
