import yaml

 # filename is the name of the configuration file
        # see inputfile for name of file being tested
def main():
    print("Initializing ----------------------------------------------")
    
    filename = './config/cms_puf.yaml'
    yaml_loaded = False
    yaml_raw = ""
    try:
        with open(filename,"r") as stream:
            try:
                yaml_raw = yaml.safe_load(stream)
                yaml_loaded = True
                print("Loaded  ---------------------------------------------------")
            except yaml.YAMLError as exc:
                print(exc)
    except FileNotFoundError as exc:
        print(exc)

    if yaml_loaded != True :
        print(f"file was not loaded")
        return (1)
    
    #print(f"{yaml_raw}")
    if 'input_filename' not in yaml_raw:
        print(f"input_filename is a required setting")
    #
    # file type is reqired and csv is the only option
    #
    if 'input_filetype' not in yaml_raw:
        print(f"input_filetype is required")
        if yaml_raw['input_filetype'] != 'csv':
            print(f"only csv file type is supported")
    #
    #   column delimiter
    #
    if 'column_delimiter' not in yaml_raw:
        print(f"column delimiter reqired")
    #
    #   stats section edits
    #
    if 'stats' in yaml_raw:
        if 'enabled' not in yaml_raw['stats']:
            print(f"enabled not found ")
        if 'file' not in yaml_raw['stats']:
            print(f"stats file required")
        if 'report' not in yaml_raw['stats']:
            print(f"report name required")
    else:
        print(f"stats section not present")
    #
    #   options section edits
    #
    if 'options' not in yaml_raw:
        print(f"options are required")
        
    print("Done ------------------------------------------------------")

if __name__ == "__main__":
    main()