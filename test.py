import unittest
from unittest.mock import patch, MagicMock
from dependency_visualizer import DependencyVisualizer

class TestDependencyVisualizer(unittest.TestCase):

    def test_load_config(self):
        visualizer = DependencyVisualizer('config.json')
        self.assertEqual(visualizer.package, 'curl')
        self.assertEqual(visualizer.max_depth, 2)

    @patch('subprocess.run')
    def test_get_dependencies(self, mock_subprocess):
        mock_subprocess.return_value = MagicMock(
            stdout=b'[{"name": "curl", "dependencies": ["brotli", "libnghttp2", "libssh2", "openssl@3", "rtmpdump", "zstd"]}]')
        visualizer = DependencyVisualizer('config.json')
        deps = visualizer.get_dependencies('curl', 0)
        self.assertEqual(deps, {'brotli', 'libnghttp2', 'libssh2', 'openssl@3', 'rtmpdump', 'zstd'})

    def test_generate_mermaid_graph(self):
        visualizer = DependencyVisualizer('config.json')
        visualizer.dependencies = {'libcurl4', 'libc6'}
        graph = visualizer.generate_mermaid_graph()
        expected_graph = "graph TD\ncurl --> libcurl4\ncurl --> libc6"
        self.assertEqual(graph, expected_graph)


if __name__ == '__main__':
    unittest.main()
