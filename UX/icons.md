# Icon Library & Usage Guidelines

## Medical Icon Standards

### 1. Primary Function Icons
```python
# Core medical functionality
'medical_services'    # Medical analysis - blue-600
'analytics'          # Data insights - green-600  
'security'           # Privacy/security - purple-600
'favorite'           # Doctor approval - red-600
'assignment'         # Documentation - orange-600
```

### 2. UI Control Icons
```python
# Interface controls
'play_arrow'         # Get started button
'close'              # Close popup/modal
'info'               # Information indicator
'chevron_right'      # Navigation arrow
'settings'           # Settings/preferences
```

### 3. Accessibility Icons
```python
# Accessibility features
'🔆'                 # High contrast toggle
'🌙'                 # Dark mode toggle  
'🔍'                 # Large text toggle
'-T' / 'T+'          # Font size controls
```

## Icon Sizing Standards

### 1. Responsive Sizing
```python
# Card icons - prominent but not overwhelming
'text-2xl sm:text-2xl md:text-3xl'  # 24px → 24px → 30px

# Button icons - functional sizing
'text-lg'                           # 18px (minimum touch target)

# Indicator icons - subtle presence  
'text-xs'                           # 12px (info buttons)
```

### 2. Color Application
```python
# Status-based coloring
required_icons = 'text-blue-600'    # Required functions
optional_icons = 'text-gray-600'    # Optional functions
success_icons = 'text-green-600'    # Positive outcomes
warning_icons = 'text-yellow-600'   # Attention needed
```

## Icon Button Patterns

### 1. Info Indicator Buttons
```python
# Small, non-intrusive status indicators
with ui.button(icon='info').classes(
    'absolute top-1 right-1 w-5 h-5 rounded-full '
    'bg-green-800 hover:bg-green-900 text-white '
    'pointer-events-none text-xs'
):
    pass
```

### 2. Action Buttons
```python
# Primary action buttons with icons
ui.button('Get Started', icon='play_arrow').classes(
    'bg-blue-600 hover:bg-blue-800 text-white '
    'px-8 py-2 font-bold border-2 border-blue-800'
)
```

### 3. Close/Navigation Buttons
```python
# Popup close button
ui.button(icon='close', on_click=close_popup).classes(
    'absolute top-4 right-4 w-12 h-12 rounded-full '
    'bg-red-600 hover:bg-red-800 text-white shadow-xl '
    'border-2 border-red-800 font-bold text-xl'
)
```

## Icon Accessibility

### 1. Text Alternatives
```python
# Always provide text labels with icons
ui.icon('medical_services')
ui.label('Medical Analysis')  # Never icon alone
```

### 2. High Contrast Support
```python
# Ensure icons work in high contrast mode
icon_color = '#ffffff' if ui_state['high_contrast'] else '#2563eb'
```

### 3. Touch Target Requirements
```python
# Minimum 44px for touch targets
'w-12 h-12'  # 48px × 48px (preferred)
'w-11 h-11'  # 44px × 44px (minimum)
```

## Icon Categories by Function

### 1. Medical Functions
- `medical_services` - Primary medical analysis
- `healing` - Treatment recommendations  
- `biotech` - Laboratory results
- `psychology` - Mental health assessments
- `monitor_heart` - Vital signs tracking

### 2. Data & Analytics  
- `analytics` - Data insights and trends
- `assessment` - Evaluation tools
- `trending_up` - Performance metrics
- `insights` - Predictive analysis
- `summarize` - Report generation

### 3. Security & Privacy
- `security` - Data protection
- `verified_user` - User authentication
- `lock` - Encrypted data
- `privacy_tip` - Privacy controls
- `admin_panel_settings` - Access management

### 4. Documentation
- `assignment` - Forms and documents
- `description` - Text documentation
- `attach_file` - File attachments
- `camera_alt` - Photo evidence
- `history` - Timeline records

### 5. Communication
- `message` - Messages and alerts
- `notifications` - System notifications
- `email` - Email communication
- `share` - Sharing capabilities
- `print` - Print functions

## Implementation Best Practices

### 1. Consistency Rules
```python
# Use same icon for same function across app
MEDICAL_ICON = 'medical_services'  # Don't mix with 'local_hospital'
DATA_ICON = 'analytics'            # Don't mix with 'bar_chart'
```

### 2. Icon Loading
```python
# Ensure icons load before content
# Use Material Icons CDN for reliability
# Have fallback text if icons fail
```

### 3. Icon States
```python
# Different states for same icon
default_state = 'text-gray-600'
hover_state = 'hover:text-blue-600' 
active_state = 'text-blue-600'
disabled_state = 'text-gray-400 opacity-50'
```

## Future Icon Considerations

### 1. Custom Medical Icons
- Consider custom SVG icons for unique medical functions
- Maintain consistent stroke width and style
- Ensure scalability at all sizes

### 2. Animation Guidelines
- Subtle hover animations only
- No spinning or bouncing (medical context)
- Focus on professional, calm interactions

### 3. Icon Font Alternatives
- SVG icons for better scaling
- Reduced file size considerations
- Offline functionality requirements
