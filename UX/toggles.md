# Toggle Controls & Interaction Patterns

## Accessibility Toggle System

### 1. Toggle Button Structure
```python
def create_accessibility_controls():
    """Central control system for all UI toggles"""
    accessibility_container.clear()
    with accessibility_container:
        # High Contrast Toggle
        ui.button('🔆 High Contrast', on_click=toggle_contrast).classes(
            'text-xs px-3 py-1 bg-gray-700 text-white'
        )
        
        # Dark Mode Toggle  
        ui.button('🌙 Dark/Light', on_click=toggle_dark_mode).classes(
            'text-xs px-3 py-1 bg-gray-700 text-white'
        )
        
        # Font Size Controls
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

### 2. State Management Pattern
```python
# Global UI state object
ui_state = {
    'high_contrast': False,     # Accessibility enhancement
    'dark_mode': False,         # Theme preference  
    'button_style': 'info',     # Visual style toggle
    'large_text': False,        # Additional text scaling
    'font_size': 'medium'       # Granular font control
}
```

## Toggle Implementation Patterns

### 1. Binary Toggles (On/Off)
```python
def toggle_contrast():
    """High contrast accessibility mode"""
    ui_state['high_contrast'] = not ui_state['high_contrast']
    update_theme()              # Apply visual changes
    create_accessibility_controls()  # Refresh UI
    create_carousel()           # Refresh main content

def toggle_dark_mode():
    """Dark/light theme toggle"""
    ui_state['dark_mode'] = not ui_state['dark_mode']
    update_theme()
    create_accessibility_controls()
    create_carousel()
```

### 2. Multi-State Toggles (Cycle Through Options)
```python
def toggle_button_style():
    """Cycle between button visual styles"""
    ui_state['button_style'] = 'plain' if ui_state['button_style'] == 'info' else 'info'
    create_accessibility_controls()
    create_carousel()

def get_button_icon():
    """Dynamic icon based on current style"""
    return 'info' if ui_state['button_style'] == 'info' else 'chevron_right'
```

### 3. Incremental Toggles (Step Through Levels)
```python
def decrease_font_size():
    """Step down font size: xl → large → medium → small"""
    if ui_state['font_size'] == 'xl':
        ui_state['font_size'] = 'large'
    elif ui_state['font_size'] == 'large':
        ui_state['font_size'] = 'medium'
    elif ui_state['font_size'] == 'medium':
        ui_state['font_size'] = 'small'
    # Stays at 'small' if already smallest
    create_accessibility_controls()
    create_carousel()

def increase_font_size():
    """Step up font size: small → medium → large → xl"""
    if ui_state['font_size'] == 'small':
        ui_state['font_size'] = 'medium'
    elif ui_state['font_size'] == 'medium':
        ui_state['font_size'] = 'large'
    elif ui_state['font_size'] == 'large':
        ui_state['font_size'] = 'xl'
    # Stays at 'xl' if already largest
    create_accessibility_controls()
    create_carousel()
```

## Visual Feedback Patterns

### 1. Button State Indicators
```python
# Current state display
ui.label(f"({ui_state['font_size']})").classes(
    'text-xs text-gray-600 px-1 font-bold'
)

# Visual button states
active_style = 'bg-blue-600 text-white'      # Currently selected
inactive_style = 'bg-gray-700 text-white'    # Available option
disabled_style = 'bg-gray-400 text-gray-200' # Not available
```

### 2. Theme-Responsive Styling
```python
def get_card_colors():
    """Dynamic color scheme based on current theme"""
    if ui_state['high_contrast']:
        return {
            'bg': '#000000',
            'text': '#ffffff', 
            'border': '#ffffff',
            'required': '#00ff00',
            'optional': '#ffff00'
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
```

## Toggle Button Design Standards

### 1. Size & Spacing
```python
# Compact toggle buttons
'text-xs px-3 py-1'        # Standard accessibility toggles
'text-xs px-2 py-1'        # Font size controls (more compact)

# Touch-friendly spacing
'gap-2'                    # Between toggle buttons
'mb-4'                     # Below toggle bar
```

### 2. Color Hierarchy
```python
# Primary toggles (theme/contrast)
'bg-gray-700 text-white'

# Secondary toggles (font controls)  
'bg-blue-600 hover:bg-blue-800 text-white'

# Status indicators
'text-gray-600'            # Current state labels
```

### 3. Hover States
```python
# Subtle hover feedback
'hover:bg-blue-800'        # Darker shade on hover
'transition-all duration-200'  # Smooth transition
```

## Accessibility Toggle Guidelines

### 1. Keyboard Navigation
```python
# Ensure all toggles are keyboard accessible
# Tab order: left to right
# Enter/Space to activate
# Escape to cancel/return
```

### 2. Screen Reader Support
```python
# Descriptive button text
'🔆 High Contrast'         # Icon + text description
'Font Size: Medium'        # Current state announcement
'Toggle Dark Mode'         # Clear action description
```

### 3. Visual Indicators
```python
# Clear state communication
# Color + text (not color alone)
# Consistent button sizing
# Logical grouping
```

## Advanced Toggle Patterns

### 1. Conditional Toggles
```python
def get_responsive_text_sizes():
    """Font size calculation with large_text boost"""
    current_size = ui_state['font_size']
    
    # Large text toggle provides additional boost
    if ui_state['large_text']:
        if current_size == 'small':
            current_size = 'medium'
        elif current_size == 'medium':
            current_size = 'large'
        elif current_size == 'large':
            current_size = 'xl'
        # xl stays xl
    
    return size_map.get(current_size, size_map['medium'])
```

### 2. Cascade Updates
```python
def update_theme():
    """Update page theme and trigger related updates"""
    # 1. Calculate colors
    if ui_state['dark_mode']:
        bg_color = '#1a1a1a' if ui_state['high_contrast'] else '#2d3748'
        text_color = '#ffffff'
    else:
        bg_color = '#ffffff' if ui_state['high_contrast'] else '#f8fafc' 
        text_color = '#000000' if ui_state['high_contrast'] else '#374151'
    
    # 2. Apply CSS changes
    ui.add_head_html(f'''
    <style>
        body {{ 
            background-color: {bg_color}; 
            color: {text_color};
            transition: all 0.3s ease;
        }}
    </style>
    ''')
```

### 3. Persistent State (Future Enhancement)
```python
# Save toggle states to localStorage
# Restore on page reload
# User preference memory
```

## Best Practices

### 1. Immediate Feedback
- Visual change happens instantly
- No loading states for toggles
- Clear before/after states

### 2. Logical Grouping
- Related toggles near each other
- Visual separation between groups
- Consistent interaction patterns

### 3. Graceful Degradation
- Functional without JavaScript
- Accessible fallbacks
- Progressive enhancement approach
