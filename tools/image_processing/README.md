# Image Processing Tools

Standalone tools for processing game graphics. These work with any game engine or framework.

## Bit Depth Converter

Converts modern images to retro-style low bit depth graphics perfect for pixel art games.

### Usage

First activate the tools environment:
```bash
cd ../../  # Go to tools directory
source tools_env/bin/activate
cd image_processing
```

Then use the tool:
```bash
# Convert to 8-bit color (256 colors)
python3 bit_depth_converter.py input.jpg output.png --bits 8

# Convert to 16-bit with dithering
python3 bit_depth_converter.py screenshot.png retro.png --bits 16 --dither

# Preview the conversion
python3 bit_depth_converter.py image.png converted.png --bits 8 --preview
```

### Supported Formats
- **Input**: PNG, JPG, BMP, GIF, TIFF
- **Output**: PNG (for best quality preservation)

### Bit Depth Options
- **8-bit**: Classic retro look, ~256 colors
- **16-bit**: Higher quality retro, ~65K colors  
- **32-bit**: Modern quality (mostly unchanged)

### Examples

Perfect for:
- **Doom-style FPS**: Convert textures to 8-bit for authentic retro feel
- **Space shooters**: Reduce sprite bit depth for pixel art aesthetic
- **RTS games**: Convert terrain textures to lower bit depths
- **Any retro-styled game**: Consistent low-fi art direction

### Dependencies

```bash
pip install pillow numpy
```

## Future Tools

Other image processing tools to be added:
- Sprite sheet generator
- Palette extractor/replacer
- Texture tiling generator
- Normal map converter