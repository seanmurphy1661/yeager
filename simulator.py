import argparse

from yconfig import yconfig

def main ():
    print("Initializing ----------------------------------------------")
    parser = argparse.ArgumentParser(
        prog='simulator',
        description='create data scenarios to verify tests',
        epilog='quality is job #1')
    parser.add_argument('filename')
    parser.add_argument('simulation')
    args = parser.parse_args()

    config = yconfig(args.filename)
    if not config.yaml_loaded:
        print(f"Configuration file {args.filename} could not be loaded.")
        return (1)

    if config.dump_config():
        config.dump_yaml(True)
        









    print("Done. -----------------------------------------------------")


if __name__ == "__main__":
    main()
