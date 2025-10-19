#!/usr/bin/env python3
"""
Test Admin Authentication Setup
Run this script to verify your admin configuration
"""

import os
import sys

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ python-dotenv loaded")
except ImportError:
    print("⚠️  python-dotenv not installed (using system environment variables only)")
    print("   Install with: pip install python-dotenv")

print("\n" + "="*60)
print("🔍 ADMIN AUTHENTICATION CONFIGURATION TEST")
print("="*60 + "\n")

# Check ADMIN_PASSWORD
admin_password = os.getenv("ADMIN_PASSWORD")

if admin_password is None:
    print("❌ ADMIN_PASSWORD is NOT set")
    print("\n📝 To enable Admin Dashboard:")
    print("   1. Create/edit .env file")
    print("   2. Add: ADMIN_PASSWORD=your_password")
    print("   3. Restart Streamlit")
    print("\n⚠️  Admin Dashboard will be DISABLED")
    sys.exit(1)
elif admin_password.strip() == "":
    print("❌ ADMIN_PASSWORD is EMPTY")
    print("\n📝 To enable Admin Dashboard:")
    print("   Set a non-empty password in .env file")
    print("   Example: ADMIN_PASSWORD=MySecurePassword123")
    print("\n⚠️  Admin Dashboard will be DISABLED")
    sys.exit(1)
else:
    print("✅ ADMIN_PASSWORD is set")
    print(f"   Length: {len(admin_password)} characters")
    
    # Password strength check
    print("\n🔐 Password Strength Check:")
    
    if len(admin_password) < 8:
        print("   ⚠️  Password is short (less than 8 characters)")
        print("      Recommendation: Use at least 8 characters")
    else:
        print(f"   ✅ Length: {len(admin_password)} characters (good)")
    
    has_upper = any(c.isupper() for c in admin_password)
    has_lower = any(c.islower() for c in admin_password)
    has_digit = any(c.isdigit() for c in admin_password)
    has_special = any(not c.isalnum() for c in admin_password)
    
    strength_score = sum([has_upper, has_lower, has_digit, has_special])
    
    if has_upper:
        print("   ✅ Contains uppercase letters")
    else:
        print("   ⚠️  No uppercase letters")
    
    if has_lower:
        print("   ✅ Contains lowercase letters")
    else:
        print("   ⚠️  No lowercase letters")
    
    if has_digit:
        print("   ✅ Contains numbers")
    else:
        print("   ⚠️  No numbers")
    
    if has_special:
        print("   ✅ Contains special characters")
    else:
        print("   ⚠️  No special characters")
    
    print(f"\n   Overall Strength: {strength_score}/4")
    
    if strength_score >= 3:
        print("   🌟 Strong password")
    elif strength_score >= 2:
        print("   👍 Moderate password")
    else:
        print("   ⚠️  Weak password - consider improving")
    
    print("\n✅ Admin Dashboard will be ENABLED")

# Check OpenAI API Key (optional)
print("\n" + "-"*60)
openai_key = os.getenv("OPENAI_API_KEY")

if openai_key:
    print("✅ OPENAI_API_KEY is set")
    if openai_key.startswith("sk-"):
        print("   ✅ Format looks correct (starts with 'sk-')")
    else:
        print("   ⚠️  Format unusual (doesn't start with 'sk-')")
else:
    print("ℹ️  OPENAI_API_KEY not set (can be entered in app)")

# Summary
print("\n" + "="*60)
print("📋 CONFIGURATION SUMMARY")
print("="*60)

if admin_password and admin_password.strip() != "":
    print("\n✅ Admin Dashboard: ENABLED")
    print("   - You can access the admin dashboard")
    print("   - Password will be required on login")
    print("   - Use the password you set in .env file")
else:
    print("\n❌ Admin Dashboard: DISABLED")
    print("   - Set ADMIN_PASSWORD to enable")

print("\n🚀 Next Steps:")
print("   1. Start Streamlit: streamlit run app.py")
print("   2. Navigate to Admin Dashboard (📊)")
print("   3. Enter your admin password")
print("   4. Enjoy monitoring your users!")

print("\n" + "="*60)
print("Test completed!")
print("="*60 + "\n")
