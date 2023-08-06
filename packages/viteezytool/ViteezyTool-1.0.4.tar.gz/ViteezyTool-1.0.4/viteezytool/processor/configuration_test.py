import yaml

with open(r"/viteezytool/resources/inventory.yaml") as stream:
    try:
        pills = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
