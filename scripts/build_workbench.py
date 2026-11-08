import argparse
from pathlib import Path
import subprocess
import sys

from encode_workbench import encode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--blender', default='blender')
    parser.add_argument('--refresh', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if args.refresh:
        subprocess.run([sys.executable, str(root/'scripts/refresh_activity.py')], check=True)
    variants = [('dark',1120,False),('light',1120,False),('mobile-dark',720,True),('mobile-light',720,True)]
    for name, width, mobile in variants:
        frames = root/'.render'/name
        command = [args.blender,'--background','--python',str(root/'scripts/render_workbench.py'),
                   '--','--out',str(frames),'--width',str(width),'--theme','dark' if 'dark' in name else 'light']
        if mobile:
            command.append('--mobile')
        subprocess.run(command, check=True)
        encode(frames, root/'assets'/f'workbench-{name}.webp')


if __name__ == '__main__':
    main()
