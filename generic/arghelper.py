# v1.0.0
import os
import json
import argparse
from path import Path


class LoadFromJson(argparse.Action):
    def __call__(self, parser, namespace, filepath, option_string=None):
        with open(filepath) as f:
            data = json.load(f)
            # XXX In current implementation, you cannot use store_true/false
            parse_str = []
            for k, v in data.items():
                if type(v[0]).__name__ == "list":
                    parser.add_argument(k, type=eval(v[1]), nargs="+")
                    parse_str.extend([k]+[str(x) for x in v[0]])
                else:
                    argtype = str if v[1] == "NoneType" else eval(v[1])
                    parser.add_argument(k, type=argtype, default=None)
                    if v[0] != "None":
                        parse_str.extend([k, v[0]])
            parser.add_argument('--cond_dir', type=str, default=None)
            parse_str.extend(['--cond_dir', os.path.dirname(filepath)])
            parser.parse_args(parse_str, namespace)
            setattr(namespace, self.dest, filepath)


def save_args_as_json(args, filepath):
    args_json = {}
    for k, v in vars(args).items():
        if k == "cond" or k == "cond_dir" or k == "args_save" or str(v) == "False" or str(v) == "None":
            continue
        if type(v).__name__ == "list":
            args_json["--{}".format(k)] = \
                [[str(x) for x in v], type(v[0]).__name__]
        else:
            args_json["--{}".format(k)] = [str(v), type(v).__name__]

    outdir = "./json"
    outfile = os.path.splitext(os.path.basename(filepath))[0] + ".json"
    outpath = os.path.join(outdir, outfile)

    if not os.path.isdir(outdir):
        Path(outdir).makedirs_p()

    if os.path.isfile(outpath):
        with open(outpath, "w", encoding="utf-8") as f:
            json.dump(args_json, f, indent=4)
    else:
        with open(outpath, "x", encoding="utf-8") as f:
            json.dump(args_json, f, indent=4)

    return "args is saved to \"{}\"".format(outpath)

