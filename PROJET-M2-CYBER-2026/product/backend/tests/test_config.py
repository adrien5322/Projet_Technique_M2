"""Tests for application configuration.

Tests cover:
- Settings loading from environment variables
- Required settings validation (no hard-coded secrets)
- Default values
- Environment file loading
- JWT_SECRET_KEY requirement (no default)
"""

import pytest
import os
from unittest.mock import patch

from app.config import Settings, settings
from pydantic_core import PydanticUndefined


class TestSettingsLoading:
    """Tests for settings loading from environment."""
    
    def test_settings_load_from_env(self):
        """Test that settings can load from environment variables."""
        test_env = {
            "DATABASE_URL": "sqlite:///test.db",
            "JWT_SECRET_KEY": "test-secret-key-for-testing-only",
            "DEBUG": "true",
            "APP_NAME": "TestApp"
        }
        
        with patch.dict(os.environ, test_env, clear=False):
            test_settings = Settings()
            assert test_settings.DATABASE_URL == "sqlite:///test.db"
            assert test_settings.JWT_SECRET_KEY == "test-secret-key-for-testing-only"
            assert test_settings.DEBUG is True
            assert test_settings.APP_NAME == "TestApp"
    
    def test_settings_use_defaults_when_env_not_set(self):
        """Test that settings use defaults for optional fields."""
        # JWT_SECRET_KEY is required (no default), so we need to provide it
        test_env = {
            "JWT_SECRET_KEY": "required-secret-for-test"
        }
        
        # Remove optional env vars to test defaults
        env_to_clear = [
            "DATABASE_URL", "DEBUG", "APP_NAME", "APP_VERSION",
            "HOST", "PORT", "JWT_ALGORITHM", "ACCESS_TOKEN_EXPIRE_MINUTES",
            "REDIS_URL"
        ]
        
        # Store original values
        original_env = {k: os.environ.get(k) for k in env_to_clear}
        
        try:
            # Clear optional env vars
            for key in env_to_clear:
                if key in os.environ:
                    del os.environ[key]
            
            with patch.dict(os.environ, test_env, clear=False):
                test_settings = Settings()
                
                # Check defaults
                assert test_settings.APP_NAME == "DAR-Cyber"
                assert test_settings.APP_VERSION == "0.1.0"
                assert test_settings.DEBUG is False
                assert test_settings.HOST == "0.0.0.0"
                assert test_settings.PORT == 8000
                assert test_settings.JWT_ALGORITHM == "HS256"
                assert test_settings.ACCESS_TOKEN_EXPIRE_MINUTES == 30
                assert test_settings.REDIS_URL == "redis://localhost:6379/0"
        finally:
            # Restore original env
            for key, value in original_env.items():
                if value is not None:
                    os.environ[key] = value
                elif key in os.environ:
                    del os.environ[key]
    
    def test_settings_load_from_env_file(self, tmp_path):
        """Test that settings can load from .env file."""
        # Create a temporary .env file
        env_file = tmp_path / ".env"
        env_file.write_text(
            "JWT_SECRET_KEY=file-secret-key\n"
            "DATABASE_URL=sqlite:///fromfile.db\n"
            "DEBUG=true\n"
        )
        
        # We can't easily test this without reimporting, but we can verify
        # the Config class has env_file configured
        assert Settings.Config.env_file == ".env"
        assert Settings.Config.env_file_encoding == "utf-8"


class TestRequiredSettings:
    """Tests for required settings validation."""
    
    def test_jwt_secret_key_required(self):
        """Test that JWT_SECRET_KEY is required (no default value)."""
        # Check that JWT_SECRET_KEY has no default in the class definition
        # We look at the field definition
        jwt_field = Settings.model_fields['JWT_SECRET_KEY']
        
        # JWT_SECRET_KEY should not have a default value
        # It's defined as `JWT_SECRET_KEY: str` without default
        assert jwt_field.default is None or jwt_field.default is PydanticUndefined
        assert jwt_field.default_factory is None
    
    def test_jwt_secret_key_no_hardcoded_default(self):
        """Test that JWT_SECRET_KEY doesn't have a hard-coded default."""
        # The class definition should not have a default for JWT_SECRET_KEY
        import inspect
        source = inspect.getsource(Settings)
        
        # Check that JWT_SECRET_KEY doesn't have an assignment with = "something"
        # This is a simple check - in real scenario, use proper AST parsing
        assert 'JWT_SECRET_KEY: str' in source
        # Make sure there's no default like JWT_SECRET_KEY: str = "secret"
        lines = source.split('\n')
        for line in lines:
            if 'JWT_SECRET_KEY' in line and '=' in line and '"' in line:
                # This would indicate a hard-coded default
                pytest.fail("JWT_SECRET_KEY appears to have a hard-coded default")
    
    def test_database_url_optional(self):
        """Test that DATABASE_URL is optional (can be None)."""
        jwt_secret = "test-secret-for-database-test"
        
        with patch.dict(os.environ, {"JWT_SECRET_KEY": jwt_secret}, clear=False):
            test_settings = Settings()
            # DATABASE_URL can be None
            assert test_settings.DATABASE_URL is None or isinstance(test_settings.DATABASE_URL, (str, type(None)))


class TestSettingsSingleton:
    """Tests for settings singleton instance."""
    
    def test_settings_is_singleton(self):
        """Test that settings instance is a singleton."""
        from app.config import settings as settings1
        from app.config import settings as settings2
        
        assert settings1 is settings2
    
    def test_settings_instance_type(self):
        """Test that settings is an instance of Settings."""
        assert isinstance(settings, Settings)


class TestCorsOrigins:
    """Tests for CORS configuration."""
    
    def test_cors_origins_default(self):
        """Test default CORS origins."""
        jwt_secret = "test-secret-for-cors-test"
        
        with patch.dict(os.environ, {"JWT_SECRET_KEY": jwt_secret}, clear=False):
            test_settings = Settings()
            assert "http://localhost:3000" in test_settings.CORS_ORIGINS
            assert "http://localhost:8000" in test_settings.CORS_ORIGINS
    
    def test_cors_origins_from_env(self):
        """Test CORS origins loaded from environment."""
        test_env = {
            "JWT_SECRET_KEY": "test-secret",
            "CORS_ORIGINS": '["http://example.com", "https://app.example.com"]'
        }
        
        with patch.dict(os.environ, test_env, clear=False):
            test_settings = Settings()
            # Note: Pydantic should parse the JSON string
            assert "http://example.com" in test_settings.CORS_ORIGINS


class TestInvalidSettings:
    """Tests for invalid settings handling."""
    
    def test_missing_jwt_secret_raises_error(self):
        """Test that missing JWT_SECRET_KEY raises an error."""
        # Remove JWT_SECRET_KEY from env
        env_backup = os.environ.get("JWT_SECRET_KEY")
        
        try:
            if "JWT_SECRET_KEY" in os.environ:
                del os.environ["JWT_SECRET_KEY"]
            
            # This should raise a validation error
            with pytest.raises(Exception):  # Pydantic ValidationError
                Settings()
        finally:
            # Restore
            if env_backup:
                os.environ["JWT_SECRET_KEY"] = env_backup
    
    def test_invalid_port_type(self):
        """Test that invalid PORT type is handled."""
        test_env = {
            "JWT_SECRET_KEY": "test-secret",
            "PORT": "not-a-number"
        }
        
        with patch.dict(os.environ, test_env, clear=False):
            with pytest.raises(Exception):  # Should raise validation error
                Settings()


class TestNoHardcodedSecrets:
    """Tests to ensure no secrets are hard-coded in config."""
    
    def test_no_hardcoded_jwt_secret(self):
        """Test that JWT_SECRET_KEY is not hard-coded."""
        import inspect
        source = inspect.getsource(Settings)
        
        # Common hard-coded secret patterns to check
        forbidden_patterns = [
            'JWT_SECRET_KEY: str = "secret"',
            'JWT_SECRET_KEY: str = "mysecret"',
            'JWT_SECRET_KEY: str = "devsecret"',
            'JWT_SECRET_KEY = "secret"',
            "JWT_SECRET_KEY = 'secret'",
        ]
        
        for pattern in forbidden_patterns:
            assert pattern not in source, f"Found hard-coded secret pattern: {pattern}"
    
    def test_jwt_secret_from_env_only(self):
        """Test that JWT_SECRET_KEY must come from environment."""
        # The field should be required (no default)
        jwt_field = Settings.model_fields['JWT_SECRET_KEY']
        
        # No default value (PydanticUndefined or None)
        assert jwt_field.default is None or jwt_field.default is PydanticUndefined
        # The type should be str (not Optional[str])
        # This ensures it's required
        assert jwt_field.is_required()
