import json, time
print("""
                  __ _                  _ _ _             
                 / _(_)                | (_) |            
  ___ ___  _ __ | |_ _  __ _    ___  __| |_| |_ ___  _ __ 
 / __/ _ \| '_ \|  _| |/ _` |  / _ \/ _` | | __/ _ \| '__|
| (_| (_) | | | | | | | (_| | |  __/ (_| | | || (_) | |   
 \___\___/|_| |_|_| |_|\__, |  \___|\__,_|_|\__\___/|_|   
                        __/ |                             
                       |___/""")
def main():
    config = {
        "modelname": input("Model Name: "),
        "iterations": int(input("Iterations: ")),
        "refreshrate": int(input("Refresh Rate: ")),
        "environment": input("Environment: "),
        "download": []
    }
    if  config['environment'] == "colab":
        print("press ENTER on empty line to finish")
        while config['environment'] == "colab":
            url = input("URL: ")
            if not url:
                break
            config["download"].append(url)


    def verify(VCvalue, VCcondition):
        if not VCcondition(VCvalue):
            print("""
Configuration Parameters:
    Iterations: 1 to 1000
    Refresh Rate: > 1
    Environment: 'local' or 'colab'
""")
            main()
    # region    VERIFICATION CONDITIONS
    verify((config['modelname']), lambda x: isinstance(x, str) and x != "")
    verify((config['iterations']), lambda x: isinstance(x, int) and 1 <= x <= 1000)
    verify((config['refreshrate']), lambda x: isinstance(x, int) and 1 <= x)
    verify((config['environment']), lambda x: isinstance(x, str) and x == "local" or x == "colab")
    # endregion

    with open("config.json", "w") as config_file:
        json.dump(config, config_file, indent=4)
main()



