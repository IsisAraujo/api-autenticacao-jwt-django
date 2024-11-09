import pytest
from django.contrib.auth import get_user_model

Usuario = get_user_model()


@pytest.mark.django_db
class TestUsuarioManager:
    def test_create_user(self):
        usuario = Usuario.objects.create_user(
            email="usuario@exemplo.com",
            password="senha123",
            nome="Usuario Teste",
            cpf="12345678901",
            celular="+5511999999999",
        )
        assert usuario.email == "usuario@exemplo.com"
        assert usuario.nome == "Usuario Teste"
        assert usuario.cpf == "12345678901"
        assert not usuario.is_staff
        assert not usuario.is_superuser
        assert usuario.is_active

    def test_create_user_sem_email(self):
        with pytest.raises(ValueError):
            Usuario.objects.create_user(
                email="", password="senha123", nome="Usuario Teste"
            )

    def test_create_superuser(self):
        admin = Usuario.objects.create_superuser(
            email="admin@exemplo.com",
            password="senha123",
            nome="Admin",
            cpf="98765432101",
            celular="+5511999999998",
        )
        assert admin.email == "admin@exemplo.com"
        assert admin.nome == "Admin"
        assert admin.cpf == "98765432101"
        assert admin.is_staff
        assert admin.is_superuser
        assert admin.is_active
