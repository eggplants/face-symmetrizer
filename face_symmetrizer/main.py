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
        print("[+]image:", filepath)
        if not os.path.exists(filepath):
            print("[!]not found.")
            continue
        f = FaceSym(filepath)
        print('[+]{} face(s) was detected.'.format(f.face_count))
        _save(f, args)


def _save(f: FaceSym, args: argparse.Namespace) -> None:
    image_names = (
        'left_cropped', 'left_cropped_inner', 'left_cropped_outer',
        'right_cropped', 'right_cropped_inner', 'right_cropped_outer')
    file, ext = os.path.splitext(f.image_location)
    if ext == '' or ext is None:
        ext = '.jpg'
    _, name = os.path.split(file)
    for face_id in range(f.face_count):
        print('[+]face:', face_id)
        ims = f.get_symmetrized_images(
            idx=face_id, show=args.show)
        for idx, im in enumerate(ims):
            savepath = os.path.join(
                args.outdir,
                '{}.face-{}.{}{}'.format(
                    name, face_id, image_names[idx], ext))
            if args.save:
                print("[+]save:", savepath)
                im.save(savepath)


if __name__ == '__main__':
    main()
