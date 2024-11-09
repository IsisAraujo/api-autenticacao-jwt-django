import os
import tempfile

from django.test import TestCase
from PIL import Image


class PerfilUsuarioTests(TestCase):
    def create_test_image(self):
        # Cria uma imagem temporária para teste
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            # Cria uma imagem simples usando PIL
            image = Image.new("RGB", (100, 100), color="red")
            image.save(f, "JPEG")
            return f.name

    def test_avatar_url(self):
        # Cria uma imagem de teste
        image_path = self.create_test_image()
        try:
            # Removido o 'as img' já que a variável não é utilizada
            with open(image_path, "rb"):

                pass
        finally:
            # Limpa o arquivo temporário
            os.unlink(image_path)
