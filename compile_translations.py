#!/usr/bin/env python3

import os
import struct
import polib

def compile_po_to_mo(po_file, mo_file):
    """Convert .po file to .mo file using polib if available, otherwise create minimal .mo file"""
    try:
        # Try to use polib if available (better .mo file creation)
        po = polib.pofile(po_file)
        po.save_as_mofile(mo_file)
        print(f"Compiled {po_file} to {mo_file} using polib")
    except ImportError:
        # Fallback to manual creation
        print(f"polib not available, creating minimal .mo file for {po_file}")
        with open(mo_file, 'wb') as f:
            # Write a minimal .mo file header
            f.write(struct.pack('<I', 0x950412de))  # magic number
            f.write(struct.pack('<I', 0))  # file format revision
            f.write(struct.pack('<I', 0))  # number of strings
            f.write(struct.pack('<I', 28))  # offset of table with original strings
            f.write(struct.pack('<I', 28))  # offset of table with translated strings
            f.write(struct.pack('<I', 0))  # size of hashing table
            f.write(struct.pack('<I', 0))  # offset of hashing table

if __name__ == "__main__":
    # Install polib if not available
    try:
        import polib
    except ImportError:
        print("Installing polib for proper .mo file creation...")
        os.system("pip install polib")
        import polib
    
    # Create directories if they don't exist
    os.makedirs('locales/en/LC_MESSAGES', exist_ok=True)
    os.makedirs('locales/am/LC_MESSAGES', exist_ok=True)
    os.makedirs('locales/om/LC_MESSAGES', exist_ok=True)
    
    # Compile .po files to .mo files
    if os.path.exists('locales/en/LC_MESSAGES/app.po'):
        compile_po_to_mo('locales/en/LC_MESSAGES/app.po', 'locales/en/LC_MESSAGES/app.mo')
    
    if os.path.exists('locales/am/LC_MESSAGES/app.po'):
        compile_po_to_mo('locales/am/LC_MESSAGES/app.po', 'locales/am/LC_MESSAGES/app.mo')
        
    if os.path.exists('locales/om/LC_MESSAGES/app.po'):
        compile_po_to_mo('locales/om/LC_MESSAGES/app.po', 'locales/om/LC_MESSAGES/app.mo')
    
    print("Translation files compiled successfully!")