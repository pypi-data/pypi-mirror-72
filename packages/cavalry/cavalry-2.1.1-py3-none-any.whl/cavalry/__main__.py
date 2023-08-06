import argparse, os.path, cavalry


def main():

    path = os.path.dirname(__file__) + "/.secrets.json"

    parser = argparse.ArgumentParser(
        description="Utility to load environment variables. To persist the variables into your scope, run 'source cav {load,clear} [options]' or '. cav {load,clear} [options]'"
    )
    parser.add_argument(
        "-s",
        "--secrets",
        metavar="FILE",
        default=path,
        help="specify an alternate secrets file",
    )  # SECRETS should be set to wherever .secrets.json is located.

    subparsers = parser.add_subparsers(dest="action")
    store = subparsers.add_parser("store", help="store variables")
    delete = subparsers.add_parser("delete", help="delete variables")
    load = subparsers.add_parser("load", help="load variables")
    list = subparsers.add_parser("list", help="list stored data")
    clear = subparsers.add_parser("clear", help="clear variables from environment")

    store.add_argument("project", help="project to load")
    store.add_argument("key", help="variable name")
    store.add_argument("value", help="secret data")
    delete.add_argument("project", help="project to load")
    delete.add_argument("key", nargs="*", help="delete specific variables")

    load.add_argument("project", help="project to load")
    load.add_argument("var", nargs="*", help="load specific variables")
    clear.add_argument("project", help="project to load")
    clear.add_argument("var", nargs="*", help="clear specific variables")

    list.add_argument("project", nargs="?", help="project to load")

    args = parser.parse_args()

    secrets = cavalry.Secrets(args.secrets, create=True)

    if args.action == "store":
        secrets.store(args.project, args.key, args.value)
    elif args.action == "delete":
        secrets.delete(args.project, *args.key)
    elif args.action == "load":
        vars = secrets.load(args.project, *args.var)
        comp = [f"{k}={v}" for k, v in vars.items()]
        print(f"export {' '.join(comp)}")
    elif args.action == "list":
        if args.project:
            if not args.project in secrets.data:
                cavalry.errors.missing_project(args.project)

            for k, v in secrets.data[args.project].items():
                print(f"${k}={v}")
        else:
            for k in secrets.data.keys():
                print(k)
    elif args.action == "clear":
        vars = secrets.load(args.project, *args.var)
        comp = [f"{k}=" for k in vars.keys()]
        print(f"export {' '.join(comp)}")

    secrets.commit()


if __name__ == "__main__":
    main()
