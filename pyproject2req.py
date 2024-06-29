import toml

def transform_version(version):
    if version.startswith("^"):
        return f">={version[1:]},<{int(version[1:].split('.')[0]) + 1}.0.0"
    if version == "*":
        return ""
    return version

def sync_requirements():
    # Load pyproject.toml
    with open('pyproject.toml', 'r') as file:
        pyproject = toml.load(file)

    # Extract dependencies from pyproject.toml
    dependencies = pyproject.get('tool', {}).get('poetry', {}).get('dependencies', {})

    # Write dependencies to requirements.txt
    with open('requirements.txt', 'w') as file:
        for package, version in dependencies.items():
            if package != 'python':
                transformed_version = transform_version(version)
                if transformed_version:
                    file.write(f'{package} {transformed_version}\n')
                else:
                    file.write(f'{package}\n')

if __name__ == "__main__":
    sync_requirements()