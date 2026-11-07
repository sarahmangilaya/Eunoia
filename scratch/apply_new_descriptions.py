import json
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_marker = 'exhibits: ['
end_marker = ']\n};'

start_idx = html.find(start_marker)
end_idx = html.find(end_marker, start_idx)
assert start_idx != -1 and end_idx != -1, "Could not find exhibits block"

exhibits_json = html[start_idx + len('exhibits: '): end_idx + 1]
exhibits = json.loads(exhibits_json)
print(f"Loaded {len(exhibits)} existing exhibits.")

# 1. Traditional Illustrations Descriptions
trad_map = {
    'annotated-Mangilaya_Sarah_20Mae-PL1-3.png': {
        'title': 'High and Mighty',
        'subtitle': 'Traditional Illustration',
        'description': "Somewhere between dreams and real life, we keep reaching for something more. Even the biggest dreams start with a tiny bit of hope. Growing into who we want to be is hard. It asks us to be brave, to be patient, and to keep rising, even when we’re scared."
    },
    'b859c124_original.jpg': {
        'title': 'A Face in Fragments',
        'subtitle': 'Traditional Illustration',
        'description': "We wear so many faces that sometimes we forget which one is really us. Behind every smile are quiet fears, heavy thoughts, and broken pieces we are still trying to understand. It’s okay to feel lost. Home is something we can find again, one piece at a time."
    },
    'CamScanner_11-07-2023_17.05_1.jpg': {
        'title': 'Thorned Devotion',
        'subtitle': 'Traditional Illustration',
        'description': "Love can feel like the most beautiful thing in the world, and still hurt the most. Like a rose with sharp thorns, we hold on tight to the things that make us feel alive, even when it makes us bleed. Because sometimes, the pain is worth it."
    },
    'CamScanner_12-05-2023_18.06_1.jpg': {
        'title': 'The Watchful',
        'subtitle': 'Traditional Illustration',
        'description': "Quiet does not always mean calm. Behind those watching eyes is a heart full of words never said and feelings kept locked away. They see everything, yet share so little. The ones who watch the most are often the ones carrying the heaviest load."
    },
    'CamScanner_12-07-2023_23.14_1.jpg': {
        'title': 'Where the Moon Embraces the Sun',
        'subtitle': 'Traditional Illustration',
        'description': "Even the brightest light needs a place to rest. The moon and the sun come from different worlds, yet they find each other and hold on. Theirs is a love between opposites. It tells us that being different does not mean we can’t belong. Like yin and yang, they make each other whole."
    },
    'CamScanner_12-09-2023_15.30_1.jpg': {
        'title': 'The Unusual Gentleman',
        'subtitle': 'Traditional Illustration',
        'description': "He sits among familiar things, dressed for a world that seems to understand him. But his unusual look carries a gentle truth: we don’t have to fit in to find where we belong. Maybe he was never meant to hide. Maybe being different is the very thing that makes him shine."
    }
}

# 2. Logos Descriptions
logo_map = {
    'aev logo.png': {
        'title': 'AEV',
        'subtitle': 'Personal Art Brand | 2025',
        'description': "Made for Aevantra, my very first art account and the start of my creative dream. This logo is where my journey began. It turns my own name into a symbol of who I was becoming, small and shy, but full of hope."
    },
    'asg logo.png': {
        'title': 'Aesthylegia: The Monogram',
        'subtitle': 'Brand Identity | 2025',
        'description': "Many letters, joined together as one. Their curves hold on to each other like old memories that never let go. The monogram feels soft, graceful, and timeless, just like the brand’s love for beauty and the past."
    },
    'asthyles.png': {
        'title': 'Aesthylegia: The Wordmark',
        'subtitle': 'Brand Identity | 2025',
        'description': "Born from two words, Aesthetic and Nostalgia, Aesthylegia holds beauty and memories close. Its decorative letters give the brand a heart and a voice of its own. They bring back the warm feeling of old things we miss, wrapped in a fresh new look."
    }
}

# 3. Graphic Design Descriptions
graphic_map = {
    'annotated-Mangilaya_Sarah_20Mae-PL1-1.png': {
        'title': 'High and Mighty',
        'subtitle': 'Mixed Media Poster Design',
        'description': "A story of ambition, growth, and the desire to reach greater heights. Beneath the layers of images, colors, and words is a reminder that no dream is too big for someone willing to rise. A visual celebration of beginnings, possibilities, and everything we hope to become."
    },
    'Chess Que.png': {
        'title': 'Chess Que',
        'subtitle': 'Editorial Magazine Cover Design',
        'description': "A playful blend of fashion, personality, and chess-inspired visuals. Bold typography, striking imagery, and creative layouts come together to capture the charm of an editorial magazine, where every detail makes its own statement."
    },
    'Feast of Power.png': {
        'title': 'Feast of Power',
        'subtitle': 'Conceptual Poster Design',
        'description': "While some sit at the table, others are left with nothing but the pieces of what was taken from them. Behind every feast of power are voices left unheard and lives slowly drained. Through surrealism, expressionism, and symbolism, this piece reflects the painful reality of corruption and the people who suffer from it."
    },
    'In Between.png': {
        'title': 'In Between',
        'subtitle': 'Music-Inspired Visual Design',
        'description': "Somewhere between stillness and movement, there is a place where everything feels at peace. Inspired by the song's gentle melody, this artwork captures the feeling of being caught between two worlds. Like a swan resting between warm and cool waters, it reminds us that there is beauty in finding balance within ourselves."
    }
}

# 4. Character Designs Descriptions
character_map = {
    'character design draft.png': {
        'title': 'Matilda',
        'subtitle': 'Character Design',
        'description': ""
    },
    'character design facial expressions.png': {
        'title': 'A Little More of Me',
        'subtitle': 'Self-Character Design | Facial Expressions',
        'description': ""
    },
    'character design poses.png': {
        'title': 'Me in Motion',
        'subtitle': 'Self-Character Design | Body Poses',
        'description': ""
    },
    'character design.png': {
        'title': 'A Study of Myself',
        'subtitle': 'Self-Character Design | Character Sheet and Different Angles',
        'description': ""
    },
    'DRAWING 2 PLATE 8 CHARACTER.png': {
        'title': 'Michael',
        'subtitle': 'Character Design',
        'description': ""
    },
    'PAH.png': {
        'title': 'Rise of the Phoenix',
        'subtitle': 'Creature Design',
        'description': ""
    },
    'Plate01_Mangilaya.png': {
        'title': 'Me, in Another Dimension',
        'subtitle': 'Self-Character Design | Rick and Morty-Inspired Style',
        'description': ""
    }
}

# 5. Atelier Lanyard Designs
lanyard_map = {
    '4a6f98af_original.jpg': 'A Little Celebration',
    '6b6e2336_original.jpg': 'Little Things, Big Joy',
    '21349538_original.jpg': 'A Place to Grow',
    'c9d3cd71_original.jpg': 'The Animal Parade',
    'd64bd39f_original.jpg': 'Heartlier',
    'ec39dc14_original.jpg': 'Playground Adventures'
}

# 6. Digital Art & Illustrations
digital_map = {
    'What the Heart Invents.png': {
        'title': 'What the Heart Invents',
        'subtitle': 'Concept Illustration',
        'description': "Some dreams never really go away. They just change shape and live inside us in new ways. This piece is where two versions of me finally meet: the musician I once dreamed of becoming, and the artist I am today. I think they would be proud of each other."
    },
    'Still Here.jpeg': {
        'title': 'Still Here',
        'subtitle': 'Personal Manifesto',
        'description': "Every scar holds a story of something I survived. Through fire, pain, and change, I found strength in the parts of me I once thought were broken. This piece is my promise to keep going, to keep creating, and to always stay true to who I am."
    },
    'Park Jihyo (Vector Art).png': {
        'title': 'Park Jihyo',
        'subtitle': 'Vector Art',
        'description': ""
    },
    'Mascara Festival.jpg': {
        'title': 'Masquerade of Smiles',
        'subtitle': 'Cultural Feature | Color Temperature Study',
        'description': "Behind every bright mask is a story of culture, joy, and people coming together. Inspired by the MassKara Festival in Bacolod, this piece is filled with warm colors and festive details. It shows a city that keeps smiling, even through hard times, and shares that joy with everyone."
    }
}

# Production Design Description
prod_design_desc = (
    "Oi Marichin Marukoy! is an eco-fantasy stop-motion animation project and bilingual "
    "Cebuano-English children's storybook (Mangayo Ko'g Asin / May I Have Some Salt), created by filmmaker and writer Ara Chawdhury. "
    "As part of a 10-member crew, I collaborated with the team on the production design of Fancy Kitchen, "
    "contributing to the visual development of the project."
)

updated_exhibits = []

for e in exhibits:
    path = e['imagePath']
    filename = path.split('/')[-1]

    # Filter out the 6 topology still images from 3D Character Design as requested:
    # "sa 3d works, character design yung video nalang"
    if '3D Works/Character Design' in path:
        if e['mediaType'] != 'video':
            print(f"Excluding 3D Character Design still image: {filename}")
            continue
        else:
            # Video: "Finals_Mangilaya.mp4"
            e['title'] = ""
            e['subtitle'] = ""
            e['description'] = ""
            updated_exhibits.append(e)
            continue

    # Traditional Illustrations
    if 'Traditional Illustrations' in path and filename in trad_map:
        e['title'] = trad_map[filename]['title']
        e['subtitle'] = trad_map[filename]['subtitle']
        e['description'] = trad_map[filename]['description']
        updated_exhibits.append(e)
        continue

    # Logos
    if 'Logos' in path and filename in logo_map:
        e['title'] = logo_map[filename]['title']
        e['subtitle'] = logo_map[filename]['subtitle']
        e['description'] = logo_map[filename]['description']
        updated_exhibits.append(e)
        continue

    # Graphic Design
    if 'Graphic Design' in path and filename in graphic_map:
        e['title'] = graphic_map[filename]['title']
        e['subtitle'] = graphic_map[filename]['subtitle']
        e['description'] = graphic_map[filename]['description']
        updated_exhibits.append(e)
        continue

    # Character Designs (2D in Wing I)
    if 'Character Designs/' in path and filename in character_map:
        e['title'] = character_map[filename]['title']
        e['subtitle'] = character_map[filename]['subtitle']
        e['description'] = character_map[filename]['description']
        updated_exhibits.append(e)
        continue

    # Atelier Lanyard Designs
    if 'Atelier Lanyard Designs' in path and filename in lanyard_map:
        e['title'] = lanyard_map[filename]
        e['subtitle'] = 'Atelier Lanyard Design'
        e['description'] = ""
        updated_exhibits.append(e)
        continue

    # 3D Works:
    # "ang may titles lang sa 3d works ay yung sa 3d vfx
    # tas the rest sa 3d ay walang titles and description"
    if '3D Works' in path or path.startswith('./assets/Projects/3D VFX'):
        if '3D VFX' in path:
            # Keep clean titles, no verbose description
            # E.g. Bonfire, Ice Cream Bar, Magical Night, Will O' Wisp, Energy Ball, Finals
            raw_title = filename.rsplit('.', 1)[0].replace('MANGILAYA_', '').replace('Mangilaya_', '')
            if 'FINALS' in raw_title.upper():
                e['title'] = "VFX Finals"
            elif 'ENERGYBALL' in raw_title.upper():
                e['title'] = "Energy Ball"
            elif 'BONFIRE' in raw_title.upper():
                e['title'] = "Bonfire"
            elif 'ICE CREAM' in raw_title.upper():
                e['title'] = "Ice Cream Bar"
            else:
                e['title'] = raw_title
            e['subtitle'] = "3D VFX"
            e['description'] = ""
        else:
            # 3D Environment, 3D Interior, 3D Still Life Render
            e['title'] = ""
            e['subtitle'] = ""
            e['description'] = ""
        updated_exhibits.append(e)
        continue

    # 2D Animation:
    # "sa 2d animation ay titles lang no description"
    if '2D Animation' in path:
        if 'Jump' in filename:
            e['title'] = "Jump Animation"
        elif 'Shadows' in filename:
            e['title'] = "The Shadows of a Secret"
        else:
            e['title'] = filename.rsplit('.', 1)[0]
        e['subtitle'] = "2D Animation"
        e['description'] = ""
        updated_exhibits.append(e)
        continue

    # Digital Art & Illustrations
    if 'Digital Illustrations' in path:
        if filename in digital_map:
            e['title'] = digital_map[filename]['title']
            e['subtitle'] = digital_map[filename]['subtitle']
            e['description'] = digital_map[filename]['description']
        else:
            clean_name = filename.rsplit('.', 1)[0]
            # Clean up prefix like "01 HIMIG - Rosa Valmora"
            e['title'] = clean_name
            e['subtitle'] = "Digital Illustration"
            e['description'] = ""
        updated_exhibits.append(e)
        continue

    # Audio Editing:
    # "No titles and descriptions"
    if 'Foley' in path:
        e['title'] = ""
        e['subtitle'] = ""
        e['description'] = ""
        updated_exhibits.append(e)
        continue

    # Storyboarding:
    # "Just the titles (by folder category name)"
    if 'Storyboarding' in path:
        folder_name = path.split('Storyboarding/')[1].split('/')[0]
        e['title'] = folder_name
        e['subtitle'] = "Storyboarding"
        e['description'] = ""
        updated_exhibits.append(e)
        continue

    # Production Design (Oi Marichin Marukoy!, Fancy Kitchen)
    if 'Production Design' in path:
        e['title'] = "Oi Marichin Marukoy! – Fancy Kitchen"
        e['subtitle'] = "Production Design | 10-Member Crew"
        e['description'] = prod_design_desc
        updated_exhibits.append(e)
        continue

    # Photography:
    # "By sub categories, no titles and descriptions"
    if 'Photography' in path:
        sub_cat = path.split('Photography/')[1].split('/')[0]
        e['title'] = sub_cat
        e['subtitle'] = "Photography"
        e['description'] = ""
        updated_exhibits.append(e)
        continue

    # Post-Production other items:
    if 'Motion Graphics' in path:
        e['title'] = "Case File No. 27"
        e['subtitle'] = "Motion Graphics"
        e['description'] = ""
        updated_exhibits.append(e)
        continue

    if 'No-Dialogue' in path:
        e['title'] = "Weekend at Ernie's"
        e['subtitle'] = "Short Film"
        e['description'] = ""
        updated_exhibits.append(e)
        continue

    # Fallback default
    e['description'] = ""
    updated_exhibits.append(e)

print(f"Total updated exhibits: {len(updated_exhibits)}")

# Format JSON nicely
new_exhibits_json = json.dumps(updated_exhibits, indent=2)

new_html = html[:start_idx + len('exhibits: ')] + new_exhibits_json + html[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("index.html updated successfully with new descriptions!")

