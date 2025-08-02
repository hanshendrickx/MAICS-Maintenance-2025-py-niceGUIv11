# MACS - Medical Analysis of Current Complaints and Signs
# Professional Medical System with Multi-Layer Security

import os
import sys
import subprocess
from pathlib import Path

# Import security manager (with fallback if not available)
try:
    from security_manager import SecurityManager
    SECURITY_AVAILABLE = True
except ImportError:
    print("⚠️  Security manager not available - running in basic mode")
    SECURITY_AVAILABLE = False
    class SecurityManager:
        def apply_security_measures(self): pass
        def security_status(self): return {"level": "BASIC"}

def check_and_setup_environment():
    """Smart environment detection and setup for any system"""
    print("🔍 Checking Python environment...")
    
    # Check if we're already in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if in_venv:
        print("✅ Already running in virtual environment")
        print(f"   Python executable: {sys.executable}")
    else:
        print("⚠️  Not in virtual environment - checking for .venv")
        
        # Look for virtual environment in current directory
        current_dir = Path.cwd()
        venv_path = current_dir / '.venv'
        venv_python = venv_path / 'Scripts' / 'python.exe'
        
        if venv_python.exists():
            print(f"✅ Found working virtual environment: {venv_path}")
            print("🔄 Restarting with virtual environment...")
            
            # Check if NiceGUI is installed in venv
            try:
                result = subprocess.run([str(venv_python), '-c', 'import nicegui; print(nicegui.__version__)'], 
                                     capture_output=True, text=True, check=True)
                print(f"✅ NiceGUI {result.stdout.strip()} already available in venv")
            except subprocess.CalledProcessError:
                print("📦 Installing NiceGUI in virtual environment...")
                try:
                    subprocess.check_call([str(venv_python), '-m', 'pip', 'install', 'nicegui', '--quiet'])
                    print("✅ NiceGUI installed successfully")
                except subprocess.CalledProcessError:
                    print("❌ Failed to install NiceGUI in venv")
                    return False
            
            # Restart the script with venv Python
            print("🚀 Restarting MACS with virtual environment...")
            print("=" * 50)
            try:
                os.execv(str(venv_python), [str(venv_python)] + sys.argv)
            except Exception as e:
                print(f"❌ Failed to restart with venv: {e}")
                return False
        else:
            print("❌ No virtual environment found")
            print("💡 Consider creating one with: python -m venv .venv")
    
    # Check NiceGUI installation in current environment
    try:
        import nicegui
        print(f"✅ NiceGUI version {nicegui.__version__} is available")
        return True
    except ImportError:
        print("❌ NiceGUI not found in current environment")
        
        # Try to install NiceGUI in current environment
        print("🔄 Attempting to install NiceGUI...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'nicegui', '--quiet'])
            print("✅ NiceGUI installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install NiceGUI")
            print("💡 Try manually: pip install nicegui")
            return False

def create_venv_if_needed():
    """Create virtual environment if it doesn't exist - Universal helper"""
    current_dir = Path.cwd()
    venv_path = current_dir / '.venv'
    
    if not venv_path.exists():
        print("🔄 Creating virtual environment...")
        try:
            subprocess.check_call([sys.executable, '-m', 'venv', '.venv'])
            print("✅ Virtual environment created at .venv")
            
            # Install NiceGUI in new venv
            venv_python = venv_path / 'Scripts' / 'python.exe' if sys.platform == 'win32' else venv_path / 'bin' / 'python'
            venv_pip = venv_path / 'Scripts' / 'pip.exe' if sys.platform == 'win32' else venv_path / 'bin' / 'pip'
            
            if venv_python.exists():
                print("� Installing NiceGUI in new virtual environment...")
                subprocess.check_call([str(venv_python), '-m', 'pip', 'install', 'nicegui', '--quiet'])
                print("✅ NiceGUI installed in virtual environment")
                
                print("\n💡 MACS is ready! Restart to use virtual environment:")
                if sys.platform == 'win32':
                    print("   .venv\\Scripts\\python.exe main.py")
                else:
                    print("   .venv/bin/python main.py")
                return False
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create virtual environment: {e}")
            print("💡 You can still run MACS if NiceGUI is installed globally")
            return True  # Continue anyway
    
    return True

def show_usage_instructions():
    """Show helpful usage instructions for different scenarios"""
    print("\n" + "="*60)
    print("📚 MACS USAGE INSTRUCTIONS")
    print("="*60)
    print("🎯 Recommended (with virtual environment):")
    if sys.platform == 'win32':
        print("   .venv\\Scripts\\python.exe main.py")
    else:
        print("   .venv/bin/python main.py")
    
    print("\n🔧 Alternative methods:")
    print("   python main.py          # Use system Python")
    print("   py main.py              # Use Python launcher (Windows)")
    
    print("\n📦 If NiceGUI is missing:")
    print("   pip install nicegui")
    
    print("\n🆕 Create virtual environment:")
    print("   python -m venv .venv")
    if sys.platform == 'win32':
        print("   .venv\\Scripts\\activate")
    else:
        print("   source .venv/bin/activate")
    print("   pip install nicegui")
    print("="*60)

# Initialize environment
print("=" * 50)
print("🏥 MACS - Medical Analysis System")
print("=" * 50)

if not check_and_setup_environment():
    print("\n❌ Environment setup failed.")
    show_usage_instructions()
    input("\nPress Enter to exit...")
    sys.exit(1)

print("🚀 Starting MACS application...")
print("🌐 Open your browser to: http://localhost:8080")
print("⏹️  Press Ctrl+C to stop the server\n")

from nicegui import ui

@ui.page('/')
def index():
    # Accessibility and UI state
    ui_state = {
        'high_contrast': False,
        'dark_mode': False,
        'button_style': 'info',  # 'info' or 'plain'
        'large_text': False,
        'font_size': 'medium'  # 'small', 'medium', 'large', 'xl'
    }
    
    # Set dynamic page background with accessibility options
    def update_theme():
        if ui_state['dark_mode']:
            bg_color = '#1a1a1a' if ui_state['high_contrast'] else '#2d3748'
            text_color = '#ffffff'
        else:
            bg_color = '#ffffff' if ui_state['high_contrast'] else '#f8fafc'
            text_color = '#000000' if ui_state['high_contrast'] else '#374151'
        
        ui.add_head_html(f'''
        <style>
            body {{ 
                background-color: {bg_color}; 
                color: {text_color};
                transition: all 0.3s ease;
            }}
            .high-contrast {{ 
                filter: contrast(150%) brightness(120%); 
            }}
            .large-text {{ 
                font-size: 120% !important; 
            }}
        </style>
        ''')
    
    update_theme()
    
    # Main container with responsive positioning
    with ui.column().classes('w-full items-center justify-start min-h-screen py-4').style('background-color: inherit'):
        # Accessibility controls bar
        accessibility_container = ui.row().classes('gap-2 mb-4 flex-wrap justify-center')
        
        def create_accessibility_controls():
            accessibility_container.clear()
            with accessibility_container:
                ui.button('🔆 High Contrast', on_click=lambda: toggle_contrast()).classes('text-xs px-3 py-1 bg-gray-700 text-white')
                ui.button('🌙 Dark/Light', on_click=lambda: toggle_dark_mode()).classes('text-xs px-3 py-1 bg-gray-700 text-white')
                ui.button('ℹ️/▶️ Button Style', on_click=lambda: toggle_button_style()).classes('text-xs px-3 py-1 bg-gray-700 text-white')
                ui.button('🔍 Large Text', on_click=lambda: toggle_large_text()).classes('text-xs px-3 py-1 bg-gray-700 text-white')
                # Font size toggle buttons with current size indicator
                ui.button('-T', on_click=lambda: decrease_font_size()).classes('text-xs px-2 py-1 bg-blue-600 hover:bg-blue-800 text-white font-bold')
                ui.label(f"({ui_state['font_size']})").classes('text-xs text-gray-600 px-1 font-bold')
                ui.button('T+', on_click=lambda: increase_font_size()).classes('text-xs px-2 py-1 bg-blue-600 hover:bg-blue-800 text-white font-bold')
        
        create_accessibility_controls()
        
        # Security Status Display
        security_container = ui.row().classes('gap-2 mb-4 flex-wrap justify-center')
        
        def create_security_status():
            security_container.clear()
            with security_container:
                # Get current security status
                if SECURITY_AVAILABLE:
                    status = security.security_status()
                    level = status['level']
                    license_valid = status['license_valid']
                    
                    # Security level indicator
                    if level == "PRO":
                        ui.badge("🏥 PRO", color="green").classes('text-sm font-bold')
                        ui.label("Medical Professional License Active").classes('text-sm text-green-600 font-medium')
                    elif level == "PROTECTED":
                        ui.badge("⚠️ PROTECTED", color="orange").classes('text-sm font-bold')
                        ui.label("Limited Mode - Hatch Service Unavailable").classes('text-sm text-orange-600')
                    else:  # OPEN
                        ui.badge("🌐 OPEN", color="blue").classes('text-sm font-bold')
                        ui.label("Open Source Mode").classes('text-sm text-blue-600')
                    
                    # PRO upgrade button for non-PRO users
                    if level != "PRO":
                        ui.button("Upgrade to PRO", on_click=lambda: show_pro_info()).classes('text-xs px-3 py-1 bg-green-600 hover:bg-green-700 text-white ml-2')
                else:
                    ui.badge("🔧 BASIC", color="gray").classes('text-sm font-bold')
                    ui.label("Basic Mode - Security Manager Not Available").classes('text-sm text-gray-600')
        
        def show_pro_info():
            """Show PRO license information dialog."""
            with ui.dialog().classes('max-w-md') as dialog:
                with ui.card():
                    ui.html('<h3 class="text-lg font-bold mb-4">🏥 MACS PRO for Medical Professionals</h3>')
                    ui.html('''
                    <div class="space-y-3">
                        <p><strong>PRO Features:</strong></p>
                        <ul class="list-disc ml-4 space-y-1">
                            <li>🔒 HIPAA Compliance</li>
                            <li>🔐 AES-256 Encryption</li>
                            <li>📊 Advanced Medical AI</li>
                            <li>🏥 Professional Support</li>
                            <li>📋 Audit Trail Logging</li>
                        </ul>
                        <p><strong>Pricing:</strong> $299/year</p>
                        <p><strong>Contact:</strong> licensing@macs-medical.com</p>
                    </div>
                    ''')
                    with ui.row().classes('mt-4 gap-2'):
                        ui.button('Close', on_click=dialog.close).classes('bg-gray-500 text-white')
                        ui.button('Request Trial', on_click=lambda: request_trial_license()).classes('bg-green-600 text-white')
            dialog.open()
        
        def request_trial_license():
            """Request a trial license."""
            if SECURITY_AVAILABLE:
                security.request_pro_license()
            else:
                ui.notify("Security manager not available", type="warning")
        
        create_security_status()
        
        # MACS title - positioned higher (1/3 height) and responsive
        ui.label('MACS').classes('text-4xl md:text-5xl lg:text-6xl font-bold text-blue-600 mb-2 text-center').style('margin-top: 5vh;')
        
        # Main welcome card with enhanced contrast
        card_bg = '#000000' if ui_state['high_contrast'] else 'white'
        card_text = '#ffffff' if ui_state['high_contrast'] else 'text-gray-800'
        
        with ui.card().classes('p-6 shadow-xl mx-auto').style(f'background-color: {card_bg}; border-radius: 12px; width: fit-content; min-width: 300px; border: 2px solid {"#ffffff" if ui_state["high_contrast"] else "#e5e7eb"};'):
            with ui.column().classes('items-center text-center'):
                text_size = 'text-3xl' if ui_state['large_text'] else 'text-2xl'
                ui.label('Medical Complaints Summary').classes(f'{text_size} font-semibold mb-4 {card_text}')
                ui.button('Get Started', icon='play_arrow').classes('bg-blue-600 hover:bg-blue-800 text-white px-8 py-2 font-bold border-2 border-blue-800')
        
        # Create carousel container
        carousel_container = ui.column().classes('mt-6 w-full max-w-6xl items-center')
        
        # Current page state
        current_page = {'value': 0}
        
        def toggle_contrast():
            ui_state['high_contrast'] = not ui_state['high_contrast']
            update_theme()
            create_accessibility_controls()
            create_carousel()
        
        def toggle_dark_mode():
            ui_state['dark_mode'] = not ui_state['dark_mode']
            update_theme()
            create_accessibility_controls()
            create_carousel()
        
        def toggle_button_style():
            ui_state['button_style'] = 'plain' if ui_state['button_style'] == 'info' else 'info'
            create_accessibility_controls()
            create_carousel()
        
        def toggle_large_text():
            ui_state['large_text'] = not ui_state['large_text']
            create_accessibility_controls()
            create_carousel()
        
        def decrease_font_size():
            """Decrease font size: xl -> large -> medium -> small (stops at small)"""
            if ui_state['font_size'] == 'xl':
                ui_state['font_size'] = 'large'
            elif ui_state['font_size'] == 'large':
                ui_state['font_size'] = 'medium'
            elif ui_state['font_size'] == 'medium':
                ui_state['font_size'] = 'small'
            # stays at 'small' if already small
            create_accessibility_controls()
            create_carousel()
        
        def increase_font_size():
            """Increase font size: small -> medium -> large -> xl (stops at xl)"""
            if ui_state['font_size'] == 'small':
                ui_state['font_size'] = 'medium'
            elif ui_state['font_size'] == 'medium':
                ui_state['font_size'] = 'large'
            elif ui_state['font_size'] == 'large':
                ui_state['font_size'] = 'xl'
            # stays at 'xl' if already xl
            create_accessibility_controls()
            create_carousel()
        
        def get_button_icon():
            return 'info' if ui_state['button_style'] == 'info' else 'chevron_right'
        
        def get_responsive_text_sizes():
            """Get responsive text sizes based on screen size and font size setting"""
            # Base sizes for different font_size settings - 18px baseline for better readability
            size_map = {
                'small': {
                    'card_title': 'text-sm sm:text-base md:text-lg lg:text-xl',      # 14px → 16px → 18px → 20px
                    'card_subtitle': 'text-xs sm:text-sm md:text-base lg:text-base', # 12px → 14px → 16px → 16px
                    'popup_title': 'text-xl sm:text-2xl md:text-3xl lg:text-4xl',
                    'popup_content': 'text-base sm:text-lg md:text-xl lg:text-xl'    # 16px → 18px → 20px → 20px
                },
                'medium': {
                    'card_title': 'text-base sm:text-lg md:text-xl lg:text-2xl',    # 16px → 18px → 20px → 24px
                    'card_subtitle': 'text-sm sm:text-base md:text-lg lg:text-lg',  # 14px → 16px → 18px → 18px
                    'popup_title': 'text-2xl sm:text-3xl md:text-4xl lg:text-5xl',
                    'popup_content': 'text-lg sm:text-xl md:text-2xl lg:text-2xl'   # 18px → 20px → 24px → 24px
                },
                'large': {
                    'card_title': 'text-lg sm:text-xl md:text-2xl lg:text-3xl',     # 18px → 20px → 24px → 30px
                    'card_subtitle': 'text-base sm:text-lg md:text-xl lg:text-xl',  # 16px → 18px → 20px → 20px
                    'popup_title': 'text-3xl sm:text-4xl md:text-5xl lg:text-6xl',
                    'popup_content': 'text-xl sm:text-2xl md:text-3xl lg:text-3xl'  # 20px → 24px → 30px → 30px
                },
                'xl': {
                    'card_title': 'text-xl sm:text-2xl md:text-3xl lg:text-4xl',    # 20px → 24px → 30px → 36px
                    'card_subtitle': 'text-lg sm:text-xl md:text-2xl lg:text-2xl',  # 18px → 20px → 24px → 24px
                    'popup_title': 'text-4xl sm:text-5xl md:text-6xl lg:text-7xl',
                    'popup_content': 'text-2xl sm:text-3xl md:text-4xl lg:text-4xl' # 24px → 30px → 36px → 36px
                }
            }
            
            # Use font_size setting, but if large_text is enabled, bump up one level
            current_size = ui_state['font_size']
            if ui_state['large_text']:
                if current_size == 'small':
                    current_size = 'medium'
                elif current_size == 'medium':
                    current_size = 'large'
                elif current_size == 'large':
                    current_size = 'xl'
                # xl stays xl
            
            return size_map.get(current_size, size_map['medium'])
        
        def get_responsive_card_sizes():
            """Get responsive card dimensions for optimal viewing - mobile-first approach"""
            return {
                # Mobile: 2 cards per row (45% width each), Tablet: 3-4 cards, Desktop: 5 cards
                'width': 'w-[45%] sm:w-36 md:w-40 lg:w-44 xl:w-48',  # 45% → 144px → 160px → 176px → 192px
                'height': 'h-32 sm:h-28 md:h-32 lg:h-36 xl:h-40',    # Taller on mobile: 128px → 112px → 128px → 144px → 160px
                'padding': 'p-3 sm:p-3 md:p-4 lg:p-4',
                'gap': 'gap-2 sm:gap-3 md:gap-4 lg:gap-5',
                # Add max-width to prevent cards from getting too wide on larger screens
                'max_width': 'max-w-[180px] sm:max-w-none'
            }
        
        def make_card_clickable(card_type):
            """Make entire card clickable for better accessibility"""
            return f"""
            cursor: pointer; 
            transition: all 0.2s ease;
            transform: scale(1);
            """
        
        def card_hover_effect():
            """Enhanced hover effect for clickable cards"""
            return """
            :hover {
                transform: scale(1.02);
                box-shadow: 0 8px 25px rgba(0,0,0,0.2);
            }
            """
        
        def get_card_colors():
            if ui_state['high_contrast']:
                return {
                    'bg': '#000000',
                    'text': '#ffffff',
                    'border': '#ffffff',
                    'required': '#00ff00',  # Bright green
                    'optional': '#ffff00'   # Bright yellow
                }
            elif ui_state['dark_mode']:
                return {
                    'bg': '#2d3748',
                    'text': '#ffffff',
                    'border': '#4a5568',
                    'required': '#48bb78',
                    'optional': '#ed8936'
                }
            else:
                return {
                    'bg': 'white',
                    'text': '#374151',
                    'border': '#e5e7eb',
                    'required': '#059669',
                    'optional': '#6b7280'
                }
        
        def create_carousel():
            carousel_container.clear()
            colors = get_card_colors()
            text_sizes = get_responsive_text_sizes()
            card_sizes = get_responsive_card_sizes()
            
            with carousel_container:
                # Main cards row with enhanced accessibility - Mobile-first responsive layout
                with ui.row().classes(f'{card_sizes["gap"]} justify-center relative flex-wrap px-4'):
                    # Medical Analysis Card - Required (Dark Green) - FULLY CLICKABLE
                    with ui.card().classes(f'{card_sizes["padding"]} shadow-xl relative cursor-pointer transition-all duration-200 hover:scale-105 {card_sizes["width"]} {card_sizes["height"]} {card_sizes["max_width"]}').style(f'background-color: {colors["bg"]}; border-radius: 8px; border: 3px solid {colors["border"]};').on('click', lambda: show_popup('medical')):
                        with ui.column().classes('items-center text-center h-full justify-center w-full'):
                            ui.icon('medical_services').classes('text-blue-600 mb-1 text-2xl sm:text-2xl md:text-3xl')
                            ui.label('Medical Analysis').classes(f'{text_sizes["card_title"]} font-bold text-center').style(f'color: {colors["text"]}')
                            ui.label('Required').classes(f'{text_sizes["card_subtitle"]} font-bold text-center').style(f'color: {colors["required"]}')
                        
                        # Info indicator button - responsive sizing
                        button_icon = get_button_icon()
                        with ui.button(icon=button_icon).classes(
                            'absolute top-1 right-1 w-5 h-5 sm:w-5 sm:h-5 md:w-6 md:h-6 rounded-full bg-green-800 hover:bg-green-900 text-white shadow-lg border border-green-900 pointer-events-none flex items-center justify-center text-xs'):
                            pass
                    
                    # Data Insights Card - Optional (Gray) - FULLY CLICKABLE
                    with ui.card().classes(f'{card_sizes["padding"]} shadow-xl relative cursor-pointer transition-all duration-200 hover:scale-105 {card_sizes["width"]} {card_sizes["height"]} {card_sizes["max_width"]}').style(f'background-color: {colors["bg"]}; border-radius: 8px; border: 3px solid {colors["border"]};').on('click', lambda: show_popup('insights')):
                        with ui.column().classes('items-center text-center h-full justify-center w-full'):
                            ui.icon('analytics').classes('text-green-600 mb-1 text-2xl sm:text-2xl md:text-3xl')
                            ui.label('Data Insights').classes(f'{text_sizes["card_title"]} font-bold text-center').style(f'color: {colors["text"]}')
                            ui.label('Optional').classes(f'{text_sizes["card_subtitle"]} font-bold text-center').style(f'color: {colors["optional"]}')
                        
                        # Info indicator button - responsive sizing
                        button_icon = get_button_icon()
                        with ui.button(icon=button_icon).classes(
                            'absolute top-1 right-1 w-5 h-5 sm:w-5 sm:h-5 md:w-6 md:h-6 rounded-full bg-gray-900 hover:bg-black text-white shadow-lg border border-black pointer-events-none flex items-center justify-center text-xs'):
                            pass
                    
                    # Security Card - Required Once (Dark Green) - FULLY CLICKABLE
                    with ui.card().classes(f'{card_sizes["padding"]} shadow-xl relative cursor-pointer transition-all duration-200 hover:scale-105 {card_sizes["width"]} {card_sizes["height"]} {card_sizes["max_width"]}').style(f'background-color: {colors["bg"]}; border-radius: 8px; border: 3px solid {colors["border"]};').on('click', lambda: show_popup('security')):
                        with ui.column().classes('items-center text-center h-full justify-center w-full'):
                            ui.icon('security').classes('text-purple-600 mb-1 text-2xl sm:text-2xl md:text-3xl')
                            ui.label('Secure & Private').classes(f'{text_sizes["card_title"]} font-bold text-center').style(f'color: {colors["text"]}')
                            ui.label('Required Once').classes(f'{text_sizes["card_subtitle"]} font-bold text-center').style(f'color: {colors["required"]}')
                        
                        # Info indicator button - responsive sizing
                        button_icon = get_button_icon()
                        with ui.button(icon=button_icon).classes(
                            'absolute top-1 right-1 w-5 h-5 sm:w-5 sm:h-5 md:w-6 md:h-6 rounded-full bg-green-800 hover:bg-green-900 text-white shadow-lg border border-green-900 pointer-events-none flex items-center justify-center text-xs'):
                            pass
                    
                    # Doctor Loves It Card - Outcome (Gold/Yellow) - FULLY CLICKABLE
                    with ui.card().classes(f'{card_sizes["padding"]} shadow-xl relative cursor-pointer transition-all duration-200 hover:scale-105 {card_sizes["width"]} {card_sizes["height"]} {card_sizes["max_width"]}').style(f'background-color: {colors["bg"]}; border-radius: 8px; border: 3px solid {colors["border"]};').on('click', lambda: show_popup('doctor')):
                        with ui.column().classes('items-center text-center h-full justify-center w-full'):
                            ui.icon('favorite').classes('text-red-600 mb-1 text-2xl sm:text-2xl md:text-3xl')
                            ui.label('Doctor Loves It!').classes(f'{text_sizes["card_title"]} font-bold text-center').style(f'color: {colors["text"]}')
                            ui.label('Best Care').classes(f'{text_sizes["card_subtitle"]} font-bold text-center').style('color: #fbbf24;')  # Gold color
                        
                        # Info indicator button - responsive sizing
                        button_icon = get_button_icon()
                        with ui.button(icon=button_icon).classes(
                            'absolute top-1 right-1 w-5 h-5 sm:w-5 sm:h-5 md:w-6 md:h-6 rounded-full bg-yellow-600 hover:bg-yellow-800 text-white shadow-lg border border-yellow-800 pointer-events-none flex items-center justify-center text-xs'):
                            pass
                    
                    # Complaints & Documentation Card - Evidence (Orange) - FULLY CLICKABLE
                    with ui.card().classes(f'{card_sizes["padding"]} shadow-xl relative cursor-pointer transition-all duration-200 hover:scale-105 {card_sizes["width"]} {card_sizes["height"]} {card_sizes["max_width"]}').style(f'background-color: {colors["bg"]}; border-radius: 8px; border: 3px solid {colors["border"]};').on('click', lambda: show_popup('complaints')):
                        with ui.column().classes('items-center text-center h-full justify-center w-full'):
                            ui.icon('assignment').classes('text-orange-600 mb-1 text-2xl sm:text-2xl md:text-3xl')
                            ui.label('Complaints & Proof').classes(f'{text_sizes["card_title"]} font-bold text-center').style(f'color: {colors["text"]}')
                            ui.label('Evidence').classes(f'{text_sizes["card_subtitle"]} font-bold text-center').style('color: #ea580c;')  # Orange color
                        
                        # Info indicator button - responsive sizing
                        button_icon = get_button_icon()
                        with ui.button(icon=button_icon).classes(
                            'absolute top-1 right-1 w-5 h-5 sm:w-5 sm:h-5 md:w-6 md:h-6 rounded-full bg-orange-600 hover:bg-orange-800 text-white shadow-lg border border-orange-800 pointer-events-none flex items-center justify-center text-xs'):
                            pass
                
                # Simple popup overlay - WITH SCROLLING for content
                if current_page['value'] > 0:
                    # Full screen overlay for popup
                    popup_bg = '#000000' if ui_state['high_contrast'] else colors['bg']
                    popup_text = '#ffffff' if ui_state['high_contrast'] else colors['text']
                    
                    with ui.card().classes('fixed inset-0 z-50 m-4 p-6 shadow-2xl overflow-y-auto').style(f'background-color: {popup_bg}; border-radius: 12px; border: 4px solid {colors["border"]}; max-height: 90vh;'):
                        # X button in top-right corner - Close popup
                        with ui.button(icon='close', on_click=lambda: close_popup()).classes(
                            'absolute top-4 right-4 w-12 h-12 rounded-full bg-red-600 hover:bg-red-800 text-white shadow-xl border-2 border-red-800 font-bold text-xl z-10'):
                            pass
                        
                        # RETURN text button in top-left corner
                        with ui.button('← RETURN', on_click=lambda: close_popup()).classes(
                            'absolute top-4 left-4 px-6 py-3 rounded-lg bg-blue-600 hover:bg-blue-800 text-white shadow-xl border-2 border-blue-800 font-bold text-lg z-10'):
                            pass
                        
                        # Scrollable content area with proper spacing
                        with ui.column().classes('items-center justify-start w-full mt-20 mb-8 px-4'):
                            create_popup_content(current_page['value'])
        
        def show_popup(card_type):
            """Show popup for specific card - no carousel navigation needed"""
            if card_type == 'medical':
                current_page['value'] = 1
            elif card_type == 'insights':
                current_page['value'] = 2
            elif card_type == 'security':
                current_page['value'] = 3
            elif card_type == 'doctor':
                current_page['value'] = 4
            elif card_type == 'complaints':
                current_page['value'] = 5
            create_carousel()
        
        def close_popup():
            """Close popup and return to main cards view"""
            current_page['value'] = 0
            create_carousel()
        
        def create_popup_content(page):
            """Create content for each popup - simple, readable, no navigation"""
            colors = get_card_colors()
            text_sizes = get_responsive_text_sizes()
            content_map = {
                1: {  # Medical Analysis
                    'title': '🔬 Medical Analysis - Advanced Diagnostic Tools',
                    'content': [
                        '✅ AI-Powered Analysis: Advanced machine learning algorithms analyze symptoms and medical history',
                        '✅ Symptom Correlation: Cross-reference symptoms with comprehensive medical databases',
                        '✅ Diagnostic Suggestions: Evidence-based diagnostic recommendations for healthcare providers',
                        '✅ Clinical Decision Support: Real-time guidance and alerts for medical professionals',
                        '✅ Integration Ready: Works seamlessly with existing Electronic Health Record systems'
                    ]
                },
                2: {  # Data Insights - Enhanced with Complaint Tracking
                    'title': '📊 Data Insights - Comprehensive Health Analytics + Complaint Tracking',
                    'content': [
                        '📈 Trend Analysis: Track patient health patterns and changes over time',
                        '📚 Complete Patient History: Integrated view of all medical records and test results',
                        '📊 Population Health Analytics: Statistical insights for improved patient care',
                        '🎯 Predictive Modeling: Advanced risk assessment and prevention strategies',
                        '📋 Custom Reports: Generate detailed reports for physicians and specialists',
                        '',
                        '🚨 COMPLAINT TRACKING FEATURES:',
                        '⏰ Timestamped Documentation: Every complaint automatically timestamped for legal proof',
                        '📸 Evidence Collection: Photos, documents, and records linked to specific complaints',
                        '🔗 Shareable Proof: Secure sharing of timestamped evidence with legal teams or authorities',
                        '📑 Complaint Timeline: Complete chronological record of all incidents and responses',
                        '⚖️ Legal Documentation: Court-ready evidence with verified timestamps and digital signatures'
                    ]
                },
                3: {  # Security & Privacy
                    'title': '🔒 Security & Privacy - HIPAA Compliant Protection',
                    'content': [
                        '�️ End-to-End Encryption: Military-grade 256-bit encryption protects all patient data',
                        '💾 Secure Cloud Storage: HIPAA-compliant infrastructure with redundant backups',
                        '📝 Complete Audit Trails: Every access and action is logged for compliance',
                        '� Role-Based Access: Granular permissions ensure only authorized access',
                        '🏥 Hospital-Grade Security: Meets or exceeds all healthcare industry standards'
                    ]
                },
                4: {  # Your Doctor Loves It!
                    'title': '❤️ Your Doctor Loves It! - Better Care for Everyone',
                    'content': [
                        '⏰ Saves Time: Doctors can focus more time on patient care, not paperwork',
                        '🎯 Better Diagnoses: AI assistance leads to more accurate and faster diagnoses',
                        '📋 Comprehensive Records: Complete patient picture helps doctors make better decisions',
                        '💬 Improved Communication: Clear, organized information improves doctor-patient conversations',
                        '🏆 Happy Patients: When doctors have better tools, patients get the BEST possible care!'
                    ]
                },
                5: {  # Complaints & Documentation - NEW CARD
                    'title': '📝 Complaints & Documentation - Evidence & Accountability',
                    'content': [
                        '🕐 Timestamped Records: Every complaint automatically recorded with precise timestamps',
                        '📸 Evidence Collection: Upload photos, documents, emails, and files as proof',
                        '🔗 Secure Sharing: Share verified evidence with lawyers, insurance, or regulatory bodies',
                        '📊 Pattern Recognition: Identify recurring issues and document systematic problems',
                        '⚖️ Legal Ready: Court-admissible documentation with digital signatures and verification',
                        '',
                        '💡 WHY THIS MATTERS:',
                        '✅ Better Data: Accurate, timestamped records improve accountability',
                        '✅ Legal Protection: Solid evidence protects patients and improves healthcare quality',
                        '✅ System Improvement: Documentation helps identify and fix healthcare system problems',
                        '✅ Patient Rights: Empowers patients with tools to demand better care and accountability'
                    ]
                }
            }
            
            if page in content_map:
                data = content_map[page]
                
                # Title with enhanced accessibility and responsive sizing
                ui.label(data['title']).classes(f'{text_sizes["popup_title"]} font-bold mb-4 sm:mb-6 md:mb-8 text-center').style(f'color: {colors["text"]}')
                
                # Content in easy-to-read format with proper scrolling spacing and responsive text
                with ui.column().classes('space-y-2 sm:space-y-3 md:space-y-4 max-w-4xl w-full'):
                    for item in data['content']:
                        if item == '':  # Empty line for spacing
                            ui.html('<div style="height: 8px; sm:height: 12px;"></div>')
                        else:
                            ui.label(item).classes(f'{text_sizes["popup_content"]} leading-relaxed font-medium text-left').style(f'color: {colors["text"]}; padding: 4px 0; sm:padding: 6px 0; md:padding: 8px 0;')
                
                # Simple instruction at bottom with extra spacing and responsive text
                ui.html('<div style="height: 16px; sm:height: 20px; md:height: 24px;"></div>')  # Extra space before instruction
                ui.label('Click X or RETURN to go back to main cards').classes('text-sm sm:text-base md:text-lg font-bold text-center opacity-75').style(f'color: {colors["text"]}; padding: 12px 0; sm:padding: 14px 0; md:padding: 16px 0;')
        
        # Initialize carousel
        create_carousel()

if __name__ in {"__main__", "__mp_main__"}:
    # Initialize security system
    print("🛡️ Initializing MACS Security System...")
    security = SecurityManager()
    security.apply_security_measures()
    
    # Display security status
    status = security.security_status()
    print(f"🔒 Security Level: {status['level']}")
    
    # Check if PRO features are requested but not licensed
    if status['level'] != 'PRO' and '--pro' in sys.argv:
        print("\n🏥 PRO features requested but not licensed")
        security.request_pro_license()
        sys.exit(0)
    
    try:
        ui.run(
            title=f"MACS - Medical Analysis System ({status['level']} Mode)",
            port=8080,
            show=True,
            reload=True
        )
    except KeyboardInterrupt:
        print("\n🛑 MACS application stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting MACS: {e}")
        print("💡 Try running: pip install nicegui")
        input("Press Enter to exit...")
    finally:
        print("👋 Thank you for using MACS!")
