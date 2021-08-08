import argparse
import os

from face_symmetrizer import FaceSym


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='fsym',
        description='Easy symmetrizer for an image contained face(s)',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('images', metavar='file', type=str, nargs='+',
                        help='input image files')
    parser.add_argument('--show', '-s',
                        action='store_true',
                        help="show images")
    parser.add_argument('--save',
                        action='store_true',
                        help="save images")

    parser.add_argument('--outdir', '-o',
                        default='.', type=str, metavar='dir',
                        help="output directory of image")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    for filepath in args.images:
        print("[+]", filepath)
        if not os.path.exists(filepath):
            print("[!]not found.")
            continue
        f = FaceSym(filepath)
        if args.save:
            _save(f, args)


def _save(f: FaceSym, args: argparse.Namespace) -> None:
    file, ext = os.path.splitext(f.image_location)
    if ext == '' or ext is None:
        ext = '.jpg'
    _, name = os.path.split(file)
    for face_id in range(f.face_count):
        ims = f.get_symmetrized_images(
            idx=face_id+1, show=args.show)
        for idx, im in enumerate(ims):
            savepath = os.path.join(
                args.outdir,
                '{}.face-{}.{}{}'.format(name, face_id, idx, ext))
            print("[+]save:", savepath)
            im.save(savepath)


if __name__ == '__main__':
    main()
