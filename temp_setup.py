import sys 
import subprocess 
import importlib.util 
 
def check_module(module_name): 
    try: 
        spec = importlib.util.find_spec(module_name) 
        return spec is not None 
    except: 
        return False 
 
def install_package(package_name): 
    try: 
        cmd = [sys.executable, '-m', 'pip', 'install', package_name, '--upgrade', '--quiet'] 
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120) 
        return result.returncode == 0 
    except: 
        return False 
 
def check_ffmpeg(): 
    try: 
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=5) 
        return result.returncode == 0 
    except: 
        return False 
 
packages = {'yt_dlp': 'yt-dlp', 'requests': 'requests', 'PIL': 'pillow'} 
missing = [] 
for module_name, package_name in packages.items(): 
    if check_module(module_name): 
        print(f'✅ {package_name} - OK') 
    else: 
        print(f'❌ {package_name} - Missing') 
        missing.append(package_name) 
 
if missing: 
    print(f'📦 Installing {len(missing)} packages...') 
    all_success = True 
    for pkg in missing: 
        print(f'  Installing {pkg}...', end='') 
        if install_package(pkg): 
            print(' ✅') 
        else: 
            print(' ❌') 
            all_success = False 
    if not all_success: 
        print('❌ Some packages failed to install') 
        sys.exit(1) 
    else: 
        print('✅ All packages installed') 
 
print('🎬 Checking FFmpeg...') 
if check_ffmpeg(): 
    print('✅ FFmpeg - Available') 
else: 
    print('⚠️  FFmpeg - Not in PATH') 
    print('  Installing ffmpeg-python package...') 
    if install_package('ffmpeg-python'): 
        print('✅ ffmpeg-python installed') 
    else: 
        print('⚠️  FFmpeg setup incomplete') 
print('🎯 Setup check completed') 
