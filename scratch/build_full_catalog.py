import os, json, re
from PIL import Image

projects_dir = r'assets\Projects'

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def determine_orientation(w, h):
    if w == 0 or h == 0:
        return 'landscape'
    ratio = w / h
    if ratio >= 1.2:
        return 'landscape'
    elif ratio <= 0.85:
        return 'portrait'
    else:
        return 'square'

# Folder classification & curatorial template
catalog = []
item_idx = 1

# Wing and Room mappings:
# Wing I: Traditional Illustrations, Character Designs, Digital Illustrations
# Wing II: 3D Works/3D Environment (Room A: env), 3D Works/3D Interior (Room B: interior), 3D Works/3D VFX (Room C: vfx), 3D Works/3D Still Life Render (Room D: stilllife), 3D Works/Character Design (Room E: char3d), 3D VFX (vfx)
# Wing III: Photography (Animal, Lunar, Model, Object, Still Life, Street)
# Wing IV: 2D Animation, Storyboarding, Post-Production, Production Design, Graphic Design, Logos, Atelier Lanyard Designs

for root, dirs, files in os.walk(projects_dir):
    for f in sorted(files):
        full = os.path.join(root, f)
        rel = os.path.relpath(full, projects_dir).replace('\\', '/')
        folder = os.path.dirname(rel)
        ext = os.path.splitext(f)[1].lower()
        size = os.path.getsize(full)
        media_type = 'video' if ext in ['.mp4', '.mov'] else 'image'
        
        w, h = 0, 0
        if media_type == 'image':
            try:
                with Image.open(full) as img:
                    w, h = img.size
            except:
                pass
        else:
            w, h = 1920, 1080
            
        orientation = determine_orientation(w, h)
        id_slug = f"project-{item_idx}-{slugify(os.path.splitext(f)[0])}"
        item_idx += 1
        
        year = '2024–2026'
        wing = 'IV'
        room = 'pavilion'
        is_hung = False
        tags = []
        title = ''
        subtitle = ''
        category = ''
        description = ''

        # 1. 2D Animation
        if folder == '2D Animation':
            wing = 'IV'
            room = 'pavilion'
            category = '2D Keyframe Animation'
            tags = ['2D Animation', 'Hand-Drawn', 'Kinematics', 'Frame-by-Frame', 'MP4']
            if 'Jump' in f:
                title = 'Jump Cycle: Momentum & Weight'
                subtitle = 'Classical 2D frame-by-frame physics study'
                year = '2025'
                description = 'A foundational study in kinematic anticipation, squash-and-stretch, dynamic hangtime, and fluid follow-through. Hand-timed to convey anatomical mass, gravitational deceleration, and elastic ground impact.'
                is_hung = True
            else:
                title = 'The Shadows of a Secret'
                subtitle = 'Narrative 2D short animation film'
                year = '2025–2026'
                description = 'A dramatic narrative short film exploring dramatic chiaroscuro lighting, emotional character interaction, atmospheric environmental mood, and hand-drawn cinematic staging.'
                is_hung = True

        # 2. 3D Works / 3D Environment (Room A)
        elif folder == '3D Works/3D Environment':
            wing = 'II'
            room = 'env'
            is_hung = True
            category = '3D Environment & ArchViz'
            tags = ['3D Environment', 'ArchViz', 'PBR', 'Lighting', 'Atmospheric', 'Blender']
            if 'Modern House' in f:
                title = 'Cantilever Modernist Villa'
                subtitle = 'Architectural visualization & natural illumination'
                year = '2025'
                description = 'Exterior architectural visualization exploring modernist structural cantilevers, floor-to-ceiling glazing materiality, manicured topography, and natural late-afternoon sun simulation.'
            elif '1st camera shot-1' in f:
                title = 'Virtual Sanctuary: Horizon View'
                subtitle = 'Cinematic environment establishing camera pass'
                year = '2025'
                description = 'First establishing camera perspective studying spatial scale, volumetric depth, atmospheric horizon scattering, and physically grounded texture response.'
            elif '1st_camera_shot' in f:
                title = 'Virtual Sanctuary: Primary Frame'
                subtitle = 'Master focal camera framing study'
                year = '2025'
                description = 'Alternative focal length pass exploring rule-of-thirds composition, directional shadow casting, and foreground framing geometry.'
            elif '673437ba' in f:
                title = 'Suburban Enclave: Twilight Vista'
                subtitle = 'Spatial worldbuilding & atmospheric scattering'
                year = '2024'
                description = 'Comprehensive neighborhood environment render featuring procedural road wear, architectural facades, and balanced twilight sky dome lighting.'
            elif '87f030ef' in f:
                title = 'Courtyard Pavilion: Sun Angle Study'
                subtitle = 'Global illumination & shadow casting analysis'
                year = '2024'
                description = 'High-contrast direct sunlight study investigating hard-edge shadows, ambient occlusion in architectural recesses, and high-frequency surface detail.'
            elif 'd447352d' in f:
                title = 'Urban Intersection: Golden Hour'
                subtitle = 'PBR urban streetscape & asset dressing'
                year = '2025'
                description = 'Modular environmental construction capturing urban street fixtures, asphalt reflectance under low-angle sunlight, and volumetric atmospheric haze.'
            elif 'e0127cd9' in f:
                title = 'Modular Complex: Spatial Scale'
                subtitle = 'Architectural layout & depth-of-field render'
                year = '2024'
                description = 'Perspective composition testing architectural massing, repeating structural motifs, and shallow depth-of-field focus falloff.'
            elif 'e8c29017' in f:
                title = 'Peristyle Terrace: Exterior Arch'
                subtitle = 'Classical-modern hybrid environment study'
                year = '2024'
                description = 'Investigation into classical architectural proportions translated into 3D polygon modeling, fluted pilasters, and soft skylight bounce.'
            elif 'f3c21f13' in f:
                title = 'Sunken Courtyard: Overcast Ambiance'
                subtitle = 'Diffuse HDRI lighting & foliage integration'
                year = '2025'
                description = 'Diffuse skylight illumination study testing vegetation shading, subtle subsurface scattering on leaves, and non-directional shadow softness.'

        # 3. 3D Works / 3D Interior (Room B)
        elif folder == '3D Works/3D Interior':
            wing = 'II'
            room = 'interior'
            is_hung = True
            category = '3D Interior Architecture'
            tags = ['3D Interior', 'ArchViz', 'Furniture Design', 'Raytracing', 'Materiality']
            if 'Mangilaya_Interior Submission_2' in f:
                title = 'Minimalist Living Salon: Afternoon Light'
                subtitle = 'Raytraced interior architecture & textiles'
                year = '2025'
                description = 'Master interior rendering exploring warm raking sunlight, fabric micro-sheen on lounge seating, polished timber flooring reflectance, and airy spatial flow.'
            elif 'Mangilaya_Interior Submission_3' in f:
                title = 'Executive Studio: Modern Workspace'
                subtitle = 'Spatial interior layout & task lighting'
                year = '2025'
                description = 'High-fidelity workspace render featuring precision joinery, brushed metallic fittings, ergonomic geometry, and calibrated multi-source artificial illumination.'
            elif 'MANGILAYA_Object Submission_1' in f:
                title = 'Contemporary Lounge Chair: Model Pass'
                subtitle = '3D product design & ergonomic topology'
                year = '2025'
                description = 'Detailed 3D furniture study focusing on clean subdivision-surface topology, leather crease normal maps, and structural frame joinery.'
            elif 'MANGILAYA_Object Submission_2' in f:
                title = 'Architectural Luminaire & Side Table'
                subtitle = 'Studio prop modeling & specular response'
                year = '2025'
                description = 'PBR asset modeling investigating frosted glass transmission, spun brass anisotropy, and polished timber grain mapping.'
            elif 'MANGILAYA_Object Submission_3' in f:
                title = 'Artisan Planter & Ceramic Assemblage'
                subtitle = 'Still-life interior dressing asset'
                year = '2025'
                description = 'Detailed ceramic material study demonstrating glazed roughness variation, clay subsurface scattering, and organic plant model integration.'
            elif '1198435d' in f:
                title = 'Living Quarters: Natural Wood Study'
                subtitle = 'Materiality & ambient occlusion pass'
                year = '2024'
                description = 'Interior lighting analysis emphasizing timber parquet bounce light, wall paneling bevels, and warm domestic ambiance.'
            elif '423472130' in f:
                title = 'Modern Residence: Dining Alcove'
                subtitle = 'Photorealistic residential interior capture'
                year = '2024'
                description = 'Wide-angle interior composition with focus on recessed ceiling downlights, reflective table surfaces, and spatial depth.'
            elif '60633433' in f:
                title = 'Studio Loft: Concrete & Timber'
                subtitle = 'Industrial modern interior aesthetic'
                year = '2024'
                description = 'Contrast study between raw exposed architectural concrete roughness and warm honey oak millwork.'
            elif '8efbb9f4' in f:
                title = 'Reading Nook: Window Bay Lighting'
                subtitle = 'Direct portal window light simulation'
                year = '2024'
                description = 'Portal window lighting test capturing subtle light bleed around window frames, airborne dust motes, and soft shadow penumbras.'
            elif '8fed482e' in f:
                title = 'Gallery Foyer: Spatial Corridor'
                subtitle = 'Long focal length interior perspective'
                year = '2024'
                description = 'Corridor study investigating ceiling coffers, wall sconce light distribution curves, and vanishing point perspective.'

        # 4. 3D Works / 3D Still Life Render (Room D)
        elif folder == '3D Works/3D Still Life Render':
            wing = 'II'
            room = 'stilllife'
            is_hung = True
            category = '3D Still Life & Studio Render'
            tags = ['3D Still Life', 'Studio Lighting', 'Materiality', 'CGI', 'Rendering']
            if '35e96165' in f:
                title = 'Studio Still Life: Form & Reflection I'
                subtitle = 'Three-point studio lighting & specular study'
                year = '2024–2025'
                description = 'Precise studio lighting study exploring three-point key, fill, and rim light balance on curated geometric and organic objects.'
            elif '9c740ba9' in f:
                title = 'Studio Still Life: Optical Glass & Clay II'
                subtitle = 'Refraction, roughness & caustics'
                year = '2024–2025'
                description = 'Investigation of light transport through translucent materials, fresnel reflections, and delicate surface imperfections.'
            elif 'a04c379a' in f:
                title = 'Studio Still Life: Metallic Patina III'
                subtitle = 'Metallic roughness & microfacet distribution'
                year = '2024–2025'
                description = 'Detailed examination of metallic sheen, brushed texture maps, and high-dynamic-range environment reflections.'
            elif 'f9febe73' in f:
                title = 'Studio Still Life: Compositional Balance IV'
                subtitle = 'Curated object staging & tonal harmony'
                year = '2024–2025'
                description = 'Exploration of classical still life principles rendered with modern physically based raytracing and balanced color temperature.'

        # 5. 3D Works / 3D VFX (Room C)
        elif folder == '3D Works/3D VFX':
            wing = 'II'
            room = 'vfx'
            is_hung = True
            category = '3D VFX & Dynamic Simulations'
            tags = ['3D VFX', 'Simulation', 'Particles', 'Dynamics', 'Blender', 'MP4']
            if 'Bonfire' in f:
                title = 'Bonfire: Thermal Convection & Ember Dynamics'
                subtitle = 'Volumetric flame & turbulent smoke simulation'
                year = '2025'
                description = 'Real-time volumetric simulation of turbulent combustion, thermal buoyancy forces, blackbody emission curves, and floating spark embers with wind turbulence.'
            elif 'Ice Cream Bar' in f:
                title = 'Ice Cream Bar: Viscous Fluid Melt'
                subtitle = 'Viscoelastic material & surface tension dynamics'
                year = '2025'
                description = 'High-viscosity fluid simulation capturing dripping melting chocolate glaze, subsurface scattering in cream layers, and playful organic deformation.'
            elif 'Magical Night' in f:
                title = 'Magical Night: Ethereal Bioluminescence'
                subtitle = 'Cinematic particle system & glow dynamics'
                year = '2025'
                description = 'Cinematic fantasy sequence featuring swirling bioluminescent particle vortices, dynamic point light emission, and dreamlike atmospheric glow.'
            elif 'Will O Wisp' in f:
                title = 'Will O Wisp: Spectral Energy Orb'
                subtitle = 'Force-field particle guidance & plasma emission'
                year = '2025'
                description = 'Floating magical orb effect utilizing curl noise turbulence, inward gravitational force fields, and dual-frequency emissive plasma color shifting.'

        # 6. 3D VFX (Root folder - alternative author cuts)
        elif folder == '3D VFX':
            wing = 'II'
            room = 'vfx'
            is_hung = False
            category = '3D VFX & Dynamic Simulations'
            tags = ['3D VFX', 'Simulation', 'Particles', 'Dynamics', 'MP4']
            if 'ENERGYBALL' in f:
                title = 'Energy Ball: Core Plasma Synthesis'
                subtitle = 'Author cut — High-energy particle discharge'
                year = '2025'
                description = 'High-intensity particle simulation detailing concentrated electrical arcs, forcefield vortex confinement, and radiant energy diffusion.'
            elif 'FINALS' in f:
                title = 'VFX Master Sequence: Cinematic Finale'
                subtitle = 'Author cut — Full resolution dynamic composite'
                year = '2025'
                description = 'Master composite reel synthesizing volumetric smoke, bioluminescent fluid particles, and dramatic timing into a cohesive cinematic sequence.'
            elif 'Bonfire' in f:
                title = 'Bonfire: Ember Field (Author Cut)'
                subtitle = 'Author cut — Combustion dynamics & ember flight'
                year = '2025'
                description = 'Extended combustion simulation focusing on ash particle dissipation, heat haze refractive distortion, and embers ascending into darkness.'
            elif 'Ice Cream' in f:
                title = 'Ice Cream Bar: Confectionery Dynamics'
                subtitle = 'Author cut — Surface tension & chocolate fracture'
                year = '2025'
                description = 'Physics simulation of brittle chocolate shell fracturing over viscous fluid melting under warm ambient studio temperature.'

        # 7. 3D Works / Character Design (Promenade & Atrium)
        elif folder == '3D Works/Character Design':
            wing = 'II'
            room = 'char3d'
            is_hung = True
            tags = ['3D Character', 'Topology', 'Turnaround', 'Subdivision', 'Rigging']
            if 'Finals_Mangilaya.mp4' in f:
                title = '3D Character Showcase: Rigging & Motion'
                subtitle = 'Full-body kinematic character turnaround'
                year = '2025'
                category = '3D Character Rigging & Motion'
                description = 'Turnaround and animation test reel demonstrating clean deformation loops, facial blend shapes, secondary cloth dynamics, and expressive joint hierarchy.'
            else:
                title = f'Character Topology & Model Pass ({os.path.splitext(f)[0][:8]})'
                subtitle = 'Production edge flow & anatomical modeling'
                year = '2024–2025'
                category = '3D Character Design & Topology'
                description = 'High-polygon digital sculpture and subdivision surface model pass detailing anatomical proportions, facial topology flow for rigging, and costume geometry.'

        # 8. Traditional Illustrations (Wing I)
        elif folder == 'Traditional Illustrations':
            wing = 'I'
            room = 'finearts'
            category = 'Traditional Fine Art & Life Study'
            tags = ['Traditional Art', 'Graphite', 'Ink', 'Perspective', 'Life Drawing']
            if '11-07-2023' in f:
                title = 'Academic Life Study: Seated Form'
                subtitle = 'Graphite and tonal hatch drawing on paper'
                year = '2023'
                description = 'Academic observational drawing examining skeletal landmarking, musculature tension, cross-contour hatching, and subtle core shadow transitions.'
                is_hung = True
            elif '12-05-2023' in f:
                title = 'Anatomical Study: Torso & Arm Mechanics'
                subtitle = 'Proportion and foreshortening plate'
                year = '2023'
                description = 'Classical anatomical study dissecting muscular origins and insertions, dynamic weight shifts, and foreshortened limb perspectives.'
            elif '12-07-2023' in f:
                title = 'Architectural Interior: Vanishing Point Grid'
                subtitle = 'Two-point linear perspective construction'
                year = '2023'
                description = 'Rigorous linear perspective grid drafting architectural columns, coffered ceilings, and spatial depth with traditional drafting tools.'
                is_hung = True
            elif '12-09-2023' in f:
                title = 'Dynamic Gesture: Quick Silhouette Study'
                subtitle = 'Expressive ink and tonal brushwork'
                year = '2023'
                description = 'Fast gesture drawing capturing weight distribution, line-of-action continuity, and kinetic balance in human posture.'
            elif 'annotated' in f:
                title = 'Academic Plate 1-3: Form Critique'
                subtitle = 'Critique notes & structural breakdown'
                year = '2023'
                description = 'Annotated academic submission documenting proportional corrections, horizon line alignment, and planar head construction.'
            else:
                title = 'Traditional Figure Study: Standing Nude'
                subtitle = 'Life drawing and value gradation plate'
                year = '2023'
                description = 'Detailed graphite plate demonstrating subtle mid-tone handling, clean contour edges, and delicate ambient light recovery in cast shadows.'

        # 9. Character Designs (2D - Wing I)
        elif folder == 'Character Designs':
            wing = 'I'
            room = 'finearts'
            category = '2D Character Design & Model Sheet'
            tags = ['Character Design', 'Model Sheet', 'Turnaround', 'Digital Ink', 'Anatomy']
            if 'DRAWING 2 PLATE 8' in f:
                title = 'Plate 8: Full Character Anatomy & Orthographic'
                subtitle = 'Academic life study & proportion model sheet'
                year = '2024'
                description = 'Complete character turnaround sheet detailing 8-head proportional division, clothing drape mechanics, and orthographic front and lateral alignments.'
                is_hung = True
            elif 'Plate01_Mangilaya' in f:
                title = 'Plate 01: Master Character Turnaround'
                subtitle = 'Model sheet with costume & gesture variants'
                year = '2024'
                description = 'Production model sheet establishing primary character silhouette, costume breakdowns, color palettes, and signature pose attitudes.'
                is_hung = True
            elif 'facial expressions' in f:
                title = 'Character Expression Matrix'
                subtitle = 'Emotional range & phonetic mouth charts'
                year = '2024'
                description = 'Exploration of dynamic facial muscle contractions across primary emotional states: joyful, solemn, inquisitive, defiant, and contemplative.'
            elif 'poses' in f:
                title = 'Character Dynamic Action Poses'
                subtitle = 'Silhouette clarity & expressive staging'
                year = '2024'
                description = 'Collection of energetic action beats exploring dynamic weight transfer, foreshortened striking gestures, and clear readability at thumbnail scale.'
            elif 'draft' in f:
                title = 'Character Concept Rough Draft'
                subtitle = 'Ideation sketches & exploratory lines'
                year = '2024'
                description = 'Early stage exploratory linework investigating silhouette variations, accessory placements, and stylistic attitude.'
            elif 'PAH' in f:
                title = 'PAH: Character Concept Silhouette'
                subtitle = 'Stylized contemporary figure design'
                year = '2024'
                description = 'Stylized character illustration combining graphic streetwear aesthetics with classical figurative proportions.'
            else:
                title = 'Character Model Sheet: Master Final'
                subtitle = 'Polished digital ink & tonal render'
                year = '2024'
                description = 'Final approved character design showcasing finalized linework, clean flat tones, and production-ready visual specifications.'

        # 10. Digital Illustrations (Wing I)
        elif folder == 'Digital Illustrations':
            wing = 'I'
            room = 'finearts'
            category = 'Digital Concept Art & Painting'
            tags = ['Digital Art', 'Concept Art', 'Folklore', 'Illustration', 'Photoshop']
            if 'Rosa Valmora' in f:
                title = 'HIMIG Series 01 — Rosa Valmora'
                subtitle = 'Vocal personification & floral lyricism'
                year = '2024'
                description = 'Lyrical digital painting portraying the dramatic operatic soprano through velvety crimson roses, delicate drapery folds, and golden celestial radiance.'
                is_hung = True
            elif 'Celestia Liranya' in f:
                title = 'HIMIG Series 02 — Celestia Liranya'
                subtitle = 'Ethereal celestial melody & starlight'
                year = '2024'
                description = 'Celestial personification painted in luminous azure and starlight silvers, depicting harmony with nocturnal constellations and radiant celestial currents.'
                is_hung = True
            elif 'Beatrix Veyrona' in f:
                title = 'HIMIG Series 03 — Beatrix Veyrona'
                subtitle = 'Fiery orchestral cadence & brass warmth'
                year = '2024'
                description = 'Powerful figurative composition balancing deep earthen reds with piercing brass highlights to evoke orchestral passion and dramatic crescendos.'
            elif 'Talia Orvida' in f:
                title = 'HIMIG Series 04 — Talia Orvida'
                subtitle = 'Verdant folk resonance & forest breath'
                year = '2024'
                description = 'Pastoral portrait steeped in emerald moss and filtered canopy sunbeams, celebrating indigenous melody and organic acoustic warmth.'
            elif 'Jovienne Yulehart' in f:
                title = 'HIMIG Series 05 — Jovienne Yulehart'
                subtitle = 'Winter choral overture & frost luminescence'
                year = '2024'
                description = 'Choral portrait composed of crystalline cerulean tones and radiant frost patterns, embodying solemn holiday reverberations.'
            elif 'Kontiliwaya' in f:
                title = 'Mythological Chronicle: Kontiliwaya'
                subtitle = 'Philippine indigenous lore & elemental guardian'
                year = '2024'
                description = 'Vibrant folklore narrative illustration depicting mythological guardians interwoven with tropical foliage, ceremonial adornments, and golden sunset backlighting.'
            elif 'Duyanara' in f:
                title = 'Mythological Chronicle: Duyanara'
                subtitle = 'Nocturnal lullaby & forest spirit'
                year = '2024'
                description = 'Dreamscape depicting celestial forest spirits weaving luminous tapestries of moonlight over sleeping earthen valleys.'
            elif 'Singsinia' in f:
                title = 'Mythological Chronicle: Singsinia'
                subtitle = 'Aquatic siren of the mountain lake'
                year = '2024'
                description = 'Atmospheric fantasy painting capturing translucent water ripples, bioluminescent water lilies, and serene mythological poise.'
            elif 'Pipitigam' in f:
                title = 'Mythological Chronicle: Pipitigam'
                subtitle = 'Guardian bird of the golden dawn'
                year = '2024'
                description = 'Golden-hour composition capturing magnificent avian plumage radiating warmth against early morning mist.'
            elif 'Pasconia' in f:
                title = 'Mythological Chronicle: Pasconia'
                subtitle = 'Festival of lanterns & ancestral spirits'
                year = '2024'
                description = 'Rich cultural tableau celebrating seasonal festivals, glowing parols, joyful village camaraderie, and warm golden lanterns.'
            elif 'Sombrero' in f:
                title = 'Ang Pambihirang Sombrero: Color Temperature'
                subtitle = 'Children’s literature conceptual color script'
                year = '2024'
                description = 'Narrative color temperature study charting emotional warmth across playful suburban storybook environments.'
                is_hung = True
            elif 'Illustration.png' in f:
                title = 'The Radiant Hall: Conceptual Vista'
                subtitle = 'Architectural fantasy & atmospheric light rays'
                year = '2024'
                description = 'Expansive conceptual painting of a sunlit colonnade bathed in radiant volumetric dust beams and timeless architectural splendor.'
                is_hung = True
            elif 'Mascara' in f:
                title = 'MassKara Festival: Spirit of Bacolod'
                subtitle = 'Celebratory cultural portrait & beadwork'
                year = '2024'
                description = 'Spectacular explosion of festive colors, smiling ceramic masks, hand-stitched sequin plumage, and vibrant Visayan cultural resilience.'
            elif 'Park Jihyo' in f:
                title = 'Park Jihyo: Stylized Vector Portrait'
                subtitle = 'Precision vector illustration & specular highlights'
                year = '2024'
                description = 'Clean vector portrait study featuring silky line gradients, sculpted hair highlights, and accurate facial likeness.'
            elif 'Still Here' in f:
                title = 'Solitude: The Window at Dusk'
                subtitle = 'Intimate mood piece & evening glow'
                year = '2024'
                description = 'Poignant slice-of-life painting capturing quiet contemplative solitude beside a rain-streaked twilight window.'
            elif 'What the Heart Invents' in f:
                title = 'What the Heart Invents'
                subtitle = 'Surrealist psychological narrative painting'
                year = '2024'
                description = 'Surrealist metaphorical composition exploring hidden memory, internal landscapes, and the delicate architecture of human emotion.'

        # 11. Photography (Wing III)
        elif folder.startswith('Photography'):
            wing = 'III'
            room = 'nocturne'
            sub = folder.split('/')[-1] if '/' in folder else folder
            
            if 'Lunar' in sub:
                category = 'Lunar Astrophotography'
                tags = ['Astrophotography', 'Lunar', 'Telephoto', 'Craters', 'Nocturne']
                num_match = re.search(r'(\d{6})_(\d{6})', f)
                date_str = num_match.group(1) if num_match else '2026'
                title = f'Lunar Surface Observation — {f[:15]}'
                subtitle = 'High-magnification telescopic lunar survey'
                year = '2026'
                description = 'High-resolution telescopic lunar capture revealing impact craters, lunar maria basalt plains, and sharp shadow transitions along the lunar terminator line.'
                if '205445' in f:
                    title = 'Mare Imbrium & Crater Copernicus'
                    subtitle = 'Telescopic lunar terminator survey'
                    is_hung = True
                elif '205540' in f:
                    title = 'Crater Tycho & Radiant Ray System'
                    subtitle = 'Full-disc optical lunar survey'
                    is_hung = True
                elif '005111' in f:
                    title = 'Waxing Crescent: Earthshine Horizon'
                    subtitle = 'Nocturnal optical atmospheric capture'
                    is_hung = True

            elif 'Street' in sub:
                category = 'Observational Street Photography'
                tags = ['Street Photography', 'Documentary', 'Campus', 'Observational', 'Urban']
                year = '2025–2026'
                if 'Carillon' in f:
                    title = 'Carillon Bell: Historic Campanile'
                    subtitle = 'UP Diliman architectural heritage study'
                    description = 'Low-angle documentary capture of the iconic UP Carillon tower bell, highlighting bronze casting texture and open sky framing.'
                    is_hung = True
                elif 'Oblation (Male Version) with LGTB' in f:
                    title = 'UP Oblation with Rainbow Banner'
                    subtitle = 'Symbolic sculpture & collegiate pride'
                    description = 'A powerful documentary photograph of the UP Oblation monument draped with the pride banner against dramatic evening clouds.'
                    is_hung = True
                elif 'Greens' in f:
                    title = 'Sunken Garden Greens: Twilight Ambiance'
                    subtitle = 'Environmental campus landscape'
                    description = 'Atmospheric study of the iconic Acacia canopies framing the UP Sunken Garden during late afternoon golden hour.'
                    is_hung = True
                elif 'Female Version of Oblation' in f:
                    title = 'Female Oblation Study'
                    subtitle = 'Contemporary public art reinterpretation'
                    description = 'Statuesque observational portrait examining contemporary artistic reinterpretations of classical heroic campus monuments.'
                elif 'Free Street Photography' in f:
                    title = 'Campus Stroll: Candid Moment'
                    subtitle = 'Observational pedestrian narrative'
                    description = 'Spontaneous street moment documenting pedestrian rhythm, soft evening shadows, and authentic daily life.'
                else:
                    title = f'Urban Observational Study ({f[:15]})'
                    subtitle = 'Documentary street capture & ambient light'
                    description = 'Candid street scene documenting dynamic urban light, spatial composition, and human architecture.'

            elif 'Animal' in sub:
                category = 'Wildlife & Animal Photography'
                tags = ['Animal Photography', 'Wildlife', 'Telephoto', 'Natural Light']
                year = '2025'
                title = f'Animal Behavioral Study ({f[:15]})'
                subtitle = 'Observational animal portraiture in natural light'
                description = 'Natural light wildlife photography capturing alert animal postures, coat textures, and intimate expressive glances.'
                if '144004' in f:
                    title = 'Feline Serenity: Sunlit Nap'
                    subtitle = 'Intimate pet portraiture & fur texture'
                    is_hung = True

            elif 'Model' in sub:
                category = 'Portrait & Model Photography'
                tags = ['Portrait Photography', 'Studio Lighting', 'Model', 'Editorial']
                year = '2023–2024'
                if 'Light Streaks' in f:
                    title = 'Long Exposure Portrait: Light Streaks'
                    subtitle = 'Kinetic light painting & studio portraiture'
                    description = 'Experimental long-exposure portrait combining sharp flash subject illumination with dynamic neon light ribbons.'
                    is_hung = True
                elif 'Portrait Plate' in f:
                    title = 'Editorial Model Plate 2023'
                    subtitle = 'Studio beauty lighting & tonal skin retouche'
                    description = 'Academic studio portrait featuring Rembrandt key lighting, soft hair edge separation, and natural skin tonal transitions.'
                else:
                    title = f'Editorial Portrait Study ({f[:15]})'
                    subtitle = 'Fashion & natural light editorial plate'
                    description = 'Contemporary fashion portrait emphasizing authentic styling, confident pose geometry, and rich environmental bokeh.'

            elif 'Still Life' in sub:
                category = 'Still Life Photographic Study'
                tags = ['Still Life', 'Photography', 'Studio Lighting', 'Composition']
                year = '2024–2026'
                title = f'Still Life Photographic Study ({f[:15]})'
                subtitle = 'Curated studio composition & texture balance'
                description = 'Carefully staged photographic still life investigating glass transparency, fruit surface textures, and calibrated studio softbox falloff.'

            elif 'Object' in sub:
                category = 'Observational Object Study'
                tags = ['Object Photography', 'Product', 'Studio', 'Texture']
                year = '2024–2026'
                title = f'Object Photographic Study ({f[:15]})'
                subtitle = 'Product geometry & specular highlight control'
                description = 'High-detail object study analyzing surface reflections, material authenticity, and clean geometric staging.'

        # 12. Storyboarding (Wing IV)
        elif folder.startswith('Storyboarding'):
            wing = 'IV'
            room = 'pavilion'
            tags = ['Storyboarding', 'Pre-vis', 'Cinematography', 'Animation', 'Visual Narrative']
            sub = folder.split('/')[-1] if '/' in folder else folder
            
            if 'Wind Rises' in sub:
                category = 'Master Storyboard Adaptation'
                num = re.search(r'-(\d+)', f)
                n = num.group(1) if num else '1'
                title = f'The Wind Rises: Sequence 0{n} — Aerodynamic Dream'
                subtitle = 'Animatic storyboard plate after Hayao Miyazaki'
                year = '2024'
                description = 'Expressive cinematic storyboard panel analyzing visual pacing, dramatic lens choice, character eye-lines, and dynamic airplane flight choreography.'
                if n in ['3', '4']:
                    is_hung = True
            elif 'Cinematography' in sub:
                category = 'Cinematography & Screen Direction'
                num = re.search(r'-(\d+)', f)
                n = num.group(1) if num else '1'
                title = f'Screen Direction & Lens Study: Plate 0{n}'
                subtitle = '180-degree axis & cinematic framing rules'
                year = '2024'
                description = 'Academic cinematic analysis exploring spatial continuity, head-room balance, cutaway inserts, and dynamic diagonal motion vectors.'
                if n == '2':
                    is_hung = True
            elif 'Continuity' in sub:
                category = 'Continuity & Narrative Sequence'
                num = re.search(r'-(\d+)', f)
                n = num.group(1) if num else '1'
                title = f'Narrative Continuity Board: Sequence 0{n}'
                subtitle = 'Action matching & spatial orientation sheet'
                year = '2024'
                description = 'Consecutive storyboard beats testing matching action cuts, eyeline match accuracy, and emotional rhythm between adjacent shots.'
                if n == '4':
                    is_hung = True
            elif 'Paneling' in sub:
                category = 'Paneling & Dynamic Framing'
                num = re.search(r'-(\d+)', f)
                n = num.group(1) if num else '1'
                title = f'Dynamic Paneling Study: Sheet 0{n}'
                subtitle = 'Manga/comic spatial pacing & panel aspect ratios'
                year = '2024'
                description = 'Graphic narrative paneling exploring time compression, wide establishing vistas, and tight emotional insert frames.'
            elif 'Patterns' in sub:
                category = 'Motion Sequences & Animatics'
                title = 'Patterns: Animated Kinetic Sequence'
                subtitle = 'Motion animatic & graphic timing test'
                year = '2024'
                description = 'Kinetic animatic sequence testing rhythmic graphic transitions, optical loops, and syncopated motion beats.'
            elif 'Shot Composition' in sub:
                category = 'Cinematic Shot Composition'
                title = 'Master Shot Composition: Architectural Scale'
                subtitle = 'Golden ratio & depth staging in storyboard'
                year = '2024'
                description = 'Master compositional plate investigating deep staging, foreground occlusion, and dramatic wide-angle perspective in animation layouts.'

        # 13. Post-Production (Wing IV)
        elif folder.startswith('Post-Production'):
            wing = 'IV'
            room = 'pavilion'
            year = '2025'
            if 'Foley' in folder:
                category = 'Foley & Sound Design Synchronization'
                tags = ['Post-Production', 'Foley', 'Sound Design', 'Audio Sync', 'MP4']
                title = 'Foley Sound Design: Mechanical & Environmental Sync'
                subtitle = 'Plate 2 — Multi-track acoustic synchronization'
                description = 'Comprehensive foley and sound design reel demonstrating precise Foley timing, footsteps, surface textures, cloth movements, and spatial reverb placement.'
            elif 'Motion Graphics' in folder:
                category = 'Motion Graphics & Kinetic Title Sequence'
                tags = ['Motion Graphics', 'Kinetic Typography', 'Title Sequence', 'After Effects', 'MP4']
                title = 'Case File No. 27: Kinetic Graphic Sequence'
                subtitle = 'Noir detective animated typography & identity'
                description = 'Noir-inspired motion design sequence featuring kinetic typography, animated redaction tape, analog glitch textures, and sleek typographic motion.'
            elif 'Short Film' in folder:
                category = 'Cinematic Visual Storytelling'
                tags = ['Short Film', 'No-Dialogue', 'Cinematography', 'Nori Productions', 'MP4']
                title = 'Weekend at Ernies (Teaser Reel)'
                subtitle = 'No-dialogue comedy short film (Nori Productions)'
                description = 'Cinematic teaser reel for an original non-dialogue comedy short film, highlighting physical comedy timing, expressive character pantomime, and visual punchlines.'

        # 14. Production Design (Wing IV)
        elif 'Production Design' in folder:
            wing = 'IV'
            room = 'pavilion'
            category = 'Production Design & Art Direction'
            tags = ['Production Design', 'Art Direction', 'Set Photography', 'Film Set', 'Stills']
            year = '2026'
            title = f'Set Art Direction Plate ({f[:15]})'
            subtitle = 'Film set dressing, props & atmospheric color palette'
            description = 'On-set production design still capturing authentic culinary props, period kitchen dressings, practical set illumination, and lived-in character textures.'
            if '143226' in f:
                title = 'Oi Marichin Marukoy: Fancy Kitchen Set'
                subtitle = 'Master set dressing & culinary art direction'
                is_hung = True

        # 15. Graphic Design, Logos & Atelier Lanyards (Wing IV)
        elif folder in ['Graphic Design', 'Logos', 'Atelier Lanyard Designs']:
            wing = 'IV'
            room = 'pavilion'
            year = '2024–2025'
            if folder == 'Graphic Design':
                category = 'Applied Graphic Design & Poster Art'
                tags = ['Graphic Design', 'Poster Art', 'Typography', 'Visual Identity']
                if 'Chess Que' in f:
                    title = 'Chess Que: Conceptual Tournament Poster'
                    subtitle = 'Kinetic typographic layout & bold geometric grid'
                    description = 'Contemporary graphic poster celebrating strategic intellect, featuring brutalist typography, stark black-and-ochre contrast, and dynamic pawn silhouette vectors.'
                elif 'Feast of Power' in f:
                    title = 'Feast of Power: Satirical Editorial Poster'
                    subtitle = 'Illustrative graphic commentary & visual metaphor'
                    description = 'Provocative graphic poster using lavish dining metaphors to explore political excess, cultural power dynamics, and societal wealth distribution.'
                elif 'In Between' in f:
                    title = 'In Between: Liminal Typography Poster'
                    subtitle = 'Experimental typography & negative space'
                    description = 'Poetic typographical poster investigating emotional transitions, spatial threshold boundaries, and minimalist Swiss grid design.'
                else:
                    title = 'Academic Layout & Graphic Plate 1-1'
                    subtitle = 'Grid alignment & typographic hierarchy'
                    description = 'Structured editorial design plate analyzing margin proportions, baseline grid locking, and multi-column visual rhythm.'
            elif folder == 'Logos':
                category = 'Identity & Visual Brand Design'
                tags = ['Branding', 'Logo Design', 'Vector', 'Identity']
                if 'aev' in f:
                    title = 'AEV Visual Identity: Monogram Logomark'
                    subtitle = 'Geometric corporate monogram & brand glyph'
                    description = 'Sleek corporate identity mark built on strict isometric grid geometry, conveying technological precision and architectural strength.'
                elif 'asg' in f:
                    title = 'ASG Creative Studio: Identity Emblem'
                    subtitle = 'Modernist studio logo & typographic mark'
                    description = 'Clean modernist emblem balancing flowing organic curves with structured geometric typography for a creative design atelier.'
                else:
                    title = 'Asthyles Fashion Atelier: Wordmark'
                    subtitle = 'High-fashion editorial logo & bespoke lettering'
                    description = 'Sophisticated high-fashion luxury wordmark showcasing refined serif terminals, delicate hairline strokes, and timeless elegance.'
            elif folder == 'Atelier Lanyard Designs':
                category = 'Textile & Jacquard Applied Design'
                tags = ['Textile Design', 'Jacquard', 'Merchandise', 'Applied Art']
                title = f'Atelier Jacquard Lanyard Pattern ({f[:8]})'
                subtitle = 'Woven textile graphic pattern & repeat print'
                description = 'Applied graphic design for jacquard woven textile lanyards, featuring high-contrast geometric repeat patterns and durable typographic branding.'
                if '21349538' in f:
                    title = 'Atelier Jacquard Lanyard: Master Edition'
                    subtitle = 'Limited edition woven textile accessory'
                    is_hung = True

        catalog.append({
            'id': id_slug,
            'title': title or f'Studio Work: {f}',
            'subtitle': subtitle or 'Creative portfolio project',
            'year': year,
            'category': category or 'Visual Arts',
            'tags': tags or ['Art', 'Design'],
            'description': description or f'Portfolio work from {folder}.',
            'imagePath': f'./assets/Projects/{rel}',
            'mediaType': media_type,
            'wing': wing,
            'room': room,
            'orientation': orientation,
            'width': w,
            'height': h,
            'size': size,
            'isHung': is_hung
        })

print(f'Catalog generated successfully! Total items: {len(catalog)}')
hung_counts = {}
for item in catalog:
    if item['isHung']:
        hung_counts[item['wing']] = hung_counts.get(item['wing'], 0) + 1
print('Hung exhibits by wing:', hung_counts)

# Save to scratch/full_catalog.json
with open(r'scratch\full_catalog.json', 'w', encoding='utf-8') as out:
    json.dump(catalog, out, indent=4)
print('Saved to scratch/full_catalog.json')

