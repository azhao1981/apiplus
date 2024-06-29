import toml

def reverse_transform_version(version):
    if version.startswith(">=") and "," in version:
        lower_bound = version.split(",")[0].replace(">=", "")
        upper_bound = version.split(",")[1].split("<")[1]
        major_version = int(lower_bound.split('.')[0])
        if int(upper_bound.split('.')[0]) == major_version + 1:
            return f"^{lower_bound}"
    return version

def reverse_sync_requirements():
    # Load requirements.txt
    with open('requirements.txt', 'r') as file:
        requirements = file.readlines()

    dependencies = {}

    # Parse requirements.txt
    for line in requirements:
        if ' ' in line:
            package, version = line.strip().split(' ', 1)
            dependencies[package] = reverse_transform_version(version)
        else:
            package = line.strip()
            dependencies[package] = "*"

    # Load pyproject.toml
    with open('pyproject.toml', 'r') as file:
        pyproject = toml.load(file)

    # Update dependencies in pyproject.toml
    pyproject['tool']['poetry']['dependencies'] = dependencies

    # Write updated pyproject.toml
    with open('pyproject.toml', 'w') as file:
        toml.dump(pyproject, file)

if __name__ == "__main__":
    reverse_sync_requirements()
