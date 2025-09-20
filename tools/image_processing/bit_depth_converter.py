#!/usr/bin/env python3
"""
Bit Depth Converter Tool

Converts images to lower bit depths (8-bit, 16-bit, 32-bit color palettes) 
for retro-style game graphics. Works with any game engine or framework.

Usage:
    python3 bit_depth_converter.py input.png output.png --bits 8
    python3 bit_depth_converter.py input.jpg output.png --bits 16 --dither
"""

import argparse
import sys
import os
from PIL import Image, ImageDraw
import numpy as np

def create_custom_sprite(image, ncols, nrows, ncolors, pixel_scale=1, use_dithering=True):
    """
    Convert image to custom sprite with specified dimensions and color count.
    
    Args:
        image: PIL Image object
        ncols: Number of columns (width) in pixels
        nrows: Number of rows (height) in pixels  
        ncolors: Number of colors in palette
        pixel_scale: Scale factor for each pixel (1=original size, 4=4x larger)
        use_dithering: Whether to apply dithering
    
    Returns:
        PIL Image as custom sprite
    """
    # Convert to RGB if not already
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize to exact dimensions
    resized = image.resize((ncols, nrows), Image.Resampling.LANCZOS)
    
    # Quantize to specified color count
    dither_mode = Image.FLOYDSTEINBERG if use_dithering else Image.NONE
    quantized = resized.quantize(colors=ncolors, dither=dither_mode)
    sprite = quantized.convert('RGB')
    
    # Scale up pixels if requested
    if pixel_scale > 1:
        final_width = ncols * pixel_scale
        final_height = nrows * pixel_scale
        # Use NEAREST to maintain crisp pixel boundaries
        sprite = sprite.resize((final_width, final_height), Image.Resampling.NEAREST)
    
    return sprite

def create_nes_sprite(image, sprite_size=8, palette_colors=3):
    """
    Convert image to NES-style sprite with authentic constraints.
    
    Args:
        image: PIL Image object
        sprite_size: Target sprite size (8 or 16)
        palette_colors: Number of colors in palette (max 3, +1 for transparency)
    
    Returns:
        PIL Image as NES-style sprite
    """
    # Convert to RGB if not already
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize to sprite dimensions (NES sprites are very small)
    image.thumbnail((sprite_size, sprite_size), Image.Resampling.NEAREST)  # Use NEAREST for blocky pixels
    
    # Create canvas and center the image
    sprite = Image.new('RGB', (sprite_size, sprite_size), (0, 0, 0))
    x_offset = (sprite_size - image.width) // 2
    y_offset = (sprite_size - image.height) // 2
    sprite.paste(image, (x_offset, y_offset))
    
    # Quantize to very limited palette (NES was extremely limited)
    quantized = sprite.quantize(colors=palette_colors, dither=Image.NONE)  # No dithering for crisp pixels
    
    # Convert back to RGB for consistency
    return quantized.convert('RGB')

def create_snes_sprite(image, sprite_size=32, palette_colors=15):
    """
    Convert image to SNES-style sprite with authentic constraints.
    
    Args:
        image: PIL Image object
        sprite_size: Target sprite size (16, 32, or 64)
        palette_colors: Number of colors in palette (max 15, +1 for transparency)
    
    Returns:
        PIL Image as SNES-style sprite
    """
    # Convert to RGB if not already
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize to sprite dimensions while maintaining aspect ratio
    # Use thumbnail to maintain aspect ratio, then center on canvas
    image.thumbnail((sprite_size, sprite_size), Image.Resampling.LANCZOS)
    
    # Create canvas and center the image
    sprite = Image.new('RGB', (sprite_size, sprite_size), (0, 0, 0))
    x_offset = (sprite_size - image.width) // 2
    y_offset = (sprite_size - image.height) // 2
    sprite.paste(image, (x_offset, y_offset))
    
    # Quantize to limited palette with dithering for smooth transitions
    quantized = sprite.quantize(colors=palette_colors, dither=Image.FLOYDSTEINBERG)
    
    # Convert back to RGB for consistency
    return quantized.convert('RGB')

def create_psx_sprite(image, sprite_size=64, palette_colors=16):
    """
    Convert image to PSX-style sprite with authentic constraints.
    
    Args:
        image: PIL Image object
        sprite_size: Target sprite size (32, 64, 128, or 256)
        palette_colors: Number of colors in palette (16 or 256)
    
    Returns:
        PIL Image as PSX-style sprite
    """
    # Convert to RGB if not already
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize to sprite dimensions with better quality (PSX had higher res)
    image.thumbnail((sprite_size, sprite_size), Image.Resampling.LANCZOS)
    
    # Create canvas and center the image
    sprite = Image.new('RGB', (sprite_size, sprite_size), (0, 0, 0))
    x_offset = (sprite_size - image.width) // 2
    y_offset = (sprite_size - image.height) // 2
    sprite.paste(image, (x_offset, y_offset))
    
    # Quantize with dithering for PSX-style gradients
    quantized = sprite.quantize(colors=palette_colors, dither=Image.FLOYDSTEINBERG)
    
    # Convert back to RGB for consistency
    return quantized.convert('RGB')

def reduce_bit_depth(image, target_bits=8, use_dithering=False):
    """
    Reduce image bit depth to create retro-style graphics.
    
    Args:
        image: PIL Image object
        target_bits: Target color depth (8, 16, or 32)
        use_dithering: Whether to apply Floyd-Steinberg dithering
    
    Returns:
        PIL Image with reduced bit depth
    """
    if target_bits == 8:
        colors = 256
    elif target_bits == 16:
        colors = 65536
    elif target_bits == 32:
        colors = 16777216
    else:
        raise ValueError("Supported bit depths: 8, 16, 32")
    
    # Convert to RGB if not already
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    if use_dithering:
        # Use PIL's built-in quantization with dithering
        quantized = image.quantize(colors=colors, dither=Image.FLOYDSTEINBERG)
        return quantized.convert('RGB')
    else:
        # Simple bit reduction
        img_array = np.array(image)
        
        # Calculate reduction factor for each channel
        if target_bits == 8:
            # 8-bit: 3-3-2 RGB (8 colors total per channel roughly)
            r_levels = 8
            g_levels = 8  
            b_levels = 4
        elif target_bits == 16:
            # 16-bit: 5-6-5 RGB
            r_levels = 32
            g_levels = 64
            b_levels = 32
        else:  # 32-bit
            return image  # Already 32-bit
        
        # Reduce bit depth
        img_array[:,:,0] = np.round(img_array[:,:,0] / 255 * (r_levels-1)) * (255 / (r_levels-1))
        img_array[:,:,1] = np.round(img_array[:,:,1] / 255 * (g_levels-1)) * (255 / (g_levels-1))
        img_array[:,:,2] = np.round(img_array[:,:,2] / 255 * (b_levels-1)) * (255 / (b_levels-1))
        
        return Image.fromarray(img_array.astype(np.uint8))

def main():
    parser = argparse.ArgumentParser(
        description="Convert images to lower bit depths for retro game graphics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Custom sprite with exact dimensions, colors, and pixel scaling
  python3 bit_depth_converter.py dog.jpg tiny.png --ncols 16 --nrows 16 --ncolors 8 --pixel-scale 1
  python3 bit_depth_converter.py dog.jpg chunky.png --ncols 16 --nrows 16 --ncolors 8 --pixel-scale 4
  python3 bit_depth_converter.py photo.jpg sprite.png --ncols 24 --nrows 32 --ncolors 12 --pixel-scale 3
  
  # Console presets (still available)
  python3 bit_depth_converter.py dog.jpg nes_dog.png --nes
  python3 bit_depth_converter.py dog.jpg snes_dog.png --snes
  
  # Regular bit depth reduction
  python3 bit_depth_converter.py input.jpg output.png --bits 8 --dither
        """)
    
    parser.add_argument("input", help="Input image file (PNG, JPG, etc.)")
    parser.add_argument("output", help="Output filename (will be saved to ./output_images/)")
    parser.add_argument("--bits", type=int, choices=[8, 16, 32], default=8, 
                       help="Target bit depth (default: 8)")
    parser.add_argument("--dither", action="store_true", 
                       help="Apply Floyd-Steinberg dithering")
    parser.add_argument("--preview", action="store_true",
                       help="Show before/after preview")
    parser.add_argument("--ncols", type=int, 
                       help="Number of columns (width) in output sprite")
    parser.add_argument("--nrows", type=int,
                       help="Number of rows (height) in output sprite") 
    parser.add_argument("--ncolors", type=int,
                       help="Number of colors in output palette")
    parser.add_argument("--pixel-scale", type=int, default=1,
                       help="Scale factor for each pixel (1=tiny, 4=chunky, etc.)")
    parser.add_argument("--nes", action="store_true",
                       help="Create NES-style sprite (8x8, 3 colors)")
    parser.add_argument("--snes", action="store_true",
                       help="Create SNES-style sprite (32x32, 15 colors)")
    parser.add_argument("--psx", action="store_true",
                       help="Create PSX-style sprite (64x64, 16 colors)")
    parser.add_argument("--sprite-size", type=int, default=None,
                       help="Sprite size for console presets")
    parser.add_argument("--palette-colors", type=int, default=None, 
                       help="Number of colors for console presets")
    
    # Show help if no arguments provided
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    args = parser.parse_args()
    
    try:
        # Load image
        print(f"Loading {args.input}...")
        image = Image.open(args.input)
        print(f"Original: {image.size[0]}x{image.size[1]}, {image.mode}")
        
        # Choose conversion method
        if args.ncols and args.nrows and args.ncolors:
            # Custom sprite with specified dimensions and colors
            final_size = f"{args.ncols * args.pixel_scale}x{args.nrows * args.pixel_scale}" if args.pixel_scale > 1 else f"{args.ncols}x{args.nrows}"
            print(f"Creating custom sprite ({args.ncols}x{args.nrows} -> {final_size}, {args.ncolors} colors)...")
            converted = create_custom_sprite(image, args.ncols, args.nrows, args.ncolors, args.pixel_scale, args.dither)
        elif args.nes:
            # NES preset
            sprite_size = args.sprite_size if args.sprite_size else 8
            palette_colors = args.palette_colors if args.palette_colors else 3
            print(f"Creating NES-style sprite ({sprite_size}x{sprite_size}, {palette_colors} colors)...")
            converted = create_nes_sprite(image, sprite_size, palette_colors)
        elif args.snes:
            # SNES preset
            sprite_size = args.sprite_size if args.sprite_size else 32
            palette_colors = args.palette_colors if args.palette_colors else 15
            print(f"Creating SNES-style sprite ({sprite_size}x{sprite_size}, {palette_colors} colors)...")
            converted = create_snes_sprite(image, sprite_size, palette_colors)
        elif args.psx:
            # PSX preset
            sprite_size = args.sprite_size if args.sprite_size else 64
            palette_colors = args.palette_colors if args.palette_colors else 16
            print(f"Creating PSX-style sprite ({sprite_size}x{sprite_size}, {palette_colors} colors)...")
            converted = create_psx_sprite(image, sprite_size, palette_colors)
        else:
            # Default bit depth reduction
            print(f"Converting to {args.bits}-bit depth...")
            converted = reduce_bit_depth(image, args.bits, args.dither)
        
        # Create output directory if it doesn't exist
        output_dir = "./output_images"
        os.makedirs(output_dir, exist_ok=True)
        
        # Build output path
        output_path = os.path.join(output_dir, args.output)
        
        # Save result
        print(f"Saving to {output_path}...")
        converted.save(output_path, "PNG")
        
        # Show preview if requested
        if args.preview:
            # Create side-by-side comparison
            total_width = image.size[0] * 2
            max_height = max(image.size[1], converted.size[1])
            
            comparison = Image.new('RGB', (total_width, max_height))
            comparison.paste(image, (0, 0))
            comparison.paste(converted, (image.size[0], 0))
            
            comparison.show()
        
        print(f"Done! Converted {args.input} to {args.bits}-bit depth.")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()