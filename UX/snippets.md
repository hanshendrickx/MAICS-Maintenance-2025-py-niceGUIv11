# Code Snippets & Implementation Examples

## Responsive Design Snippets

### 1. Font Size System
```python
def get_responsive_text_sizes():
    """18px baseline responsive typography system"""
    size_map = {
        'small': {
            'card_title': 'text-sm sm:text-base md:text-lg lg:text-xl',      # 14→16→18→20px
            'card_subtitle': 'text-xs sm:text-sm md:text-base lg:text-base', # 12→14→16→16px
            'popup_title': 'text-xl sm:text-2xl md:text-3xl lg:text-4xl',
            'popup_content': 'text-base sm:text-lg md:text-xl lg:text-xl'    # 16→18→20→20px
        },
        'medium': {
            'card_title': 'text-base sm:text-lg md:text-xl lg:text-2xl',    # 16→18→20→24px
            'card_subtitle': 'text-sm sm:text-base md:text-lg lg:text-lg',  # 14→16→18→18px
            'popup_title': 'text-2xl sm:text-3xl md:text-4xl lg:text-5xl',
            'popup_content': 'text-lg sm:text-xl md:text-2xl lg:text-2xl'   # 18→20→24→24px
        },
        'large': {
            'card_title': 'text-lg sm:text-xl md:text-2xl lg:text-3xl',     # 18→20→24→30px
            'card_subtitle': 'text-base sm:text-lg md:text-xl lg:text-xl',  # 16→18→20→20px
            'popup_title': 'text-3xl sm:text-4xl md:text-5xl lg:text-6xl',
            'popup_content': 'text-xl sm:text-2xl md:text-3xl lg:text-3xl'  # 20→24→30→30px
        },
        'xl': {
            'card_title': 'text-xl sm:text-2xl md:text-3xl lg:text-4xl',    # 20→24→30→36px
            'card_subtitle': 'text-lg sm:text-xl md:text-2xl lg:text-2xl',  # 18→20→24→24px
            'popup_title': 'text-4xl sm:text-5xl md:text-6xl lg:text-7xl',
            'popup_content': 'text-2xl sm:text-3xl md:text-4xl lg:text-4xl' # 24→30→36→36px
        }
    }
    
    current_size = ui_state['font_size']
    if ui_state['large_text']:
        # Boost one level for additional accessibility
        size_boost = {'small': 'medium', 'medium': 'large', 'large': 'xl', 'xl': 'xl'}
        current_size = size_boost.get(current_size, current_size)
    
    return size_map.get(current_size, size_map['medium'])
```

### 2. Card Layout System
```python
def get_responsive_card_sizes():
    """Mobile-first card dimensions"""
    return {
        'width': 'w-[45%] sm:w-36 md:w-40 lg:w-44 xl:w-48',  # 45% → 144→160→176→192px
        'height': 'h-32 sm:h-28 md:h-32 lg:h-36 xl:h-40',    # 128→112→128→144→160px
        'padding': 'p-3 sm:p-3 md:p-4 lg:p-4',
        'gap': 'gap-2 sm:gap-3 md:gap-4 lg:gap-5',
        'max_width': 'max-w-[180px] sm:max-w-none'
    }
```

## Card Component Template

### 1. Clickable Card Structure
```python
# Professional clickable card with accessibility
with ui.card().classes(
    f'{card_sizes["padding"]} shadow-lg relative cursor-pointer '
    f'transition-all duration-200 hover:translate-y-[-2px] '
    f'{card_sizes["width"]} {card_sizes["height"]} {card_sizes["max_width"]}'
).style(
    f'background-color: {colors["bg"]}; border-radius: 8px; '
    f'border: 2px solid {colors["border"]};'
).on('click', lambda: show_popup('card_type')):
    
    with ui.column().classes('items-center text-center h-full justify-center w-full'):
        # Icon
        ui.icon('medical_services').classes('text-blue-600 mb-1 text-2xl sm:text-2xl md:text-3xl')
        
        # Title
        ui.label('Medical Analysis').classes(
            f'{text_sizes["card_title"]} font-bold text-center'
        ).style(f'color: {colors["text"]}')
        
        # Status
        ui.label('Required').classes(
            f'{text_sizes["card_subtitle"]} font-semibold text-center'
        ).style(f'color: {colors["required"]}')
```

### 2. Info Indicator Button
```python
# Subtle status indicator (optional)
button_icon = get_button_icon()
with ui.button(icon=button_icon).classes(
    'absolute top-1 right-1 w-5 h-5 sm:w-5 sm:h-5 md:w-6 md:h-6 '
    'rounded-full bg-green-800 hover:bg-green-900 text-white '
    'shadow-lg border border-green-900 pointer-events-none '
    'flex items-center justify-center text-xs'
):
    pass
```

## Theme System

### 1. Dynamic Theme Application
```python
def update_theme():
    """Apply theme changes across entire interface"""
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
```

### 2. Color Scheme Generator
```python
def get_card_colors():
    """Context-aware color schemes"""
    if ui_state['high_contrast']:
        return {
            'bg': '#000000', 'text': '#ffffff', 'border': '#ffffff',
            'required': '#00ff00', 'optional': '#ffff00'
        }
    elif ui_state['dark_mode']:
        return {
            'bg': '#2d3748', 'text': '#ffffff', 'border': '#4a5568',
            'required': '#48bb78', 'optional': '#ed8936'
        }
    else:
        return {
            'bg': 'white', 'text': '#374151', 'border': '#e5e7eb',
            'required': '#059669', 'optional': '#6b7280'
        }
```

## Popup/Modal System

### 1. Full-Screen Popup
```python
# Accessible popup with proper navigation
with ui.card().classes(
    'fixed inset-0 z-50 m-4 p-6 shadow-2xl overflow-y-auto'
).style(
    f'background-color: {popup_bg}; border-radius: 12px; '
    f'border: 2px solid {colors["border"]}; max-height: 90vh;'
):
    # Close button
    with ui.button(icon='close', on_click=close_popup).classes(
        'absolute top-4 right-4 w-12 h-12 rounded-full '
        'bg-red-600 hover:bg-red-800 text-white shadow-xl '
        'border-2 border-red-800 font-bold text-xl z-10'
    ):
        pass
    
    # Return button
    with ui.button('← RETURN', on_click=close_popup).classes(
        'absolute top-4 left-4 px-6 py-3 rounded-lg '
        'bg-blue-600 hover:bg-blue-800 text-white shadow-xl '
        'border-2 border-blue-800 font-bold text-lg z-10'
    ):
        pass
    
    # Content area
    with ui.column().classes('items-center justify-start w-full mt-20 mb-8 px-4'):
        create_popup_content(current_page['value'])
```

### 2. Popup Content Template
```python
def create_popup_content(page):
    """Structured popup content with proper typography"""
    colors = get_card_colors()
    text_sizes = get_responsive_text_sizes()
    
    # Title
    ui.label(title).classes(
        f'{text_sizes["popup_title"]} font-bold mb-4 sm:mb-6 md:mb-8 text-center'
    ).style(f'color: {colors["text"]}')
    
    # Content list
    with ui.column().classes('space-y-2 sm:space-y-3 md:space-y-4 max-w-4xl w-full'):
        for item in content_list:
            if item == '':  # Spacing
                ui.html('<div style="height: 8px; sm:height: 12px;"></div>')
            else:
                ui.label(item).classes(
                    f'{text_sizes["popup_content"]} leading-relaxed font-medium text-left'
                ).style(f'color: {colors["text"]}; padding: 4px 0; sm:padding: 6px 0;')
```

## Accessibility Controls

### 1. Toggle Controls Bar
```python
def create_accessibility_controls():
    """Centralized accessibility control system"""
    accessibility_container.clear()
    with accessibility_container:
        # Theme toggles
        ui.button('🔆 High Contrast', on_click=toggle_contrast).classes(
            'text-xs px-3 py-1 bg-gray-700 text-white hover:bg-gray-900'
        )
        ui.button('🌙 Dark/Light', on_click=toggle_dark_mode).classes(
            'text-xs px-3 py-1 bg-gray-700 text-white hover:bg-gray-900'
        )
        
        # Font controls
        ui.button('-T', on_click=decrease_font_size).classes(
            'text-xs px-2 py-1 bg-blue-600 hover:bg-blue-800 text-white font-bold'
        )
        ui.label(f"({ui_state['font_size']})").classes(
            'text-xs text-gray-600 px-1 font-bold'
        )
        ui.button('T+', on_click=increase_font_size).classes(
            'text-xs px-2 py-1 bg-blue-600 hover:bg-blue-800 text-white font-bold'
        )
```

## Animation & Transitions

### 1. Hover Effects
```python
# Subtle professional hover (no scale)
'transition-all duration-200 hover:translate-y-[-2px]'
'hover:shadow-lg'

# Button hover
'hover:bg-blue-800 transition-colors duration-200'
```

### 2. Page Transitions  
```python
# Smooth theme transitions
'transition: all 0.3s ease;'

# Content updates
'transition-opacity duration-200'
```

## Utility Functions

### 1. State Management
```python
def refresh_ui():
    """Refresh all UI components after state change"""
    create_accessibility_controls()
    create_carousel()

def toggle_with_refresh(state_key):
    """Generic toggle with UI refresh"""
    ui_state[state_key] = not ui_state[state_key]
    refresh_ui()
```

### 2. Responsive Utilities
```python
def get_mobile_classes():
    """Mobile-specific CSS classes"""
    return 'flex-wrap gap-2 px-4'

def get_desktop_classes():
    """Desktop-specific CSS classes"""  
    return 'gap-5 px-8'
```

This documentation will help maintain consistency and speed up development when you continue tomorrow!
