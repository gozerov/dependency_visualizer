import json
import subprocess
from typing import Dict, Set

class DependencyVisualizer:
    def __init__(self, config_path: str):
        self.config = self.load_config(config_path)
        self.package = self.config['package']
        self.max_depth = self.config['max_depth']
        self.output_path = self.config['output_path']
        self.dependencies = set()

    def load_config(self, path: str) -> Dict:
        with open(path, 'r') as f:
            return json.load(f)

    def get_dependencies(self, package: str, depth: int) -> Set[str]:
        if depth > self.max_depth:
            return set()

        result = subprocess.run(['brew', 'info', '--json=v1', package], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8')

        if not output.strip():
            raise ValueError(f"Package '{package}' not found or no data returned in JSON format")

        try:
            package_info = json.loads(output)[0]  # Мы уверены, что пакет будет первым элементом
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON for package '{package}': {e}")

        deps = set()

        if 'dependencies' in package_info:
            for dep in package_info['dependencies']:
                if dep not in self.dependencies:
                    deps.add(dep)
                    self.dependencies.add(dep)
                    deps.update(self.get_dependencies(dep, depth + 1))

        return deps

    def generate_mermaid_graph(self) -> str:
        graph = ["graph TD"]
        for dep in self.dependencies:
            graph.append(f"{self.package} --> {dep}")
        return "\n".join(graph)

    def save_output(self, content: str):
        with open(self.output_path, 'w') as f:
            f.write(content)

    def run(self):
        self.dependencies = self.get_dependencies(self.package, 0)
        graph = self.generate_mermaid_graph()
        print(graph)
        self.save_output(graph)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python dependency_visualizer.py <config_path>")
        sys.exit(1)

    config_path = sys.argv[1]
    visualizer = DependencyVisualizer(config_path)
    visualizer.run()
