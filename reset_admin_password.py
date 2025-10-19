#!/usr/bin/env python3
"""
Admin Password Reset Tool
Interactive script to reset admin password
"""

import os
import sys
import getpass

def reset_password():
    """Reset admin password in .env file"""
    
    print("\n" + "="*60)
    print("🔐 ADMIN PASSWORD RESET TOOL")
    print("="*60 + "\n")
    
    env_file = ".env"
    
    # Check if .env exists
    if os.path.exists(env_file):
        print(f"✅ Found {env_file}")
        
        # Show current password (optional)
        show_current = input("\n❓ Do you want to see the current password? (y/n): ").lower()
        if show_current == 'y':
            try:
                with open(env_file, 'r') as f:
                    content = f.read()
                    for line in content.split('\n'):
                        if line.startswith('ADMIN_PASSWORD='):
                            current_password = line.split('=', 1)[1].strip()
                            print(f"\n📝 Current password: {current_password}")
                            break
                    else:
                        print("\n⚠️  No ADMIN_PASSWORD found in .env")
            except Exception as e:
                print(f"\n❌ Error reading .env: {e}")
    else:
        print(f"⚠️  {env_file} not found. Will create new one.")
    
    print("\n" + "-"*60)
    print("Enter new admin password")
    print("(Press Ctrl+C to cancel)")
    print("-"*60 + "\n")
    
    # Get new password
    while True:
        try:
            new_password = getpass.getpass("New password: ")
            
            if not new_password:
                print("❌ Password cannot be empty. Please try again.\n")
                continue
            
            # Confirm password
            confirm_password = getpass.getpass("Confirm password: ")
            
            if new_password != confirm_password:
                print("❌ Passwords don't match. Please try again.\n")
                continue
            
            break
            
        except KeyboardInterrupt:
            print("\n\n❌ Password reset cancelled.")
            sys.exit(0)
    
    # Update .env file
    try:
        # Read existing content
        existing_content = []
        password_found = False
        
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('ADMIN_PASSWORD='):
                        existing_content.append(f'ADMIN_PASSWORD={new_password}\n')
                        password_found = True
                    else:
                        existing_content.append(line)
        
        # If ADMIN_PASSWORD wasn't found, add it
        if not password_found:
            existing_content.append(f'ADMIN_PASSWORD={new_password}\n')
        
        # Write back to file
        with open(env_file, 'w') as f:
            f.writelines(existing_content)
        
        print("\n" + "="*60)
        print("✅ PASSWORD RESET SUCCESSFUL!")
        print("="*60)
        print(f"\n📝 New password has been saved to {env_file}")
        
        # Show password strength
        print("\n🔐 Password Strength Analysis:")
        strength_score = 0
        
        if len(new_password) >= 8:
            print("   ✅ Length: Good (8+ characters)")
            strength_score += 1
        else:
            print(f"   ⚠️  Length: {len(new_password)} characters (recommend 8+)")
        
        if any(c.isupper() for c in new_password):
            print("   ✅ Contains uppercase letters")
            strength_score += 1
        else:
            print("   ⚠️  No uppercase letters")
        
        if any(c.islower() for c in new_password):
            print("   ✅ Contains lowercase letters")
            strength_score += 1
        else:
            print("   ⚠️  No lowercase letters")
        
        if any(c.isdigit() for c in new_password):
            print("   ✅ Contains numbers")
            strength_score += 1
        else:
            print("   ⚠️  No numbers")
        
        if any(not c.isalnum() for c in new_password):
            print("   ✅ Contains special characters")
            strength_score += 1
        else:
            print("   ⚠️  No special characters")
        
        print(f"\n   Overall Strength: {strength_score}/5")
        if strength_score >= 4:
            print("   🌟 Strong password!")
        elif strength_score >= 3:
            print("   👍 Good password")
        else:
            print("   ⚠️  Consider using a stronger password")
        
        print("\n" + "="*60)
        print("🚀 NEXT STEPS:")
        print("="*60)
        print("\n1. Restart Streamlit application")
        print("   Press Ctrl+C in the Streamlit terminal, then run:")
        print("   streamlit run app.py")
        print("\n2. Navigate to Admin Dashboard")
        print("   Click the 📊 icon in the sidebar")
        print("\n3. Login with your new password")
        print(f"   Password: [your new password]")
        print("\n" + "="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error updating password: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        reset_password()
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user.")
        sys.exit(0)
