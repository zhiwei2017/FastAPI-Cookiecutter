from unittest import TestCase
from fastapi.testclient import TestClient
from {{cookiecutter.project_slug}}.app.application import create_application


class TestBaseEventHandler(TestCase):
    def test_startup_handler(self):
        app = create_application()
        with self.assertLogs('{{cookiecutter.project_slug}}', level='INFO') as cm:

            with TestClient(app):
                pass
            self.assertEqual(cm.output,
                             ['INFO:{{cookiecutter.project_slug}}:Starting up ...',
                              'INFO:{{cookiecutter.project_slug}}:Shutting down ...'])
