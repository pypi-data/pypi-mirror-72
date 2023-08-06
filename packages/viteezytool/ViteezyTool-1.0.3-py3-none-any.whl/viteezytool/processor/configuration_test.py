import yaml

with open(r"C:\Users\sande\PycharmProjects\ViteezyTool\viteezytool\resources\pills.yaml") as stream:
    try:
        pills = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
