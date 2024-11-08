from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext as _
from rest_framework import serializers


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "username",
            "telefone",
            "nome",
            "avatar",
            "data_cadastro",
            "email_confirmado",
        )
        extra_kwargs = {"password": {"write_only": True}}


class AlterarPerfilSerializer(serializers.Serializer):
    nome = serializers.CharField(required=False)
    # Outros campos que você deseja permitir alteração


class CadastroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "username", "password", "telefone", "nome")

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"})

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            usuario = authenticate(
                request=self.context.get("request"), email=email, password=password
            )

            if usuario:
                if not usuario.email_confirmado:
                    raise serializers.ValidationError(
                        _("Email não confirmado. Por favor, ative sua conta.")
                    )

                data["usuario"] = usuario
                return data
            else:
                raise serializers.ValidationError(_("Email ou password inválidos."))
        else:
            raise serializers.ValidationError(_('Deve incluir "email" e "password".'))


class AtivacaoContaSerializer(serializers.Serializer):
    codigo = serializers.CharField()


class ResetSenhaSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerificarResetSenhaSerializer(serializers.Serializer):
    codigo = serializers.CharField()
    new_password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        validators=[validate_password],
    )


class AlterarEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerificarAlteracaoEmailSerializer(serializers.Serializer):
    codigo = serializers.CharField()
    novo_email = serializers.EmailField()


class AlterarSenhaSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )
    new_password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )


class SolicitarNovoCodigoAtivacaoSerializer(serializers.Serializer):
    email = serializers.EmailField()
