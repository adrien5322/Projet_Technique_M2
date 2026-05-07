"""Test script to verify P0 fixes are working.

This script tests:
1. Config loads without defaults for JWT_SECRET_KEY
2. Database connection works
3. get_db() returns a real session (not None)
4. No hard-coded passwords in auth routes
"""

import os
import sys
from pathlib import Path

# Add the backend directory to the path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))


def test_config_requires_jwt_secret():
    """Test that JWT_SECRET_KEY is required (no default)."""
    print("=" * 60)
    print("TEST 1: Config requires JWT_SECRET_KEY (no default)")
    print("=" * 60)
    
    # Temporarily rename .env if it exists to test required field
    env_file = backend_dir / ".env"
    env_backup = backend_dir / ".env.backup_test"
    
    if env_file.exists():
        env_file.rename(env_backup)
    
    try:
        # Clear any cached settings
        if 'app.config' in sys.modules:
            del sys.modules['app.config']
        
        from app.config import Settings
        
        try:
            # This should fail without JWT_SECRET_KEY
            settings = Settings()
            print("❌ FAIL: Settings loaded without JWT_SECRET_KEY (should have failed)")
            return False
        except Exception as e:
            if "JWT_SECRET_KEY" in str(e):
                print("✅ PASS: JWT_SECRET_KEY is required (no default value)")
                return True
            else:
                print(f"❌ FAIL: Unexpected error: {e}")
                return False
    finally:
        # Restore .env if we backed it up
        if env_backup.exists():
            env_backup.rename(env_file)


def test_db_connection():
    """Test that database connection works."""
    print("\n" + "=" * 60)
    print("TEST 2: Database connection")
    print("=" * 60)
    
    try:
        from app.db import engine
        
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            row = result.fetchone()
            if row and row[0] == 1:
                print("✅ PASS: Database connection successful")
                return True
            else:
                print("❌ FAIL: Database query returned unexpected result")
                return False
    except Exception as e:
        print(f"❌ FAIL: Database connection failed: {e}")
        print("   Make sure PostgreSQL is running and DATABASE_URL is correct")
        return False


def test_get_db_returns_real_session():
    """Test that get_db() returns a real session (not None)."""
    print("\n" + "=" * 60)
    print("TEST 3: get_db() returns real session")
    print("=" * 60)
    
    try:
        from app.db import get_db
        from sqlalchemy.orm import Session
        
        # Get a session from the generator
        db_gen = get_db()
        db = next(db_gen)
        
        if db is None:
            print("❌ FAIL: get_db() returned None (mock DB still in place)")
            return False
        
        if not isinstance(db, Session):
            print(f"❌ FAIL: get_db() returned {type(db)} instead of Session")
            return False
        
        # Try to close the session properly
        try:
            next(db_gen)
        except StopIteration:
            pass
        
        print("✅ PASS: get_db() returns a real SQLAlchemy Session")
        return True
    except Exception as e:
        print(f"❌ FAIL: get_db() test failed: {e}")
        return False


def test_no_hardcoded_passwords():
    """Test that auth routes don't contain hard-coded passwords."""
    print("\n" + "=" * 60)
    print("TEST 4: No hard-coded passwords in auth routes")
    print("=" * 60)
    
    try:
        auth_routes_file = backend_dir / "app" / "auth" / "routes.py"
        
        with open(auth_routes_file, 'r') as f:
            content = f.read()
        
        # Check for common hard-coded password patterns
        suspicious_patterns = [
            ('admin123', 'Hard-coded admin password'),
            ('analyst123', 'Hard-coded analyst password'),
            ('password123', 'Common hard-coded password'),
            ('"admin"', 'Hard-coded username with password check'),
        ]
        
        found_issues = False
        for pattern, description in suspicious_patterns:
            if pattern in content:
                # Check if it's in a comment or actual code
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if pattern in line and not line.strip().startswith('#'):
                        print(f"❌ FAIL: Found {description} on line {i+1}")
                        found_issues = True
        
        if not found_issues:
            print("✅ PASS: No hard-coded passwords found in auth routes")
            return True
        else:
            return False
    except Exception as e:
        print(f"❌ FAIL: Could not check for hard-coded passwords: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("DEVINCIWATCH P0 FIXES VERIFICATION")
    print("=" * 60)
    
    results = []
    
    # Note: test_config_requires_jwt_secret will rename .env temporarily
    # So we run it first
    results.append(("Config requires JWT_SECRET_KEY", test_config_requires_jwt_secret()))
    
    # For the remaining tests, we need .env to exist
    env_file = backend_dir / ".env"
    if not env_file.exists():
        print("\n⚠️  WARNING: .env file not found")
        print("   Create one from .env.example to run DB tests")
        print("   Skipping DB connection tests...\n")
        
        results.append(("Database connection", False))
        results.append(("get_db() returns real session", False))
    else:
        results.append(("Database connection", test_db_connection()))
        results.append(("get_db() returns real session", test_get_db_returns_real_session()))
    
    results.append(("No hard-coded passwords", test_no_hardcoded_passwords()))
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All P0 fixes verified successfully!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the fixes.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
