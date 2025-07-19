import shutil
import os

source_profile = r"C:\Users\Acer\AppData\Local\Google\Chrome\User Data\Profile 4"
destination_profile = r"D:\whatsapp-bot-profile"

# Make sure destination directory is clean
if os.path.exists(destination_profile):
    print(f"⚠️ Destination '{destination_profile}' already exists. Removing it...")
    shutil.rmtree(destination_profile)

print(f"📁 Copying Chrome Profile from:\n{source_profile}\n→\n{destination_profile}")

try:
    shutil.copytree(source_profile, destination_profile)
    print("✅ Profile cloned successfully!")
except Exception as e:
    print(f"❌ Error cloning profile:\n{e}")
