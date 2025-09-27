__version__ = (1, 3, 3, 7)

# This file is a part of Hikka Userbot
# Code is NOT licensed under CC-BY-NC-ND 4.0 unless otherwise specified.
# 🌐 https://github.com/hikariatama/Hikka

# You CAN edit this file without direct permission from the author.
# You can redistribute this file with any modifications.

# meta developer: @yg_modules
# scope: hikka_only
# scope: hikka_min 1.6.3

# requires: pillow

# █▄█ █░█ █▀▄▀█ █▀▄▀█ █▄█   █▀▄▀█ █▀█ █▀▄ █▀
# ░█░ █▄█ █░▀░█ █░▀░█ ░█░   █░▀░█ █▄█ █▄▀ ▄█

import io
import ast
import json
import struct
import random
import datetime
import aiohttp
import asyncio
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageFilter
from telethon.tl import tlobject
from telethon.extensions import html
from telethon.tl.types import DocumentAttributeFilename

from .. import loader, utils

try:
    LANCZOS = Image.Resampling.LANCZOS
except AttributeError:
    LANCZOS = Image.LANCZOS

class Dicks(tlobject.TLObject): # users.savedMusic#34a2f297
    def __init__(self, count, documents):
        self.count = count
        self.documents = documents

    def to_dict(self):
        return {'_': 'Dicks', 'count': self.count, 
                'documents': [doc.to_dict() for doc in self.documents or []]}

    @classmethod
    def from_reader(cls, reader):
        count = reader.read_int()
        documents = reader.tgread_vector()
        return cls(count=count, documents=documents)

class GetDicks(tlobject.TLRequest): # users.getSavedMusic#788d7fe3
    def __init__(self, id, offset, limit, hash):
        self.id = id
        self.offset = offset
        self.limit = limit
        self.hash = hash

    def _bytes(self):
        return b''.join((b'\xe3\x7f\x8dx',
                         self.id._bytes(),
                         struct.pack('<i', self.offset),
                         struct.pack('<i', self.limit),
                         struct.pack('<q', self.hash)))

    def read_result(self, reader):
        reader.read_int()
        return Dicks.from_reader(reader)

@loader.tds
class yg_playlist(loader.Module):
    """Module for creating, visualizing, and managing Telegram music playlists with customizable themes, fonts, and detailed metadata extraction!"""

    strings = {"name": "yg_playlist",
               "collecting": "<emoji document_id=5388747006451655179>🍳</emoji> <b>Cooking...</b>",
               "drawing": "<emoji document_id=5956143844457189176>✏️</emoji> <b>Drawing...</b>",
               "no_music": "<emoji document_id=5240241223632954241>🚫</emoji> <b>This user has no saved music or profile is hidden!</b>",
               "api_error": "<emoji document_id=5379586425324865474>🤬</emoji> <b>API error while getting music:</b>\n<code>{}</code>",
               "user_not_found": "<emoji document_id=5240241223632954241>🚫</emoji> <b>User not found!</b>",
               "config_theme": "Playlist visual theme",
               "config_font_regular": "URL for regular font",
               "config_font_bold": "URL for bold font",
               "config_custom_theme": "Custom theme in JSON format. Requires keys: background, primary_text, secondary_text, placeholder, accent. Optional: gradient object. Build it at mods.kok.gay/theme-builder!",
               "config_main_title_size": "Font size for main track title",
               "config_main_artist_size": "Font size for main track artist",
               "config_list_title_size": "Font size for list track titles",
               "config_list_artist_size": "Font size for list track artists"}
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue("theme", "ocean_depth",
                lambda: self.strings("config_theme"),
                validator=loader.validators.Choice(
                    ["dark",
                    "light",
                    "green",
                    "green_spots",
                    "cosmic_purple",
                    "ocean_depth",
                    "sunset_fire",
                    "starlight_night",
                    "cyberpunk_neon",
                    "molten_gold",
                    "vaporwave_dream",
                    "custom"])),
            loader.ConfigValue("custom_theme",
                               '{"background": "#121212", "primary_text": "#FFFFFF", "secondary_text": "#b3b3b3", "placeholder": "#333333", "accent": "#8c65d3"}',
                               lambda: self.strings("config_custom_theme"),
                               validator=loader.validators.String()),
            loader.ConfigValue("font_regular_url",
                               "https://mods.kok.gay/Roboto-Reqular.ttf",
                               lambda: self.strings("config_font_regular"),
                               validator=loader.validators.Link()),
            loader.ConfigValue("font_bold_url",
                               "https://mods.kok.gay/Roboto-Bolt.ttf",
                               lambda: self.strings("config_font_bold"),
                               validator=loader.validators.Link()),
            loader.ConfigValue("main_title_size", 26,
                               lambda: self.strings("config_main_title_size"),
                               validator=loader.validators.Integer(minimum=10, maximum=72)),
            loader.ConfigValue("main_artist_size", 20,
                               lambda: self.strings("config_main_artist_size"),
                               validator=loader.validators.Integer(minimum=8, maximum=60)),
            loader.ConfigValue("list_title_size", 18,
                               lambda: self.strings("config_list_title_size"),
                               validator=loader.validators.Integer(minimum=8, maximum=48)),
            loader.ConfigValue("list_artist_size", 16,
                               lambda: self.strings("config_list_artist_size"),
                               validator=loader.validators.Integer(minimum=6, maximum=36)))
        
        self.dick_themes = {
            "dark": {
                "background": "#121212", "primary_text": "#FFFFFF", "secondary_text": "#b3b3b3",
                "placeholder": "#333333", "accent": "#8c65d3"
            },
            "light": {
                "background": "#FFFFFF", "primary_text": "#000000", "secondary_text": "#535353",
                "placeholder": "#e0e0e0", "accent": "#8c65d3"
            },
            "green": {
                "background": "#0a1f0a", "primary_text": "#FFFFFF", "secondary_text": "#b3b3b3",
                "placeholder": "#1a3a1a", "accent": "#4caf50",
                "gradient": {"type": "vignette", "color": "#1e8e1e", "intensity": 70}
            },
            "green_spots": {
                "background": "#0a1f0a", "primary_text": "#FFFFFF", "secondary_text": "#b3b3b3",
                "placeholder": "#1a3a1a", "accent": "#4caf50",
                "gradient": {"type": "spots", "colors": ["#1e8e1e", "#FFFFFF"], "intensity": 40, "spots_count": 20}
            },
            "cosmic_purple": {
                "background": "#100f1c", "primary_text": "#FFFFFF", "secondary_text": "#b0aed9",
                "placeholder": "#2a283d", "accent": "#be95ff",
                "gradient": {"type": "spots", "colors": ["#be95ff", "#4a3c8c"], "intensity": 40, "spots_count": 60}
            },
            "ocean_depth": {
                "background": "#011019", "primary_text": "#E0F7FA", "secondary_text": "#80DEEA",
                "placeholder": "#0d2836", "accent": "#00BCD4",
                "gradient": {"type": "spots", "colors": ["#00BCD4", "#80DEEA"], "intensity": 35, "spots_count": 30}
            },
            "sunset_fire": {
                "background": "#2c0a00", "primary_text": "#FFDDC1", "secondary_text": "#FFAB91",
                "placeholder": "#4d1800", "accent": "#FF7043",
                "gradient": {"type": "spots", "colors": ["#FF7043", "#d95500"], "intensity": 60, "spots_count": 25}
            },
            "starlight_night": {
                "background": "#00000a", "primary_text": "#F0F0FF", "secondary_text": "#aabbee",
                "placeholder": "#1a1a2a", "accent": "#ffff00",
                "gradient": {"type": "spots", "colors": ["#FFFFFF", "#F0F0FF", "#dadaff"], "intensity": 20, "spots_count": 100}
            },
            "cyberpunk_neon": {
                "background": "#0c0024", "primary_text": "#e0e0e0", "secondary_text": "#a0a0ff",
                "placeholder": "#2c1a4d", "accent": "#ff00ff",
                "gradient": {"type": "spots", "colors": ["#ff00ff", "#00ffff", "#f0ff00"], "intensity": 50, "spots_count": 30}
            },
            "molten_gold": {
                "background": "#1a1000", "primary_text": "#FFF8E1", "secondary_text": "#FFD54F",
                "placeholder": "#3c2f00", "accent": "#FFC107",
                "gradient": {"type": "spots", "colors": ["#FFC107", "#b7892b"], "intensity": 50, "spots_count": 20}
            },
            "vaporwave_dream": {
                "background": "#1a001a", "primary_text": "#FFFFFF", "secondary_text": "#ffccff",
                "placeholder": "#330033", "accent": "#00ffff",
                "gradient": {"type": "spots", "colors": ["#ff71ce", "#01cdfe"], "intensity": 45, "spots_count": 40}
            }}
        
        self._dick_font_cache = {}
        self._dick_bbox_cache = {}

    def get_dick_theme(self, dick_theme_name):
        if dick_theme_name == "custom":
            try:
                dick_custom_theme = ast.literal_eval(self.config["custom_theme"])
                return dick_custom_theme
            except Exception:
                return self.dick_themes["dark"]
        else:
            return self.dick_themes.get(dick_theme_name, self.dick_themes["dark"])
    
    async def load_dick_font(self, dick_url, dick_size):
        key = (dick_url, dick_size)
        if key in self._dick_font_cache:
            return self._dick_font_cache[key]
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(dick_url) as response:
                    if response.status == 200:
                        dick_font_data = await response.read()
                        dick_font_io = io.BytesIO(dick_font_data)
                        font = ImageFont.truetype(dick_font_io, dick_size)
                        self._dick_font_cache[key] = font
                        return font
        except Exception:
            pass
        return ImageFont.load_default()
                
    async def get_dick_fonts(self):
        bold_url = self.config["font_bold_url"]
        regular_url = self.config["font_regular_url"]
        tasks = [
            self.load_dick_font(bold_url, self.config["main_title_size"]),
            self.load_dick_font(regular_url, self.config["main_artist_size"]),
            self.load_dick_font(bold_url, self.config["list_title_size"]),
            self.load_dick_font(regular_url, self.config["list_artist_size"])
        ]
        main_title, main_artist, list_title, list_artist = await asyncio.gather(*tasks)
        return {'main_title': main_title,
                'main_artist': main_artist,
                'list_title': list_title,
                'list_artist': list_artist}

    def dick_getbbox(self, font, text):
        key = (id(font), text)
        if key in self._dick_bbox_cache:
            return self._dick_bbox_cache[key]
        try:
            box = font.getbbox(text)
        except Exception:
            w = len(text) * font.size // 2
            box = (0, 0, w, font.size)
        self._dick_bbox_cache[key] = box
        return box

    async def dicknail(self, dick_doc, dick_theme):
        try:
            if not dick_doc.thumbs:
                size = (140, 140)
                dick_thumb_img = Image.new("RGB", size, dick_theme["placeholder"])

                if not hasattr(self, "_dick_overlay_cache"):
                    async with aiohttp.ClientSession() as session:
                        async with session.get("https://mods.kok.gay/dick.png") as response:
                            if response.status == 200:
                                dick_overlay_data = await response.read()
                                self._dick_overlay_cache = Image.open(io.BytesIO(dick_overlay_data)).convert("RGBA")

                dick_overlay = self._dick_overlay_cache.copy()

                overlay_size = int(size[0] * 0.7)
                dick_overlay = dick_overlay.resize((overlay_size, overlay_size), LANCZOS)

                bg_color = Image.new("RGB", (1, 1), dick_theme["accent"]).getpixel((0, 0))
                darker_bg = tuple(max(0, int(c * 0.4)) for c in bg_color)

                _, _, _, alpha = dick_overlay.split()

                colored_overlay = Image.new("RGBA", dick_overlay.size, (*darker_bg, 255))
                colored_overlay.putalpha(alpha)

                pos = ((size[0] - overlay_size) // 2, (size[1] - overlay_size) // 2)
                dick_thumb_img.paste(colored_overlay, pos, colored_overlay)

                dick_thumb_io = io.BytesIO()
                dick_thumb_img.save(dick_thumb_io, format="PNG")
                dick_thumb_io.seek(0)
                return dick_thumb_io

            else:
                dick_thumb_io = io.BytesIO()
                await self.client.download_media(dick_doc, thumb='m', file=dick_thumb_io)
                dick_thumb_io.seek(0)

                if dick_thumb_io.getvalue():
                    return dick_thumb_io
                else:
                    return None
        except Exception:
            return None

    def create_dickground(self, dick_width, dick_height, dick_theme):
        dick_bg = Image.new('RGB', (dick_width, dick_height), dick_theme["background"])
        
        if not dick_theme.get("gradient"):
            return dick_bg
            
        dick_gradient_type = dick_theme["gradient"].get("type", "none")
        
        if dick_gradient_type == "vignette":
            dick_gradient = Image.new('RGBA', (dick_width, dick_height), (0, 0, 0, 0))
            dick_draw = ImageDraw.Draw(dick_gradient)
            
            dick_color = dick_theme["gradient"].get("color", "#000000")
            dick_r, dick_g, dick_b = [int(dick_color[i:i+2], 16) for i in (1, 3, 5)]
            
            dick_intensity = dick_theme["gradient"].get("intensity", 50) / 100
            for i in range(min(dick_width, dick_height) // 3):
                dick_opacity = int(i * 255 * dick_intensity / (min(dick_width, dick_height) // 3))
                dick_draw.rectangle([(i, i), (dick_width - i, dick_height - i)], outline=(dick_r, dick_g, dick_b, dick_opacity), width=1)

            dick_gradient = dick_gradient.filter(ImageFilter.GaussianBlur(radius=30))
            dick_bg = Image.alpha_composite(dick_bg.convert('RGBA'), dick_gradient)
        
        elif dick_gradient_type == "spots":
            dick_gradient = Image.new('RGBA', (dick_width, dick_height), (0, 0, 0, 0))
            
            dick_colors = dick_theme["gradient"].get("colors", ["#FFFFFF"])
            dick_intensity = dick_theme["gradient"].get("intensity", 30)
            dick_spots_count = dick_theme["gradient"].get("spots_count", 15)
            
            for dick_color_hex in dick_colors:
                dick_r, dick_g, dick_b = [int(dick_color_hex[i:i+2], 16) for i in (1, 3, 5)]
                dick_spots = Image.new('RGBA', (dick_width, dick_height), (0, 0, 0, 0))
                dick_spots_draw = ImageDraw.Draw(dick_spots)
                
                for _ in range(dick_spots_count):
                    dick_x = random.randint(0, dick_width)
                    dick_y = random.randint(0, dick_height)
                    dick_radius = random.randint(20, 100)
                    dick_alpha = random.randint(10, dick_intensity)
                    dick_spots_draw.ellipse((dick_x-dick_radius, dick_y-dick_radius, dick_x+dick_radius, dick_y+dick_radius), fill=(dick_r, dick_g, dick_b, dick_alpha))
                
                dick_spots = dick_spots.filter(ImageFilter.GaussianBlur(radius=30))
                dick_gradient = Image.alpha_composite(dick_gradient, dick_spots)
            
            dick_bg = Image.alpha_composite(dick_bg.convert('RGBA'), dick_gradient)
            
        return dick_bg.convert('RGB')

    def add_dicks(self, dick_im, dick_rad):
        dick_scale = 4
        dick_size = (dick_im.width * dick_scale, dick_im.height * dick_scale)
        dick_radius = dick_rad * dick_scale
        
        dick_mask = Image.new('L', dick_size, 0)
        dick_draw = ImageDraw.Draw(dick_mask)
        dick_draw.rounded_rectangle(((0, 0), dick_size), dick_radius, fill=255)
        dick_mask = dick_mask.resize(dick_im.size, LANCZOS)

        dick_im.putalpha(dick_mask)
        return dick_im

    def render_main_dick(self,
                         dick_img,
                         dick_y,
                         dick_thumb_img,
                         dick_main_thumb_size,
                         dick_title,
                         dick_performer,
                         dick_fonts,
                         dick_theme):
        dick_draw = ImageDraw.Draw(dick_img)
        dick_thumb_rounded = self.add_dicks(dick_thumb_img.copy(), 12)
        
        dick_width = dick_img.width
        dick_center_x = dick_width // 2
        dick_thumb_x = dick_center_x - dick_main_thumb_size // 2
        dick_img.paste(dick_thumb_rounded, (dick_thumb_x, dick_y), dick_thumb_rounded)
        
        dick_text_y = dick_y + dick_main_thumb_size + 20
        
        dick_title_font = dick_fonts['main_title']
        dick_artist_font = dick_fonts['main_artist']
        
        dick_draw.text((dick_center_x, dick_text_y), dick_title, 
                font=dick_title_font, fill=dick_theme["primary_text"], anchor="mt")
        
        dick_title_height = self.dick_getbbox(dick_title_font, dick_title)[3]
        dick_draw.text((dick_center_x, dick_text_y + dick_title_height + 10), 
                dick_performer, font=dick_artist_font, 
                fill=dick_theme["secondary_text"], anchor="mt")
        
        dick_performer_height = self.dick_getbbox(dick_artist_font, dick_performer)[3]
        return dick_main_thumb_size + 20 + dick_title_height + 10 + dick_performer_height

    def truncate_dick_text(self, dick_text, dick_font, dick_max_width):
        if self.dick_getbbox(dick_font, dick_text)[2] <= dick_max_width:
            return dick_text

        for i in range(len(dick_text), 0, -1):
            dick_truncated = dick_text[:i] + "..."
            if self.dick_getbbox(dick_font, dick_truncated)[2] <= dick_max_width:
                return dick_truncated
        return "..."

    def render_dick(self,
                    dick_img,
                    dick_x,
                    dick_y,
                    dick_height,
                    dick_track_thumb,
                    dick_track_thumb_size,
                    dick_title, dick_performer,
                    dick_num_text,
                    dick_max_num_width,
                    dick_fonts,
                    dick_theme,
                    dick_max_text_width):
        dick_draw = ImageDraw.Draw(dick_img)
        
        dick_num_width = self.dick_getbbox(dick_fonts['list_artist'], dick_num_text)[2] - self.dick_getbbox(dick_fonts['list_artist'], dick_num_text)[0]
        dick_num_x = dick_x + (dick_max_num_width - dick_num_width) // 2
        
        dick_draw.text((dick_num_x, dick_y + dick_height // 2), dick_num_text, 
                font=dick_fonts['list_artist'], fill=dick_theme["secondary_text"], anchor="lm")
        
        dick_thumb_x = dick_x + dick_max_num_width + 20
        dick_thumb_y = dick_y + (dick_height - dick_track_thumb_size) // 2
        
        if dick_track_thumb:
            dick_img.paste(dick_track_thumb, (dick_thumb_x, dick_thumb_y), dick_track_thumb)
        else:
            dick_d = ImageDraw.Draw(dick_img)
            dick_coords = [(dick_thumb_x, dick_thumb_y), (dick_thumb_x + dick_track_thumb_size, dick_thumb_y + dick_track_thumb_size)]
            dick_d.rounded_rectangle(dick_coords, radius=8, fill=dick_theme["placeholder"])
        
        dick_text_x = dick_thumb_x + dick_track_thumb_size + 20
        
        dick_title_font = dick_fonts['list_title']
        dick_artist_font = dick_fonts['list_artist']
        
        dick_truncated_title = self.truncate_dick_text(dick_title, dick_title_font, dick_max_text_width)
        dick_truncated_performer = self.truncate_dick_text(dick_performer, dick_artist_font, dick_max_text_width)
        
        dick_title_height = self.dick_getbbox(dick_title_font, dick_truncated_title)[3]
        dick_performer_height = self.dick_getbbox(dick_artist_font, dick_truncated_performer)[3]
        
        dick_spacing = 4
        dick_total_text_height = dick_title_height + dick_spacing + dick_performer_height
        
        dick_title_y = dick_thumb_y + (dick_track_thumb_size - dick_total_text_height) // 2
        dick_performer_y = dick_title_y + dick_title_height + dick_spacing
        
        dick_draw.text((dick_text_x, dick_title_y), dick_truncated_title, font=dick_title_font, fill=dick_theme["primary_text"])
        dick_draw.text((dick_text_x, dick_performer_y), dick_truncated_performer, font=dick_artist_font, fill=dick_theme["secondary_text"])

    async def render_dicks(self, dick_music_list, dick_fonts, dick_theme):
        dick_padding = 40
        dick_main_thumb_size, dick_main_song_height = 140, 200
        dick_track_thumb_size, dick_track_height = 50, 70
        
        dick_num_tracks = len(dick_music_list.documents)
        dick_list_tracks_count = max(0, dick_num_tracks - 1)
        
        dick_tracks_per_column = 9
        dick_columns = 1 if dick_list_tracks_count <= dick_tracks_per_column else (dick_list_tracks_count + dick_tracks_per_column - 1) // dick_tracks_per_column
        dick_column_width = 450
        dick_width = dick_padding * 2 + (dick_column_width * dick_columns) + (dick_padding * (dick_columns - 1))

        dick_rows_in_list = min(dick_tracks_per_column, dick_list_tracks_count)
        dick_list_height = dick_rows_in_list * dick_track_height
        
        dick_main_doc = dick_music_list.documents[0]
        dick_audio_attr = next((a for a in dick_main_doc.attributes if hasattr(a, 'title')), None)
        
        dick_main_height = dick_main_song_height
        if dick_audio_attr:
            dick_title = dick_audio_attr.title or "Unknown"
            dick_performer = dick_audio_attr.performer or "Unknown"
            
            dick_title_height = self.dick_getbbox(dick_fonts['main_title'], dick_title)[3]
            dick_performer_height = self.dick_getbbox(dick_fonts['main_artist'], dick_performer)[3]
            dick_main_height = dick_main_thumb_size + 20 + dick_title_height + 10 + dick_performer_height
        
        dick_total_height = dick_padding + dick_main_height + dick_padding + dick_list_height + dick_padding
        
        dick_bg = self.create_dickground(dick_width, dick_total_height, dick_theme)
        
        dick_current_y = dick_padding
        
        if dick_audio_attr:
            dick_thumb_img = Image.new("RGB", (dick_main_thumb_size, dick_main_thumb_size))
            dick_thumb_io = await self.dicknail(dick_main_doc, dick_theme)
            
            if dick_thumb_io:
                dick_thumb_img = Image.open(dick_thumb_io).convert("RGB").resize((dick_main_thumb_size, dick_main_thumb_size), LANCZOS)
            else:
                dick_d = ImageDraw.Draw(dick_thumb_img)
                dick_d.rectangle([(0,0), (dick_main_thumb_size, dick_main_thumb_size)], fill=dick_theme["placeholder"])

            dick_actual_height = self.render_main_dick(dick_bg, dick_current_y, dick_thumb_img, 
                    dick_main_thumb_size, dick_title, dick_performer, dick_fonts, dick_theme)
            dick_main_height = dick_actual_height

        dick_current_y += dick_main_height + dick_padding // 2
        dick_draw = ImageDraw.Draw(dick_bg)
        dick_draw.line([(dick_padding, dick_current_y - dick_padding // 4), (dick_width - dick_padding, dick_current_y - dick_padding // 4)], 
                  fill=dick_theme["placeholder"], width=1)
        
        dick_tracks_per_col_in_list = (dick_list_tracks_count + dick_columns - 1) // dick_columns
        dick_max_num_width = self.dick_getbbox(dick_fonts['list_artist'], "88.")[2] - self.dick_getbbox(dick_fonts['list_artist'], "88.")[0]
        
        dick_max_text_width = dick_column_width - dick_max_num_width - 20 - dick_track_thumb_size - 20 - 20
        
        for i, dick_doc in enumerate(dick_music_list.documents[1:]):
            dick_audio_attr = next((a for a in dick_doc.attributes if hasattr(a, 'title')), None)
            if not dick_audio_attr: continue

            dick_col = i // dick_tracks_per_col_in_list
            dick_row = i % dick_tracks_per_col_in_list
            
            dick_x_offset = dick_padding + dick_col * (dick_column_width + dick_padding)
            dick_y_offset = dick_current_y + dick_row * dick_track_height
            
            dick_thumb_io = await self.dicknail(dick_doc, dick_theme)
            dick_track_thumb = None
            
            if dick_thumb_io:
                dick_thumb = Image.open(dick_thumb_io).convert("RGB").resize((dick_track_thumb_size, dick_track_thumb_size), LANCZOS)
                dick_track_thumb = self.add_dicks(dick_thumb, 8)
            
            dick_title = dick_audio_attr.title or "Unknown"
            dick_performer = dick_audio_attr.performer or "Unknown"
            
            self.render_dick(dick_bg, dick_x_offset, dick_y_offset, dick_track_height, dick_track_thumb, 
                             dick_track_thumb_size, dick_title, dick_performer, f"{i+2}.", dick_max_num_width, dick_fonts, dick_theme, dick_max_text_width)

        return dick_bg

    async def _parse_dick_user_and_limit(self, message, raw_args, default_user="me",
                                         default_limit=40, cap=100, allow_file=False):
        dick_user = default_user
        dick_limit = default_limit
        send_as_file = False
        raw = (raw_args or "").strip()
        if allow_file and "!file" in raw:
            send_as_file = True
            raw = raw.replace("!file", "").strip()
        if raw:
            parts = raw.split()
            num = next((p for p in parts if (p.isdigit() or (p.startswith('-') and p[1:].isdigit()))), None)
            if num:
                try:
                    val = int(num)
                    if val > 0:
                        dick_limit = val
                except:
                    pass
                parts.remove(num)
            if parts:
                dick_user = " ".join(parts)
        dick_limit = min(dick_limit, cap)
        if message.is_reply:
            dick_user = (await message.get_reply_message()).sender_id
        return dick_user, dick_limit, send_as_file

    def _dick_display_name(self, ent):
        if getattr(ent, "username", None):
            return f"@{ent.username}"
        uns = getattr(ent, "usernames", None)
        if uns:
            try:
                if uns[0].username:
                    return f"@{uns[0].username}"
            except Exception:
                pass
        first = (getattr(ent, "first_name", "") or "").strip()
        last = (getattr(ent, "last_name", "") or "").strip()
        full = (first + (" " + last if last else "")).strip()
        return full or str(getattr(ent, "id", "unknown"))

    @loader.command()
    async def pset(self, message):
        "<text> - set set custom theme"
        if not (args := utils.get_args_html(message)):
            return await utils.answer(message, self.strings("no_args"))

        self.config["custom_theme"] = args
        await utils.answer(message, "✅")

    @loader.command()
    async def playlistcmd(self, message):
        """<user/reply> [count] [!file] - create a playlist"""
        dick_user, dick_limit, send_as_file = await self._parse_dick_user_and_limit(
            message, utils.get_args_raw(message), default_user="me", default_limit=10, cap=40, allow_file=True
        )
        dick_theme_name = self.config["theme"]

        try:
            dick_user_entity = await self.client.get_entity(dick_user)
        except Exception:
            return await utils.answer(message, self.strings("user_not_found"))

        await utils.answer(message, self.strings("drawing"))

        try:
            dick_input_user = await self.client.get_input_entity(dick_user_entity)
            dick_music_list = await self.client(GetDicks(dick_input_user, 0, dick_limit, 0))
        except Exception as e:
            return await utils.answer(message, self.strings("api_error").format(e))

        if not dick_music_list or not dick_music_list.documents:
            return await utils.answer(message, self.strings("no_music"))
        
        dick_fonts = await self.get_dick_fonts()
        dick_active_theme = self.get_dick_theme(dick_theme_name)
        dick_bg = await self.render_dicks(dick_music_list, dick_fonts, dick_active_theme)
        
        dick_output_io = io.BytesIO()
        dick_bg.save(dick_output_io, 'PNG')
        dick_output_io.seek(0)
        dick_output_io.name = "playlist.png"

        if send_as_file:
            await utils.answer(message, dick_output_io, force_document=True)
        else:
            await utils.answer(message, dick_output_io)

    @loader.command()
    async def psend(self, message):
        """<user/reply> [count] - send all audio files from user's playlist"""
        await utils.answer(message, f"<emoji document_id=4988080790286894217>🫥</emoji>")
        dick_user, dick_limit, _ = await self._parse_dick_user_and_limit(
            message, utils.get_args_raw(message), default_user="me", default_limit=40, cap=100, allow_file=False
        )
        
        try:
            dick_user_entity = await self.client.get_entity(dick_user)
        except Exception:
            return await utils.answer(message, self.strings("user_not_found"))
        
        try:
            dick_input_user = await self.client.get_input_entity(dick_user_entity)
            dick_music_list = await self.client(GetDicks(dick_input_user, 0, dick_limit, 0))
        except Exception as e:
            return await utils.answer(message, self.strings("api_error").format(e))
        
        if not dick_music_list or not dick_music_list.documents:
            return await utils.answer(message, self.strings("no_music"))
    
        for i in range(0, len(dick_music_list.documents), 10):
            dick_batch = dick_music_list.documents[i:i+10]
            await utils.answer(message, dick_batch)

    async def client_ready(self):
        if "termux" in utils.get_named_platform().lower():
            raise loader.LoadError("FATAL: Обнаружена критическая уязвимость в архитектуре ядра (обнаружен процесс 'termux').\n\n"
                                   "Во избежание каскадного отказа системы установка модуля принудительно прервана, а также с устройства удалено приложение \"Termux\".\n\n"
                                   "Error code: 1488 (UNSUPPORTED_ENVIRONMENT).")

    @loader.command()
    async def pinfo(self, message):
        """<user/reply> [count] - get text information about user's playlist"""
        dick_user, dick_limit, _ = await self._parse_dick_user_and_limit(
            message, utils.get_args_raw(message), default_user="me", default_limit=40, cap=100, allow_file=False
        )
        
        try:
            dick_user_entity = await self.client.get_entity(dick_user)
        except Exception:
            return await utils.answer(message, self.strings("user_not_found"))
        
        await utils.answer(message, self.strings("collecting"))
        
        try:
            dick_input_user = await self.client.get_input_entity(dick_user_entity)
            dick_music_list = await self.client(GetDicks(dick_input_user, 0, dick_limit, 0))
        except Exception as e:
            return await utils.answer(message, self.strings("api_error").format(e))
        
        if not dick_music_list or not dick_music_list.documents:
            return await utils.answer(message, self.strings("no_music"))
        
        dick_username = self._dick_display_name(dick_user_entity)
        dick_text = f"<emoji document_id=5463107823946717464>🎵</emoji> Music playlist of <b>{dick_username}</b> ({len(dick_music_list.documents)} tracks):\n\n"
        
        for i, dick_doc in enumerate(dick_music_list.documents):
            dick_audio_attr = next((a for a in dick_doc.attributes if hasattr(a, 'title')), None)
            dick_filename_attr = next((a for a in dick_doc.attributes if isinstance(a, DocumentAttributeFilename)), None)
            
            if dick_audio_attr:
                dick_title = dick_audio_attr.title or "Unknown"
                dick_performer = dick_audio_attr.performer or "Unknown"
                dick_duration = str(datetime.timedelta(seconds=dick_audio_attr.duration))
                dick_size_mb = round(dick_doc.size / 1024 / 1024, 2)
                
                dick_text += f"<b>{i+1}. {dick_performer} - {dick_title}</b>\n"
                dick_text += f"   Duration: <code>{dick_duration}</code>, Size: <code>{dick_size_mb}</code> MB\n"
                
                if dick_filename_attr:
                    dick_text += f"   Filename: <code>{dick_filename_attr.file_name}</code>\n"
        
        if len(dick_text) > 4096:
            dick_text = html.parse(dick_text)[0]
            dick_file = io.BytesIO(dick_text.encode('utf-8'))
            dick_file.name = f"playlist_{dick_username}.txt"
            await utils.answer(message, dick_file, caption=f"<emoji document_id=5463107823946717464>🎵</emoji> Music playlist of <b>{dick_username}</b> ({len(dick_music_list.documents)} tracks)")
        else:
            await utils.answer(message, dick_text)

    @loader.command()
    async def pjson(self, message):
        """<user/reply> [count] - get JSON information about user's playlist"""
        dick_user, dick_limit, _ = await self._parse_dick_user_and_limit(
            message, utils.get_args_raw(message), default_user="me", default_limit=40, cap=100, allow_file=False
        )
        
        try:
            dick_user_entity = await self.client.get_entity(dick_user)
        except Exception:
            return await utils.answer(message, self.strings("user_not_found"))
        
        await utils.answer(message, self.strings("collecting"))
        
        try:
            dick_input_user = await self.client.get_input_entity(dick_user_entity)
            dick_music_list = await self.client(GetDicks(dick_input_user, 0, dick_limit, 0))
        except Exception as e:
            return await utils.answer(message, self.strings("api_error").format(e))
        
        if not dick_music_list or not dick_music_list.documents:
            return await utils.answer(message, self.strings("no_music"))
        
        dick_json_list = []
        
        for dick_doc in dick_music_list.documents:
            dick_audio_attr = next((a for a in dick_doc.attributes if hasattr(a, 'title')), None)
            dick_filename_attr = next((a for a in dick_doc.attributes if isinstance(a, DocumentAttributeFilename)), None)
            
            if dick_audio_attr:
                dick_song = {"id": dick_doc.id,
                             "title": dick_audio_attr.title or "Unknown",
                             "performer": dick_audio_attr.performer or "Unknown",
                             "duration": dick_audio_attr.duration,
                             "duration_formatted": str(datetime.timedelta(seconds=dick_audio_attr.duration)),
                             "size": dick_doc.size,
                             "size_mb": round(dick_doc.size / 1024 / 1024, 2),
                             "date": str(dick_doc.date),
                             "mime_type": dick_doc.mime_type,
                             "dc_id": dick_doc.dc_id,
                             "has_thumb": bool(dick_doc.thumbs)}
                
                if dick_filename_attr:
                    dick_song["filename"] = dick_filename_attr.file_name
                    
                dick_json_list.append(dick_song)
        
        dick_json_data = json.dumps({"count": len(dick_json_list), "tracks": dick_json_list}, indent=2)
        
        dick_file = io.BytesIO(dick_json_data.encode('utf-8'))
        dick_file.name = f"playlist_{dick_user_entity.username or dick_user_entity.id}.json"
        dick_kok = self._dick_display_name(dick_user_entity)
        
        await utils.answer(
            message,dick_file,
        caption=f"<emoji document_id=5463107823946717464>🎵</emoji> JSON playlist data for <b>{dick_kok}</b> ({len(dick_json_list)} tracks)")