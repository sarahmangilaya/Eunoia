
/* ==========================================================================
   §3  EUNOIA_CONFIG — edit this block to customise the museum.
   --------------------------------------------------------------------------
   • site      : title, tagline, curator details shown in the lobby & HUD.
   • links     : social / contact buttons (lobby footer). Any number allowed.
   • wings     : display names for the three gallery wings (keys I, II, III).
                 The architecture/lighting theme of each wing is fixed:
                   I  = Classical (burgundy walls, gilded frames, herringbone)
                   II = Modernist (olive-alabaster, wood & brass, track lights)
                   III= Nocturne  (charcoal-slate, dramatic spotlights)
   • exhibits  : 6–8 works. Each entry:
       id            unique string
       title, subtitle, year, category, tags[], description
       imagePath     relative path to the artwork (PNG/JPG). Leave "" to use
                     the procedural canvas painting only.
       wing          "I" | "II" | "III"  — works are auto-hung along that wing
       orientation   "landscape" | "portrait" (frame proportions)
       fallbackStyle procedural painting used instantly / if the file is
                     missing: courtyard | seascape | abstract | stilllife |
                     gallery | sculpture | geometric | nocturne
       links[]       { label, url } external buttons on the curator plaque
   ========================================================================== */
const EUNOIA_CONFIG = {
  site: {
    title: "EUNOIA",
    overline: "A Museum of Animation & Visual Art",
    tagline: "Selected Works of Mangilaya · Animation, 3D CGI & Visual Arts",
    intro: "Step into the Grand Rotunda and explore four museum wings. Inspect any work to read curatorial notes, watch kinematic animation playback, or study high-resolution plates.",
    curator: "Mangilaya",
    curatorRole: "2D Animator · 3D Generalist · Visual Development Artist",
    contactEmail: "hello@eunoia.studio",
    copyright: "© 2024–2026 Mangilaya · Eunoia Museum. All rights reserved."
  },
  links: [
    { label: "ArtStation", url: "https://artstation.com" },
    { label: "Instagram",  url: "https://instagram.com" },
    { label: "LinkedIn",   url: "https://linkedin.com" },
    { label: "Contact",    url: "mailto:hello@eunoia.studio" }
  ],
  wings: {
    I:   { name: "The Classical & Fine Arts Wing", blurb: "Traditional life drawings, character model sheets & digital paintings." },
    II:  { name: "The 3D Virtual Worlds Wing", blurb: "Spatial architecture, interior visualization & character topology." },
    III: { name: "The Nocturne & Light Gallery", blurb: "Lunar astrophotography, observational optics & street portraits." },
    IV:  { name: "The Kinematic Pavilion", blurb: "2D hand-drawn animation, masterwork storyboards & applied design." }
  },
  textures: {
    floorWood:   "./assets/textures/herringbone_wood.png",
    floorMarble: "./assets/textures/checkered_marble.png"
  },
  exhibits: [
    {
        "id": "project-1-jump-animation-mp4",
        "title": "Jump Cycle: Momentum & Weight",
        "subtitle": "Classical 2D frame-by-frame physics study",
        "year": "2025",
        "category": "2D Keyframe Animation",
        "tags": [
            "2D Animation",
            "Keyframes",
            "Physics",
            "Hand-Drawn",
            "MP4"
        ],
        "description": "A foundational study in kinematic anticipation, squash-and-stretch, dynamic hangtime, and fluid follow-through. Hand-timed to convey anatomical mass, gravitational deceleration, and elastic ground impact.",
        "imagePath": "./assets/Projects/2D Animation/Jump Animation.mp4",
        "mediaType": "video",
        "wing": "IV",
        "orientation": "landscape",
        "width": 0,
        "height": 0,
        "size": 150757,
        "isHung": true
    },
    {
        "id": "project-2-673437ba-original-jpg",
        "title": "Virtual Environment Study (673437ba)",
        "subtitle": "Atmospheric 3D worldbuilding & illumination",
        "year": "2024–2025",
        "category": "3D Environment & ArchViz",
        "tags": [
            "3D Environment",
            "ArchViz",
            "PBR",
            "Lighting",
            "Blender",
            "Global Illumination"
        ],
        "description": "Exterior architectural visualization and worldbuilding study featuring physically based materials, volumetric atmospheric scattering, and natural late-afternoon sun simulation.",
        "imagePath": "./assets/Projects/3D Works/3D Environment/673437ba_original.jpg",
        "mediaType": "image",
        "wing": "II",
        "orientation": "landscape",
        "width": 1920,
        "height": 1079,
        "size": 136262,
        "isHung": false
    },
    {
        "id": "project-3-87f030ef-original-jpg",
        "title": "Virtual Environment Study (87f030ef)",
        "subtitle": "Atmospheric 3D worldbuilding & illumination",
        "year": "2024–2025",
        "category": "3D Environment & ArchViz",
        "tags": [
            "3D Environment",
            "ArchViz",
            "PBR",
            "Lighting",
            "Blender",
            "Global Illumination"
        ],
        "description": "Exterior architectural visualization and worldbuilding study featuring physically based materials, volumetric atmospheric scattering, and natural late-afternoon sun simulation.",
        "imagePath": "./assets/Projects/3D Works/3D Environment/87f030ef_original.jpg",
        "mediaType": "image",
        "wing": "II",
        "orientation": "landscape",
        "width": 1440,
        "height": 766,
        "size": 225355,
        "isHung": false
    },
    {
        "id": "project-4-d447352d-original-jpg",
        "title": "Virtual Environment Study (d447352d)",
        "subtitle": "Atmospheric 3D worldbuilding & illumination",
        "year": "2024–2025",
        "category": "3D Environment & ArchViz",
        "tags": [
            "3D Environment",
            "ArchViz",
            "PBR",
            "Lighting",
            "Blender",
            "Global Illumination"
        ],
        "description": "Exterior architectural visualization and worldbuilding study featuring physically based materials, volumetric atmospheric scattering, and natural late-afternoon sun simulation.",
        "imagePath": "./assets/Projects/3D Works/3D Environment/d447352d_original.jpg",
        "mediaType": "image",
        "wing": "II",
        "orientation": "landscape",
        "width": 1920,
        "height": 1080,
        "size": 213046,
        "isHung": false
    },
    {
        "id": "project-5-e0127cd9-original-jpg",
        "title": "Virtual Environment Study (e0127cd9)",
        "subtitle": "Atmospheric 3D worldbuilding & illumination",
        "year": "2024–2025",
        "category": "3D Environment & ArchViz",
        "tags": [
            "3D Environment",
            "ArchViz",
            "PBR",
            "Lighting",
            "Blender",
            "Global Illumination"
        ],
        "description": "Exterior architectural visualization and worldbuilding study featuring physically based materials, volumetric atmospheric scattering, and natural late-afternoon sun simulation.",
        "imagePath": "./assets/Projects/3D Works/3D Environment/e0127cd9_original.jpg",
        "mediaType": "image",
        "wing": "II",
        "orientation": "landscape",
        "width": 1440,
        "height": 784,
        "size": 284372,
        "isHung": true
    },
    {
        "id": "project-6-e8c29017-original-jpg",
        "title": "Virtual Environment Study (e8c29017)",
        "subtitle": "Atmospheric 3D worldbuilding & illumination",
        "year": "2024–2025",
        "category": "3D Environment & ArchViz",
        "tags": [
            "3D Environment",
            "ArchViz",
            "PBR",
            "Lighting",
            "Blender",
            "Global Illumination"
        ],
        "description": "Exterior architectural visualization and worldbuilding study featuring physically based materials, volumetric atmospheric scattering, and natural late-afternoon sun simulation.",
        "imagePath": "./assets/Projects/3D Works/3D Environment/e8c29017_original.jpg",
        "mediaType": "image",
        "wing": "II",
        "orientation": "landscape",
        "width": 1918,
        "height": 1079,
        "size": 169813,
        "isHung": false
    },
    {
        "id": "project-7-f3c21f13-original-jpg",
        "title": "Virtual Environment Study (f3c21f13)",
        "subtitle": "Atmospheric 3D worldbuilding & illumination",
        "year": "2024–2025",
        "category": "3D Environment & ArchViz",
        "tags": [
            "3D Environment",
            "ArchViz",
            "PBR",
            "Lighting",
            "Blender",
            "Global Illumination"
        ],
        "description": "Exterior architectural visualization and worldbuilding study featuring physically based materials, volumetric atmospheric scattering, and natural late-afternoon sun simulation.",
        "imagePath": "./assets/Projects/3D Works/3D Environment/f3c21f13_original.jpg",
        "mediaType": "image",
        "wing": "II",
        "orientation": "landscape",
        "width": 1440,
        "height": 1051,
        "size": 398111,
        "isHung": true
    },
    {
        "id": "project-8-modern-house-design-png",
        "title": "Contemporary Residential Sanctuary",
        "subtitle": "Architectural visualization & exterior daylighting",
        "year": "2024–2025",
        "category": "3D Environment & ArchViz",
        "tags": [
            "3D Environment",
            "ArchViz",
            "PBR",
            "Lighting",
            "Blender",
            "Global Illumination"
        ],
        "description": "Exterior architectural visualization and worldbuilding study featuring physically based materials, volumetric atmospheric scattering, and natural late-afternoon sun simulation.",
        "imagePath": "./assets/Projects/3D Works/3D Environment/Modern House Design.png",
        "mediaType": "image",
        "wing": "II",
        "orientation": "landscape",
        "width": 2667,
        "height": 1500,
        "size": 953420,
        "isHung": true
    },
    {
        "id": "project-9-1198435d-original-jpg",
        "title": "Spatial Interior Study (1198435d)",
        "subtitle": "Interior lighting, texture baking & mood",
        "year": "2024–2025",
        "category": "3D Interior Architecture",
        "tags": [
            "Interior Design",
            "3D Modeling",
            "Hard-Surface",
            "Texturing",
            "Substance"
        ],
        "description": "Detailed spatial render evaluating indirect photon bounces, soft contact shadows, and tactile surface finishes across natural timber, polished concrete, and architectural ceramics.",
        "imagePath": "./assets/Projects/3D Works/3D Interior/1198435d_original.jpg",
        "mediaType": "image",
        "wing": "II",
        "orientation": "landscape",
        "width": 1440,
        "height": 809,
        "size": 64320,
        "isHung": false
    },
    {
        "id": "project-10-423472130-275755438889463-206675416873562280-n-jpg",
        "title": "Spatial Interior Study (42347213)",
        "subtitle": "Interior lighting, texture baking & mood",
        "year": "2024–2025",
        "category": "3D Interior Architecture",
        "tags": [
            "Interior Design",
            "3D Modeling",
            "Hard-Surface",
            "Texturing",
            "Substance"
        ],
        "description": "Detailed spatial render evaluating indirect photon bounces, soft contact shadows, and tactile surface finishes across natural timber, polished concrete, and architectural ceramics.",
        "imagePath": "./assets/Projects/3D Works/3D Interior/423472130_275755438889463_206675416873562280_n.jpg",
        "mediaType": "image",
        "wing": "II",
        "orientation": "landscape",
        "width": 1920,
        "height": 1080,
        "size": 87251,
        "isHung": false
    },
    {
        "id": "project-11-60633433-original-jpg",
        "title": "Spatial Interior Study (60633433)",
        "subtitle": "Interior lighting, texture baking & mood",
        "year": "2024–2025",
        "category": "3D Interior Architecture",
        "tags": [
            "Interior Design",
            "3D Modeling",
            "Hard-Surface",
            "Texturing",
            "Substance"
        ],
        "description": "Detailed spatial render evaluating indirect photon bounces, soft contact shadows, and tactile surface finishes across natural timber, polished concrete, and architectural ceramics.",
        "imagePath": "./assets/Projects/3D Works/3D Interior/60633433_original.jpg",
        "mediaType": "image",
        "wing": "II",
        "orientation": "landscape",
        "width": 1280,
        "height": 720,
        "size": 47982,
        "isHung": false
    },
    {
        "id": "project-12-8efbb9f4-original-jpg",
        "title": "Spatial Interior Study (8efbb9f4)",
        "subtitle": "Interior lighting, texture baking & mood",
        "year": "2024–2025",
        "category": "3D Interior Architecture",
        "tags": [
            "Interior Design",
            "3D Modeling",
            "Hard-Surface",
            "Texturing",
            "Substance"
        ],
        "description": "Detailed spatial render evaluating indirect photon bounces, soft contact shadows, and tactile surface finishes across natural timber, polished concrete, and architectural ceramics.",
        "imagePath": "./assets/Projects/3D Works/3D Interior/8efbb9f4_original.jpg",
        "mediaType": "image",
        "wing": "II",
        "orientation": "landscape",
        "width": 1440,
        "height": 810,
        "size": 119156,
        "isHung": false
    },
    {
        "id": "project-13-8fed482e-original-jpg",
        "title": "Spatial Interior Study (8fed482e)",
        "subtitle": "Interior lighting, texture baking & mood",
        "year": "2024–2025",
        "category": "3D Interior Architecture",
        "tags": [
            "Interior Design",
            "3D Modeling",
            "Hard-Surface",
            "Texturing",
            "Substance"
        ],
        "description": "Detailed spatial render evaluating indirect photon bounces, soft contact shadows, and tactile surface finishes across natural timber, polished concrete, and architectural ceramics.",
        "imagePath": "./assets/Projects/3D Works/3D Interior/8fed482e_original.jpg",
        "mediaType": "image",
        "wing": "II",
        "orientation": "landscape",
        "width": 1440,
        "height": 810,
        "size": 73775,
        "isHung": false
    },
    {
        "id": "project-14-mangilaya-interior-submission-2-jpg",
        "title": "Mangilaya Interior Architecture (2)",
        "subtitle": "Cinematic spatial interior & material design",
        "year": "2024–2025",
        "category": "3D Interior Architecture",
        "tags": [
            "Interior Design",
            "3D Modeling",
            "Hard-Surface",
            "Texturing",
            "Substance"
        ],
        "description": "Detailed spatial render evaluating indirect photon bounces, soft contact shadows, and tactile surface finishes across natural timber, polished concrete, and architectural ceramics.",
        "imagePath": "./assets/Projects/3D Works/3D Interior/Mangilaya_Interior Submission_2.jpg",
        "mediaType": "image",
        "wing": "II",
        "orientation": "landscape",
        "width": 1920,
        "height": 1080,
        "size": 595424,
        "isHung": true
    },
    {
        "id": "project-15-mangilaya-interior-submission-3-jpg",
        "title": "Mangilaya Interior Architecture (3)",
        "subtitle": "Cinematic spatial interior & material design",
        "year": "2024–2025",
        "category": "3D Interior Architecture",
        "tags": [
            "Interior Design",
            "3D Modeling",
            "Hard-Surface",
            "Texturing",
            "Substance"
        ],
        "description": "Detailed spatial render evaluating indirect photon bounces, soft contact shadows, and tactile surface finishes across natural timber, polished concrete, and architectural ceramics.",
        "imagePath": "./assets/Projects/3D Works/3D Interior/Mangilaya_Interior Submission_3.jpg",
        "mediaType": "image",
        "wing": "II",
        "orientation": "landscape",
        "width": 1920,
        "height": 1080,
        "size": 412457,
        "isHung": true
    },
    {
        "id": "project-16-mangilaya-object-submission-1-jpg",
        "title": "Mangilaya Prop & Object Asset (1)",
        "subtitle": "Hard-surface modeling & surface shaders",
        "year": "2024–2025",
        "category": "3D Interior Architecture",
        "tags": [
            "Interior Design",
            "3D Modeling",
            "Hard-Surface",
            "Texturing",
            "Substance"
        ],
        "description": "Detailed spatial render evaluating indirect photon bounces, soft contact shadows, and tactile surface finishes across natural timber, polished concrete, and architectural ceramics.",
        "imagePath": "./assets/Projects/3D Works/3D Interior/MANGILAYA_Object Submission_1.jpg",
        "mediaType": "image",
        "wing": "II",
        "orientation": "landscape",
        "width": 1920,
        "height": 1080,
        "size": 359455,
        "isHung": true
    },
    {
        "id": "project-17-mangilaya-object-submission-2-jpg",
        "title": "Mangilaya Prop & Object Asset (2)",
        "subtitle": "Hard-surface modeling & surface shaders",
        "year": "2024–2025",
        "category": "3D Interior Architecture",
        "tags": [
            "Interior Design",
            "3D Modeling",
            "Hard-Surface",
            "Texturing",
            "Substance"
        ],
        "description": "Detailed spatial render evaluating indirect photon bounces, soft contact shadows, and tactile surface finishes across natural timber, polished concrete, and architectural ceramics.",
        "imagePath": "./assets/Projects/3D Works/3D Interior/MANGILAYA_Object Submission_2.jpg",
        "mediaType": "image",
        "wing": "II",
        "orientation": "landscape",
        "width": 1920,
        "height": 1080,
        "size": 349772,
        "isHung": true
    },
    {
        "id": "project-18-mangilaya-object-submission-3-jpg",
        "title": "Mangilaya Prop & Object Asset (3)",
        "subtitle": "Hard-surface modeling & surface shaders",
        "year": "2024–2025",
        "category": "3D Interior Architecture",
        "tags": [
            "Interior Design",
            "3D Modeling",
            "Hard-Surface",
            "Texturing",
            "Substance"
        ],
        "description": "Detailed spatial render evaluating indirect photon bounces, soft contact shadows, and tactile surface finishes across natural timber, polished concrete, and architectural ceramics.",
        "imagePath": "./assets/Projects/3D Works/3D Interior/MANGILAYA_Object Submission_3.jpg",
        "mediaType": "image",
        "wing": "II",
        "orientation": "landscape",
        "width": 1920,
        "height": 1080,
        "size": 219576,
        "isHung": false
    },
    {
        "id": "project-19-35e96165-original-jpg",
        "title": "PBR Material & Still Life Render (35e96165)",
        "subtitle": "Micro-facet roughness & surface scatter",
        "year": "2024",
        "category": "3D LookDev & Shading",
        "tags": [
            "LookDev",
            "PBR",
            "Shaders",
            "Still Life",
            "Studio Lighting"
        ],
        "description": "Studio render rig designed to test anisotropic highlights, clearcoat reflections, and dielectric Fresnel curves across complex geometric tabletop assemblages.",
        "imagePath": "./assets/Projects/3D Works/3D Still Life Render/35e96165_original.jpg",
        "mediaType": "image",
        "wing": "II",
        "orientation": "landscape",
        "width": 1440,
        "height": 810,
        "size": 59493,
        "isHung": false
    },
    {
        "id": "project-20-9c740ba9-original-jpg",
        "title": "PBR Material & Still Life Render (9c740ba9)",
        "subtitle": "Micro-facet roughness & surface scatter",
        "year": "2024",
        "category": "3D LookDev & Shading",
        "tags": [
            "LookDev",
            "PBR",
            "Shaders",
            "Still Life",
            "Studio Lighting"
        ],
        "description": "Studio render rig designed to test anisotropic highlights, clearcoat reflections, and dielectric Fresnel curves across complex geometric tabletop assemblages.",
        "imagePath": "./assets/Projects/3D Works/3D Still Life Render/9c740ba9_original.jpg",
        "mediaType": "image",
        "wing": "II",
        "orientation": "landscape",
        "width": 1440,
        "height": 808,
        "size": 93663,
        "isHung": false
    },
    {
        "id": "project-21-a04c379a-original-jpg",
        "title": "PBR Material & Still Life Render (a04c379a)",
        "subtitle": "Micro-facet roughness & surface scatter",
        "year": "2024",
        "category": "3D LookDev & Shading",
        "tags": [
            "LookDev",
            "PBR",
            "Shaders",
            "Still Life",
            "Studio Lighting"
        ],
        "description": "Studio render rig designed to test anisotropic highlights, clearcoat reflections, and dielectric Fresnel curves across complex geometric tabletop assemblages.",
        "imagePath": "./assets/Projects/3D Works/3D Still Life Render/a04c379a_original.jpg",
        "mediaType": "image",
        "wing": "II",
        "orientation": "landscape",
        "width": 1440,
        "height": 810,
        "size": 56403,
        "isHung": false
    },
    {
        "id": "project-22-f9febe73-original-jpg",
        "title": "PBR Material & Still Life Render (f9febe73)",
        "subtitle": "Micro-facet roughness & surface scatter",
        "year": "2024",
        "category": "3D LookDev & Shading",
        "tags": [
            "LookDev",
            "PBR",
            "Shaders",
            "Still Life",
            "Studio Lighting"
        ],
        "description": "Studio render rig designed to test anisotropic highlights, clearcoat reflections, and dielectric Fresnel curves across complex geometric tabletop assemblages.",
        "imagePath": "./assets/Projects/3D Works/3D Still Life Render/f9febe73_original.jpg",
        "mediaType": "image",
        "wing": "II",
        "orientation": "landscape",
        "width": 1440,
        "height": 809,
        "size": 88665,
        "isHung": false
    },
    {
        "id": "project-23-0cc31d7a-e539-4912-bd3f-954ce95ce9b9-jpg",
        "title": "Digital Character Turnaround (0cc31d7a)",
        "subtitle": "ZBrush high-poly sculpt to clean quad topology",
        "year": "2025",
        "category": "3D Character Sculpting & Topology",
        "tags": [
            "ZBrush",
            "Character Art",
            "3D Sculpt",
            "Topology",
            "Anatomy"
        ],
        "description": "Organic character modeling focusing on anatomical fidelity, deformation-friendly edge loops, and expressive facial topology ready for rigging and production deformation.",
        "imagePath": "./assets/Projects/3D Works/Character Design/0cc31d7a-e539-4912-bd3f-954ce95ce9b9.jpg",
        "mediaType": "image",
        "wing": "II",
        "orientation": "landscape",
        "width": 1919,
        "height": 1079,
        "size": 46020,
        "isHung": false
    },
    {
        "id": "project-24-1c1d4866-9076-490f-a35e-b2c2b015cbfa-jpg",
        "title": "Digital Character Turnaround (1c1d4866)",
        "subtitle": "ZBrush high-poly sculpt to clean quad topology",
        "year": "2025",
        "category": "3D Character Sculpting & Topology",
        "tags": [
            "ZBrush",
            "Character Art",
            "3D Sculpt",
            "Topology",
            "Anatomy"
        ],
        "description": "Organic character modeling focusing on anatomical fidelity, deformation-friendly edge loops, and expressive facial topology ready for rigging and production deformation.",
        "imagePath": "./assets/Projects/3D Works/Character Design/1c1d4866-9076-490f-a35e-b2c2b015cbfa.jpg",
        "mediaType": "image",
        "wing": "II",
        "orientation": "landscape",
        "width": 1919,
        "height": 1079,
        "size": 45229,
        "isHung": false
    },
    {
        "id": "project-25-96af7a33-bbca-4b1d-8a9e-867fc46679ad-jpg",
        "title": "Digital Character Turnaround (96af7a33)",
        "subtitle": "ZBrush high-poly sculpt to clean quad topology",
        "year": "2025",
        "category": "3D Character Sculpting & Topology",
        "tags": [
            "ZBrush",
            "Character Art",
            "3D Sculpt",
            "Topology",
            "Anatomy"
        ],
        "description": "Organic character modeling focusing on anatomical fidelity, deformation-friendly edge loops, and expressive facial topology ready for rigging and production deformation.",
        "imagePath": "./assets/Projects/3D Works/Character Design/96af7a33-bbca-4b1d-8a9e-867fc46679ad.jpg",
        "mediaType": "image",
        "wing": "II",
        "orientation": "landscape",
        "width": 1919,
        "height": 1079,
        "size": 56427,
        "isHung": false
    },
    {
        "id": "project-26-b16dd61a-2f00-4951-811d-6f0ef3c49dab-jpg",
        "title": "Digital Character Turnaround (b16dd61a)",
        "subtitle": "ZBrush high-poly sculpt to clean quad topology",
        "year": "2025",
        "category": "3D Character Sculpting & Topology",
        "tags": [
            "ZBrush",
            "Character Art",
            "3D Sculpt",
            "Topology",
            "Anatomy"
        ],
        "description": "Organic character modeling focusing on anatomical fidelity, deformation-friendly edge loops, and expressive facial topology ready for rigging and production deformation.",
        "imagePath": "./assets/Projects/3D Works/Character Design/b16dd61a-2f00-4951-811d-6f0ef3c49dab.jpg",
        "mediaType": "image",
        "wing": "II",
        "orientation": "landscape",
        "width": 1919,
        "height": 1079,
        "size": 54715,
        "isHung": false
    },
    {
        "id": "project-27-db3a0f57-07e8-4cdc-8080-b36d2a9a15be-jpg",
        "title": "Digital Character Turnaround (db3a0f57)",
        "subtitle": "ZBrush high-poly sculpt to clean quad topology",
        "year": "2025",
        "category": "3D Character Sculpting & Topology",
        "tags": [
            "ZBrush",
            "Character Art",
            "3D Sculpt",
            "Topology",
            "Anatomy"
        ],
        "description": "Organic character modeling focusing on anatomical fidelity, deformation-friendly edge loops, and expressive facial topology ready for rigging and production deformation.",
        "imagePath": "./assets/Projects/3D Works/Character Design/db3a0f57-07e8-4cdc-8080-b36d2a9a15be.jpg",
        "mediaType": "image",
        "wing": "II",
        "orientation": "landscape",
        "width": 1919,
        "height": 1079,
        "size": 58099,
        "isHung": true
    },
    {
        "id": "project-28-f39a60d9-c016-4c51-bf5a-a0bf0da6d763-jpg",
        "title": "Digital Character Turnaround (f39a60d9)",
        "subtitle": "ZBrush high-poly sculpt to clean quad topology",
        "year": "2025",
        "category": "3D Character Sculpting & Topology",
        "tags": [
            "ZBrush",
            "Character Art",
            "3D Sculpt",
            "Topology",
            "Anatomy"
        ],
        "description": "Organic character modeling focusing on anatomical fidelity, deformation-friendly edge loops, and expressive facial topology ready for rigging and production deformation.",
        "imagePath": "./assets/Projects/3D Works/Character Design/f39a60d9-c016-4c51-bf5a-a0bf0da6d763.jpg",
        "mediaType": "image",
        "wing": "II",
        "orientation": "landscape",
        "width": 1919,
        "height": 1079,
        "size": 59187,
        "isHung": false
    },
    {
        "id": "project-29-21349538-original-jpg",
        "title": "Atelier Jacquard Lanyard Edition (21349538)",
        "subtitle": "Woven textile & high-density dye-sublimation",
        "year": "2025",
        "category": "Applied Merchandise & Jacquard Print",
        "tags": [
            "Applied Arts",
            "Textile Design",
            "Merchandise",
            "Jacquard",
            "Product Design"
        ],
        "description": "Custom wearable merchandise developed for creative collectives and cultural events. Features bespoke repeating motifs engineered specifically for narrow-gauge woven jacquard and dye-sublimated polyester.",
        "imagePath": "./assets/Projects/Atelier Lanyard Designs/21349538_original.jpg",
        "mediaType": "image",
        "wing": "IV",
        "orientation": "landscape",
        "width": 1440,
        "height": 1074,
        "size": 170070,
        "isHung": false
    },
    {
        "id": "project-30-4a6f98af-original-jpg",
        "title": "Atelier Jacquard Lanyard Edition (4a6f98af)",
        "subtitle": "Woven textile & high-density dye-sublimation",
        "year": "2025",
        "category": "Applied Merchandise & Jacquard Print",
        "tags": [
            "Applied Arts",
            "Textile Design",
            "Merchandise",
            "Jacquard",
            "Product Design"
        ],
        "description": "Custom wearable merchandise developed for creative collectives and cultural events. Features bespoke repeating motifs engineered specifically for narrow-gauge woven jacquard and dye-sublimated polyester.",
        "imagePath": "./assets/Projects/Atelier Lanyard Designs/4a6f98af_original.jpg",
        "mediaType": "image",
        "wing": "IV",
        "orientation": "landscape",
        "width": 1440,
        "height": 1080,
        "size": 240897,
        "isHung": false
    },
    {
        "id": "project-31-6b6e2336-original-jpg",
        "title": "Atelier Jacquard Lanyard Edition (6b6e2336)",
        "subtitle": "Woven textile & high-density dye-sublimation",
        "year": "2025",
        "category": "Applied Merchandise & Jacquard Print",
        "tags": [
            "Applied Arts",
            "Textile Design",
            "Merchandise",
            "Jacquard",
            "Product Design"
        ],
        "description": "Custom wearable merchandise developed for creative collectives and cultural events. Features bespoke repeating motifs engineered specifically for narrow-gauge woven jacquard and dye-sublimated polyester.",
        "imagePath": "./assets/Projects/Atelier Lanyard Designs/6b6e2336_original.jpg",
        "mediaType": "image",
        "wing": "IV",
        "orientation": "landscape",
        "width": 1440,
        "height": 960,
        "size": 122840,
        "isHung": false
    },
    {
        "id": "project-32-c9d3cd71-original-jpg",
        "title": "Atelier Jacquard Lanyard Edition (c9d3cd71)",
        "subtitle": "Woven textile & high-density dye-sublimation",
        "year": "2025",
        "category": "Applied Merchandise & Jacquard Print",
        "tags": [
            "Applied Arts",
            "Textile Design",
            "Merchandise",
            "Jacquard",
            "Product Design"
        ],
        "description": "Custom wearable merchandise developed for creative collectives and cultural events. Features bespoke repeating motifs engineered specifically for narrow-gauge woven jacquard and dye-sublimated polyester.",
        "imagePath": "./assets/Projects/Atelier Lanyard Designs/c9d3cd71_original.jpg",
        "mediaType": "image",
        "wing": "IV",
        "orientation": "landscape",
        "width": 1440,
        "height": 1078,
        "size": 174700,
        "isHung": false
    },
    {
        "id": "project-33-d64bd39f-original-jpg",
        "title": "Atelier Jacquard Lanyard Edition (d64bd39f)",
        "subtitle": "Woven textile & high-density dye-sublimation",
        "year": "2025",
        "category": "Applied Merchandise & Jacquard Print",
        "tags": [
            "Applied Arts",
            "Textile Design",
            "Merchandise",
            "Jacquard",
            "Product Design"
        ],
        "description": "Custom wearable merchandise developed for creative collectives and cultural events. Features bespoke repeating motifs engineered specifically for narrow-gauge woven jacquard and dye-sublimated polyester.",
        "imagePath": "./assets/Projects/Atelier Lanyard Designs/d64bd39f_original.jpg",
        "mediaType": "image",
        "wing": "IV",
        "orientation": "landscape",
        "width": 1440,
        "height": 1077,
        "size": 239095,
        "isHung": false
    },
    {
        "id": "project-34-ec39dc14-original-jpg",
        "title": "Atelier Jacquard Lanyard Edition (ec39dc14)",
        "subtitle": "Woven textile & high-density dye-sublimation",
        "year": "2025",
        "category": "Applied Merchandise & Jacquard Print",
        "tags": [
            "Applied Arts",
            "Textile Design",
            "Merchandise",
            "Jacquard",
            "Product Design"
        ],
        "description": "Custom wearable merchandise developed for creative collectives and cultural events. Features bespoke repeating motifs engineered specifically for narrow-gauge woven jacquard and dye-sublimated polyester.",
        "imagePath": "./assets/Projects/Atelier Lanyard Designs/ec39dc14_original.jpg",
        "mediaType": "image",
        "wing": "IV",
        "orientation": "landscape",
        "width": 1440,
        "height": 1078,
        "size": 238142,
        "isHung": true
    },
    {
        "id": "project-35-character-design-draft-png",
        "title": "Character Concept Iteration & Drafts",
        "subtitle": "Exploratory silhouette & dynamic poses",
        "year": "2024",
        "category": "Academic Character Design",
        "tags": [
            "Character Design",
            "Academic Art",
            "Model Sheet",
            "UP CFA",
            "Line Art"
        ],
        "description": "Exemplary character model sheets detailing anatomical proportions, costume silhouette read, and turnarounds designed for animation pipeline consistency.",
        "imagePath": "./assets/Projects/Character Designs/character design draft.png",
        "mediaType": "image",
        "wing": "I",
        "orientation": "landscape",
        "width": 3508,
        "height": 2480,
        "size": 753659,
        "isHung": true
    },
    {
        "id": "project-36-drawing-2-plate-8-character-png",
        "title": "Drawing II: Plate 8 — Character Anatomy",
        "subtitle": "Academic fine arts life study & proportion sheet",
        "year": "2024",
        "category": "Academic Character Design",
        "tags": [
            "Character Design",
            "Academic Art",
            "Model Sheet",
            "UP CFA",
            "Line Art"
        ],
        "description": "Exemplary character model sheets detailing anatomical proportions, costume silhouette read, and turnarounds designed for animation pipeline consistency.",
        "imagePath": "./assets/Projects/Character Designs/DRAWING 2 PLATE 8 CHARACTER.png",
        "mediaType": "image",
        "wing": "I",
        "orientation": "portrait",
        "width": 2480,
        "height": 3508,
        "size": 957286,
        "isHung": true
    },
    {
        "id": "project-37-plate01-mangilaya-png",
        "title": "Mangilaya: Master Character Lineup",
        "subtitle": "Turnaround, scale sheet & costume breakdown",
        "year": "2024",
        "category": "Academic Character Design",
        "tags": [
            "Character Design",
            "Academic Art",
            "Model Sheet",
            "UP CFA",
            "Line Art"
        ],
        "description": "Exemplary character model sheets detailing anatomical proportions, costume silhouette read, and turnarounds designed for animation pipeline consistency.",
        "imagePath": "./assets/Projects/Character Designs/Plate01_Mangilaya.png",
        "mediaType": "image",
        "wing": "I",
        "orientation": "landscape",
        "width": 1920,
        "height": 1080,
        "size": 111326,
        "isHung": true
    },
    {
        "id": "project-38-illustration-png",
        "title": "Eunoia: The Radiant Hall",
        "subtitle": "Digital landscape composition & color script",
        "year": "2024–2025",
        "category": "Digital Fine Art & Illustration",
        "tags": [
            "Digital Painting",
            "Vector Art",
            "Culture",
            "Color Script",
            "Atmosphere"
        ],
        "description": "Digital illustration combining painterly textures and tight graphic values. Demonstrates mastery of dramatic chromatic temperature and narrative mood.",
        "imagePath": "./assets/Projects/Digital Illustrations/Illustration.png",
        "mediaType": "image",
        "wing": "I",
        "orientation": "landscape",
        "width": 2700,
        "height": 1800,
        "size": 807731,
        "isHung": true
    },
    {
        "id": "project-39-mascara-festival-jpg",
        "title": "MassKara: The Smiling City",
        "subtitle": "Cultural festival tribute in vivid color",
        "year": "2024–2025",
        "category": "Digital Fine Art & Illustration",
        "tags": [
            "Digital Painting",
            "Vector Art",
            "Culture",
            "Color Script",
            "Atmosphere"
        ],
        "description": "Digital illustration combining painterly textures and tight graphic values. Demonstrates mastery of dramatic chromatic temperature and narrative mood.",
        "imagePath": "./assets/Projects/Digital Illustrations/Mascara Festival.jpg",
        "mediaType": "image",
        "wing": "I",
        "orientation": "portrait",
        "width": 1078,
        "height": 1440,
        "size": 187670,
        "isHung": true
    },
    {
        "id": "project-40-park-jihyo-vector-art-png",
        "title": "Portrait of Park Jihyo",
        "subtitle": "Precision vector illustration & chromatic modeling",
        "year": "2024–2025",
        "category": "Digital Fine Art & Illustration",
        "tags": [
            "Digital Painting",
            "Vector Art",
            "Culture",
            "Color Script",
            "Atmosphere"
        ],
        "description": "Digital illustration combining painterly textures and tight graphic values. Demonstrates mastery of dramatic chromatic temperature and narrative mood.",
        "imagePath": "./assets/Projects/Digital Illustrations/Park Jihyo (Vector Art).png",
        "mediaType": "image",
        "wing": "I",
        "orientation": "portrait",
        "width": 1060,
        "height": 1500,
        "size": 313022,
        "isHung": true
    },
    {
        "id": "project-41-still-here-jpeg",
        "title": "Still Here: Solitude",
        "subtitle": "Atmospheric digital narrative painting",
        "year": "2024–2025",
        "category": "Digital Fine Art & Illustration",
        "tags": [
            "Digital Painting",
            "Vector Art",
            "Culture",
            "Color Script",
            "Atmosphere"
        ],
        "description": "Digital illustration combining painterly textures and tight graphic values. Demonstrates mastery of dramatic chromatic temperature and narrative mood.",
        "imagePath": "./assets/Projects/Digital Illustrations/Still Here.jpeg",
        "mediaType": "image",
        "wing": "I",
        "orientation": "portrait",
        "width": 1143,
        "height": 1600,
        "size": 100352,
        "isHung": true
    },
    {
        "id": "project-42-chess-que-png",
        "title": "CHESS QUE",
        "subtitle": "Editorial typography & Swiss grid",
        "year": "2024–2025",
        "category": "Graphic Composition & Typography",
        "tags": [
            "Graphic Design",
            "Identity",
            "Typography",
            "Branding",
            "Vector"
        ],
        "description": "Minimalist visual marks and typographic posters engineered with mathematical harmony, balance, and distinctive silhouette value across physical and digital platforms.",
        "imagePath": "./assets/Projects/Graphic Design/Chess Que.png",
        "mediaType": "image",
        "wing": "IV",
        "orientation": "portrait",
        "width": 595,
        "height": 842,
        "size": 538101,
        "isHung": true
    },
    {
        "id": "project-43-aev-logo-png",
        "title": "AEV LOGO",
        "subtitle": "Identity design & corporate symbol",
        "year": "2024–2025",
        "category": "Brand Identity & Visual Mark",
        "tags": [
            "Graphic Design",
            "Identity",
            "Typography",
            "Branding",
            "Vector"
        ],
        "description": "Minimalist visual marks and typographic posters engineered with mathematical harmony, balance, and distinctive silhouette value across physical and digital platforms.",
        "imagePath": "./assets/Projects/Logos/aev logo.png",
        "mediaType": "image",
        "wing": "IV",
        "orientation": "landscape",
        "width": 432,
        "height": 398,
        "size": 82005,
        "isHung": false
    },
    {
        "id": "project-44-asg-logo-png",
        "title": "ASG LOGO",
        "subtitle": "Identity design & corporate symbol",
        "year": "2024–2025",
        "category": "Brand Identity & Visual Mark",
        "tags": [
            "Graphic Design",
            "Identity",
            "Typography",
            "Branding",
            "Vector"
        ],
        "description": "Minimalist visual marks and typographic posters engineered with mathematical harmony, balance, and distinctive silhouette value across physical and digital platforms.",
        "imagePath": "./assets/Projects/Logos/asg logo.png",
        "mediaType": "image",
        "wing": "IV",
        "orientation": "landscape",
        "width": 546,
        "height": 545,
        "size": 28392,
        "isHung": false
    },
    {
        "id": "project-45-asthyles-png",
        "title": "ASTHYLES",
        "subtitle": "Identity design & corporate symbol",
        "year": "2024–2025",
        "category": "Brand Identity & Visual Mark",
        "tags": [
            "Graphic Design",
            "Identity",
            "Typography",
            "Branding",
            "Vector"
        ],
        "description": "Minimalist visual marks and typographic posters engineered with mathematical harmony, balance, and distinctive silhouette value across physical and digital platforms.",
        "imagePath": "./assets/Projects/Logos/asthyles.png",
        "mediaType": "image",
        "wing": "IV",
        "orientation": "landscape",
        "width": 617,
        "height": 617,
        "size": 42459,
        "isHung": false
    },
    {
        "id": "project-46-20250901-144004-100kb-jpg",
        "title": "Fauna Observational Study (20250901)",
        "subtitle": "Optics, focal plane & natural texture",
        "year": "2025",
        "category": "Macro Wildlife Studies",
        "tags": [
            "Photography",
            "Macro",
            "Optics",
            "Depth of Field"
        ],
        "description": "Precision focal plane capture examining organic patterns, fur/scale micro-reflections, and creamy shallow depth-of-field bokeh.",
        "imagePath": "./assets/Projects/Photography/Animal Photography/20250901_144004-100kb.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "portrait",
        "width": 1200,
        "height": 1600,
        "size": 100352,
        "isHung": false
    },
    {
        "id": "project-47-20250901-144006-100kb-jpg",
        "title": "Fauna Observational Study (20250901)",
        "subtitle": "Optics, focal plane & natural texture",
        "year": "2025",
        "category": "Macro Wildlife Studies",
        "tags": [
            "Photography",
            "Macro",
            "Optics",
            "Depth of Field"
        ],
        "description": "Precision focal plane capture examining organic patterns, fur/scale micro-reflections, and creamy shallow depth-of-field bokeh.",
        "imagePath": "./assets/Projects/Photography/Animal Photography/20250901_144006-100kb.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "portrait",
        "width": 1200,
        "height": 1600,
        "size": 100352,
        "isHung": false
    },
    {
        "id": "project-48-20250917-125307-100kb-jpg",
        "title": "Fauna Observational Study (20250917)",
        "subtitle": "Optics, focal plane & natural texture",
        "year": "2025",
        "category": "Macro Wildlife Studies",
        "tags": [
            "Photography",
            "Macro",
            "Optics",
            "Depth of Field"
        ],
        "description": "Precision focal plane capture examining organic patterns, fur/scale micro-reflections, and creamy shallow depth-of-field bokeh.",
        "imagePath": "./assets/Projects/Photography/Animal Photography/20250917_125307-100kb.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "portrait",
        "width": 1200,
        "height": 1600,
        "size": 100352,
        "isHung": false
    },
    {
        "id": "project-49-20250917-125310-100kb-jpg",
        "title": "Fauna Observational Study (20250917)",
        "subtitle": "Optics, focal plane & natural texture",
        "year": "2025",
        "category": "Macro Wildlife Studies",
        "tags": [
            "Photography",
            "Macro",
            "Optics",
            "Depth of Field"
        ],
        "description": "Precision focal plane capture examining organic patterns, fur/scale micro-reflections, and creamy shallow depth-of-field bokeh.",
        "imagePath": "./assets/Projects/Photography/Animal Photography/20250917_125310-100kb.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "portrait",
        "width": 1200,
        "height": 1600,
        "size": 100352,
        "isHung": false
    },
    {
        "id": "project-50-20250917-125333-100kb-jpg",
        "title": "Fauna Observational Study (20250917)",
        "subtitle": "Optics, focal plane & natural texture",
        "year": "2025",
        "category": "Macro Wildlife Studies",
        "tags": [
            "Photography",
            "Macro",
            "Optics",
            "Depth of Field"
        ],
        "description": "Precision focal plane capture examining organic patterns, fur/scale micro-reflections, and creamy shallow depth-of-field bokeh.",
        "imagePath": "./assets/Projects/Photography/Animal Photography/20250917_125333-100kb.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "portrait",
        "width": 1200,
        "height": 1600,
        "size": 100352,
        "isHung": false
    },
    {
        "id": "project-51-20250917-125348-100kb-jpg",
        "title": "Fauna Observational Study (20250917)",
        "subtitle": "Optics, focal plane & natural texture",
        "year": "2025",
        "category": "Macro Wildlife Studies",
        "tags": [
            "Photography",
            "Macro",
            "Optics",
            "Depth of Field"
        ],
        "description": "Precision focal plane capture examining organic patterns, fur/scale micro-reflections, and creamy shallow depth-of-field bokeh.",
        "imagePath": "./assets/Projects/Photography/Animal Photography/20250917_125348-100kb.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "portrait",
        "width": 1200,
        "height": 1600,
        "size": 100352,
        "isHung": true
    },
    {
        "id": "project-52-20250917-125401-100kb-jpg",
        "title": "Fauna Observational Study (20250917)",
        "subtitle": "Optics, focal plane & natural texture",
        "year": "2025",
        "category": "Macro Wildlife Studies",
        "tags": [
            "Photography",
            "Macro",
            "Optics",
            "Depth of Field"
        ],
        "description": "Precision focal plane capture examining organic patterns, fur/scale micro-reflections, and creamy shallow depth-of-field bokeh.",
        "imagePath": "./assets/Projects/Photography/Animal Photography/20250917_125401-100kb.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "portrait",
        "width": 1200,
        "height": 1600,
        "size": 100352,
        "isHung": false
    },
    {
        "id": "project-53-20260302-205445-jpg",
        "title": "Selenography: Lunar Detail (2026.03.02)",
        "subtitle": "High-magnification telescopic crater study",
        "year": "2026",
        "category": "Astrophotography & Optics",
        "tags": [
            "Astrophotography",
            "Lunar",
            "Telephoto",
            "Astronomy",
            "Fine Art Photography"
        ],
        "description": "Telescopic lunar capture recording terminal shadows across the Mare Tranquillitatis and Tycho crater ejecta. High-shutter exposure revealing razor-sharp basalt plains and crater rims.",
        "imagePath": "./assets/Projects/Photography/Lunar Photography/20260302_205445.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "landscape",
        "width": 4000,
        "height": 3000,
        "size": 282574,
        "isHung": false
    },
    {
        "id": "project-54-20260302-205457-jpg",
        "title": "Selenography: Lunar Detail (2026.03.02)",
        "subtitle": "High-magnification telescopic crater study",
        "year": "2026",
        "category": "Astrophotography & Optics",
        "tags": [
            "Astrophotography",
            "Lunar",
            "Telephoto",
            "Astronomy",
            "Fine Art Photography"
        ],
        "description": "Telescopic lunar capture recording terminal shadows across the Mare Tranquillitatis and Tycho crater ejecta. High-shutter exposure revealing razor-sharp basalt plains and crater rims.",
        "imagePath": "./assets/Projects/Photography/Lunar Photography/20260302_205457.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "landscape",
        "width": 4000,
        "height": 3000,
        "size": 433753,
        "isHung": false
    },
    {
        "id": "project-55-20260302-205511-jpg",
        "title": "Selenography: Lunar Detail (2026.03.02)",
        "subtitle": "High-magnification telescopic crater study",
        "year": "2026",
        "category": "Astrophotography & Optics",
        "tags": [
            "Astrophotography",
            "Lunar",
            "Telephoto",
            "Astronomy",
            "Fine Art Photography"
        ],
        "description": "Telescopic lunar capture recording terminal shadows across the Mare Tranquillitatis and Tycho crater ejecta. High-shutter exposure revealing razor-sharp basalt plains and crater rims.",
        "imagePath": "./assets/Projects/Photography/Lunar Photography/20260302_205511.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "landscape",
        "width": 4000,
        "height": 3000,
        "size": 424582,
        "isHung": false
    },
    {
        "id": "project-56-20260302-205540-jpg",
        "title": "Selenography: Lunar Detail (2026.03.02)",
        "subtitle": "High-magnification telescopic crater study",
        "year": "2026",
        "category": "Astrophotography & Optics",
        "tags": [
            "Astrophotography",
            "Lunar",
            "Telephoto",
            "Astronomy",
            "Fine Art Photography"
        ],
        "description": "Telescopic lunar capture recording terminal shadows across the Mare Tranquillitatis and Tycho crater ejecta. High-shutter exposure revealing razor-sharp basalt plains and crater rims.",
        "imagePath": "./assets/Projects/Photography/Lunar Photography/20260302_205540.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "landscape",
        "width": 4000,
        "height": 3000,
        "size": 331096,
        "isHung": false
    },
    {
        "id": "project-57-20260302-205643-jpg",
        "title": "Selenography: Lunar Detail (2026.03.02)",
        "subtitle": "High-magnification telescopic crater study",
        "year": "2026",
        "category": "Astrophotography & Optics",
        "tags": [
            "Astrophotography",
            "Lunar",
            "Telephoto",
            "Astronomy",
            "Fine Art Photography"
        ],
        "description": "Telescopic lunar capture recording terminal shadows across the Mare Tranquillitatis and Tycho crater ejecta. High-shutter exposure revealing razor-sharp basalt plains and crater rims.",
        "imagePath": "./assets/Projects/Photography/Lunar Photography/20260302_205643.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "landscape",
        "width": 4000,
        "height": 3000,
        "size": 422948,
        "isHung": false
    },
    {
        "id": "project-58-20260302-205707-jpg",
        "title": "Selenography: Lunar Detail (2026.03.02)",
        "subtitle": "High-magnification telescopic crater study",
        "year": "2026",
        "category": "Astrophotography & Optics",
        "tags": [
            "Astrophotography",
            "Lunar",
            "Telephoto",
            "Astronomy",
            "Fine Art Photography"
        ],
        "description": "Telescopic lunar capture recording terminal shadows across the Mare Tranquillitatis and Tycho crater ejecta. High-shutter exposure revealing razor-sharp basalt plains and crater rims.",
        "imagePath": "./assets/Projects/Photography/Lunar Photography/20260302_205707.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "landscape",
        "width": 4000,
        "height": 3000,
        "size": 622248,
        "isHung": false
    },
    {
        "id": "project-59-20260302-205738-jpg",
        "title": "Selenography: Lunar Detail (2026.03.02)",
        "subtitle": "High-magnification telescopic crater study",
        "year": "2026",
        "category": "Astrophotography & Optics",
        "tags": [
            "Astrophotography",
            "Lunar",
            "Telephoto",
            "Astronomy",
            "Fine Art Photography"
        ],
        "description": "Telescopic lunar capture recording terminal shadows across the Mare Tranquillitatis and Tycho crater ejecta. High-shutter exposure revealing razor-sharp basalt plains and crater rims.",
        "imagePath": "./assets/Projects/Photography/Lunar Photography/20260302_205738.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "landscape",
        "width": 4000,
        "height": 3000,
        "size": 634094,
        "isHung": true
    },
    {
        "id": "project-60-20260302-205757-jpg",
        "title": "Selenography: Lunar Detail (2026.03.02)",
        "subtitle": "High-magnification telescopic crater study",
        "year": "2026",
        "category": "Astrophotography & Optics",
        "tags": [
            "Astrophotography",
            "Lunar",
            "Telephoto",
            "Astronomy",
            "Fine Art Photography"
        ],
        "description": "Telescopic lunar capture recording terminal shadows across the Mare Tranquillitatis and Tycho crater ejecta. High-shutter exposure revealing razor-sharp basalt plains and crater rims.",
        "imagePath": "./assets/Projects/Photography/Lunar Photography/20260302_205757.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "landscape",
        "width": 4000,
        "height": 3000,
        "size": 619710,
        "isHung": false
    },
    {
        "id": "project-61-20260302-205804-jpg",
        "title": "Selenography: Lunar Detail (2026.03.02)",
        "subtitle": "High-magnification telescopic crater study",
        "year": "2026",
        "category": "Astrophotography & Optics",
        "tags": [
            "Astrophotography",
            "Lunar",
            "Telephoto",
            "Astronomy",
            "Fine Art Photography"
        ],
        "description": "Telescopic lunar capture recording terminal shadows across the Mare Tranquillitatis and Tycho crater ejecta. High-shutter exposure revealing razor-sharp basalt plains and crater rims.",
        "imagePath": "./assets/Projects/Photography/Lunar Photography/20260302_205804.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "landscape",
        "width": 4000,
        "height": 3000,
        "size": 625981,
        "isHung": false
    },
    {
        "id": "project-62-20260403-200150-jpg",
        "title": "Selenography: Lunar Detail (2026.04.03)",
        "subtitle": "High-magnification telescopic crater study",
        "year": "2026",
        "category": "Astrophotography & Optics",
        "tags": [
            "Astrophotography",
            "Lunar",
            "Telephoto",
            "Astronomy",
            "Fine Art Photography"
        ],
        "description": "Telescopic lunar capture recording terminal shadows across the Mare Tranquillitatis and Tycho crater ejecta. High-shutter exposure revealing razor-sharp basalt plains and crater rims.",
        "imagePath": "./assets/Projects/Photography/Lunar Photography/20260403_200150.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "landscape",
        "width": 4000,
        "height": 3000,
        "size": 358788,
        "isHung": false
    },
    {
        "id": "project-63-20260403-200426-jpg",
        "title": "Selenography: Lunar Detail (2026.04.03)",
        "subtitle": "High-magnification telescopic crater study",
        "year": "2026",
        "category": "Astrophotography & Optics",
        "tags": [
            "Astrophotography",
            "Lunar",
            "Telephoto",
            "Astronomy",
            "Fine Art Photography"
        ],
        "description": "Telescopic lunar capture recording terminal shadows across the Mare Tranquillitatis and Tycho crater ejecta. High-shutter exposure revealing razor-sharp basalt plains and crater rims.",
        "imagePath": "./assets/Projects/Photography/Lunar Photography/20260403_200426.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "landscape",
        "width": 4000,
        "height": 3000,
        "size": 320288,
        "isHung": false
    },
    {
        "id": "project-64-20260403-200433-jpg",
        "title": "Selenography: Lunar Detail (2026.04.03)",
        "subtitle": "High-magnification telescopic crater study",
        "year": "2026",
        "category": "Astrophotography & Optics",
        "tags": [
            "Astrophotography",
            "Lunar",
            "Telephoto",
            "Astronomy",
            "Fine Art Photography"
        ],
        "description": "Telescopic lunar capture recording terminal shadows across the Mare Tranquillitatis and Tycho crater ejecta. High-shutter exposure revealing razor-sharp basalt plains and crater rims.",
        "imagePath": "./assets/Projects/Photography/Lunar Photography/20260403_200433.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "landscape",
        "width": 4000,
        "height": 3000,
        "size": 471698,
        "isHung": true
    },
    {
        "id": "project-65-20261004-005102-jpg",
        "title": "Selenography: Lunar Detail (2026.10.04)",
        "subtitle": "High-magnification telescopic crater study",
        "year": "2026",
        "category": "Astrophotography & Optics",
        "tags": [
            "Astrophotography",
            "Lunar",
            "Telephoto",
            "Astronomy",
            "Fine Art Photography"
        ],
        "description": "Telescopic lunar capture recording terminal shadows across the Mare Tranquillitatis and Tycho crater ejecta. High-shutter exposure revealing razor-sharp basalt plains and crater rims.",
        "imagePath": "./assets/Projects/Photography/Lunar Photography/20261004_005102.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "landscape",
        "width": 4000,
        "height": 3000,
        "size": 357386,
        "isHung": false
    },
    {
        "id": "project-66-20261004-005111-jpg",
        "title": "Selenography: Lunar Detail (2026.10.04)",
        "subtitle": "High-magnification telescopic crater study",
        "year": "2026",
        "category": "Astrophotography & Optics",
        "tags": [
            "Astrophotography",
            "Lunar",
            "Telephoto",
            "Astronomy",
            "Fine Art Photography"
        ],
        "description": "Telescopic lunar capture recording terminal shadows across the Mare Tranquillitatis and Tycho crater ejecta. High-shutter exposure revealing razor-sharp basalt plains and crater rims.",
        "imagePath": "./assets/Projects/Photography/Lunar Photography/20261004_005111.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "landscape",
        "width": 4000,
        "height": 3000,
        "size": 343689,
        "isHung": false
    },
    {
        "id": "project-67-20261004-005117-jpg",
        "title": "Selenography: Lunar Detail (2026.10.04)",
        "subtitle": "High-magnification telescopic crater study",
        "year": "2026",
        "category": "Astrophotography & Optics",
        "tags": [
            "Astrophotography",
            "Lunar",
            "Telephoto",
            "Astronomy",
            "Fine Art Photography"
        ],
        "description": "Telescopic lunar capture recording terminal shadows across the Mare Tranquillitatis and Tycho crater ejecta. High-shutter exposure revealing razor-sharp basalt plains and crater rims.",
        "imagePath": "./assets/Projects/Photography/Lunar Photography/20261004_005117.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "landscape",
        "width": 4000,
        "height": 3000,
        "size": 349473,
        "isHung": true
    },
    {
        "id": "project-68-20261004-005119-jpg",
        "title": "Selenography: Lunar Detail (2026.10.04)",
        "subtitle": "High-magnification telescopic crater study",
        "year": "2026",
        "category": "Astrophotography & Optics",
        "tags": [
            "Astrophotography",
            "Lunar",
            "Telephoto",
            "Astronomy",
            "Fine Art Photography"
        ],
        "description": "Telescopic lunar capture recording terminal shadows across the Mare Tranquillitatis and Tycho crater ejecta. High-shutter exposure revealing razor-sharp basalt plains and crater rims.",
        "imagePath": "./assets/Projects/Photography/Lunar Photography/20261004_005119.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "landscape",
        "width": 4000,
        "height": 3000,
        "size": 347659,
        "isHung": false
    },
    {
        "id": "project-69-20261004-005148-jpg",
        "title": "Selenography: Lunar Detail (2026.10.04)",
        "subtitle": "High-magnification telescopic crater study",
        "year": "2026",
        "category": "Astrophotography & Optics",
        "tags": [
            "Astrophotography",
            "Lunar",
            "Telephoto",
            "Astronomy",
            "Fine Art Photography"
        ],
        "description": "Telescopic lunar capture recording terminal shadows across the Mare Tranquillitatis and Tycho crater ejecta. High-shutter exposure revealing razor-sharp basalt plains and crater rims.",
        "imagePath": "./assets/Projects/Photography/Lunar Photography/20261004_005148.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "landscape",
        "width": 4000,
        "height": 3000,
        "size": 245823,
        "isHung": false
    },
    {
        "id": "project-70-20261004-005149-jpg",
        "title": "Selenography: Lunar Detail (2026.10.04)",
        "subtitle": "High-magnification telescopic crater study",
        "year": "2026",
        "category": "Astrophotography & Optics",
        "tags": [
            "Astrophotography",
            "Lunar",
            "Telephoto",
            "Astronomy",
            "Fine Art Photography"
        ],
        "description": "Telescopic lunar capture recording terminal shadows across the Mare Tranquillitatis and Tycho crater ejecta. High-shutter exposure revealing razor-sharp basalt plains and crater rims.",
        "imagePath": "./assets/Projects/Photography/Lunar Photography/20261004_005149.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "landscape",
        "width": 4000,
        "height": 3000,
        "size": 245889,
        "isHung": false
    },
    {
        "id": "project-71-xan05934-jpg",
        "title": "Nocturne Portrait: In Search of Form",
        "subtitle": "High-resolution medium-format model study",
        "year": "2025",
        "category": "Studio Portraiture",
        "tags": [
            "Portraiture",
            "Model",
            "Studio Lighting",
            "Chiaroscuro",
            "4000x6000"
        ],
        "description": "Studio portrait study exploring subtle skin subsurface scattering, high-contrast chiaroscuro key lighting, and direct gaze engagement captured at 24 megapixels.",
        "imagePath": "./assets/Projects/Photography/Model Photography/XAN05934.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "portrait",
        "width": 4000,
        "height": 6000,
        "size": 753831,
        "isHung": true
    },
    {
        "id": "project-72-object-photograph-jpg",
        "title": "Sculptural Object Study",
        "subtitle": "Optics, focal plane & natural texture",
        "year": "2025",
        "category": "Product & Object Photography",
        "tags": [
            "Photography",
            "Macro",
            "Optics",
            "Depth of Field"
        ],
        "description": "Precision focal plane capture examining organic patterns, fur/scale micro-reflections, and creamy shallow depth-of-field bokeh.",
        "imagePath": "./assets/Projects/Photography/Object Photography/Object Photograph.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "portrait",
        "width": 3300,
        "height": 5100,
        "size": 335599,
        "isHung": true
    },
    {
        "id": "project-73-20250503-183223-100kb-jpg",
        "title": "Observational Table Study (20250503)",
        "subtitle": "Natural ambient light & tactile textures",
        "year": "2025",
        "category": "Fine Art Still Life Photography",
        "tags": [
            "Still Life",
            "Photography",
            "Natural Light",
            "Composition"
        ],
        "description": "Atmospheric still life capturing the tactile subtleties of domestic objects bathed in filtered window light. A meditation on everyday quietude.",
        "imagePath": "./assets/Projects/Photography/Still Life Photography/20250503_183223-100kb.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "portrait",
        "width": 1200,
        "height": 1600,
        "size": 100352,
        "isHung": false
    },
    {
        "id": "project-74-20250515-122341-100kb-jpg",
        "title": "Observational Table Study (20250515)",
        "subtitle": "Natural ambient light & tactile textures",
        "year": "2025",
        "category": "Fine Art Still Life Photography",
        "tags": [
            "Still Life",
            "Photography",
            "Natural Light",
            "Composition"
        ],
        "description": "Atmospheric still life capturing the tactile subtleties of domestic objects bathed in filtered window light. A meditation on everyday quietude.",
        "imagePath": "./assets/Projects/Photography/Still Life Photography/20250515_122341-100kb.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "portrait",
        "width": 1200,
        "height": 1600,
        "size": 100352,
        "isHung": false
    },
    {
        "id": "project-75-20250628-174425-100kb-jpg",
        "title": "Observational Table Study (20250628)",
        "subtitle": "Natural ambient light & tactile textures",
        "year": "2025",
        "category": "Fine Art Still Life Photography",
        "tags": [
            "Still Life",
            "Photography",
            "Natural Light",
            "Composition"
        ],
        "description": "Atmospheric still life capturing the tactile subtleties of domestic objects bathed in filtered window light. A meditation on everyday quietude.",
        "imagePath": "./assets/Projects/Photography/Still Life Photography/20250628_174425-100kb.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "portrait",
        "width": 1200,
        "height": 1600,
        "size": 100352,
        "isHung": true
    },
    {
        "id": "project-76-20250917-223817-100kb-jpg",
        "title": "Observational Table Study (20250917)",
        "subtitle": "Natural ambient light & tactile textures",
        "year": "2025",
        "category": "Fine Art Still Life Photography",
        "tags": [
            "Still Life",
            "Photography",
            "Natural Light",
            "Composition"
        ],
        "description": "Atmospheric still life capturing the tactile subtleties of domestic objects bathed in filtered window light. A meditation on everyday quietude.",
        "imagePath": "./assets/Projects/Photography/Still Life Photography/20250917_223817-100kb.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "portrait",
        "width": 1200,
        "height": 1600,
        "size": 100352,
        "isHung": false
    },
    {
        "id": "project-77-up-oblation-male-version-with-lgtb-flag-jpg",
        "title": "UP Oblation: Pride & Identity",
        "subtitle": "Documentary capture at University of the Philippines",
        "year": "2024",
        "category": "Documentary & Street Photography",
        "tags": [
            "Street Photography",
            "UP Diliman",
            "Documentary",
            "Culture",
            "Social Fabric"
        ],
        "description": "Documentary street photograph taken at the UP Diliman campus, juxtaposing Guillermo Tolentino’s iconic Oblation monument with the vibrant rainbow flag in an evocative statement on identity and academic freedom.",
        "imagePath": "./assets/Projects/Photography/Street Photography/UP Oblation (Male Version) with LGTB Flag.jpg",
        "mediaType": "image",
        "wing": "III",
        "orientation": "portrait",
        "width": 1542,
        "height": 2048,
        "size": 348026,
        "isHung": true
    },
    {
        "id": "project-78-cinematography-and-screen-direction-1-png",
        "title": "Screen Direction & Spatial Axis (Plate 1)",
        "subtitle": "180-degree rule & camera vectors",
        "year": "2024",
        "category": "Cinematography & Screen Direction",
        "tags": [
            "Cinematography",
            "Screen Direction",
            "180-Degree Rule",
            "Axis of Action"
        ],
        "description": "Theoretical and practical exploration of screen direction vectors, eye-line matches, and spatial continuity across reverse angles. Rigorous academic staging for animated sequences.",
        "imagePath": "./assets/Projects/Storyboarding/Cinematography and Screen Direction/Cinematography and Screen Direction-1.png",
        "mediaType": "image",
        "wing": "IV",
        "orientation": "landscape",
        "width": 2200,
        "height": 1700,
        "size": 24442,
        "isHung": false
    },
    {
        "id": "project-79-cinematography-and-screen-direction-2-png",
        "title": "Screen Direction & Spatial Axis (Plate 2)",
        "subtitle": "180-degree rule & camera vectors",
        "year": "2024",
        "category": "Cinematography & Screen Direction",
        "tags": [
            "Cinematography",
            "Screen Direction",
            "180-Degree Rule",
            "Axis of Action"
        ],
        "description": "Theoretical and practical exploration of screen direction vectors, eye-line matches, and spatial continuity across reverse angles. Rigorous academic staging for animated sequences.",
        "imagePath": "./assets/Projects/Storyboarding/Cinematography and Screen Direction/Cinematography and Screen Direction-2.png",
        "mediaType": "image",
        "wing": "IV",
        "orientation": "landscape",
        "width": 2200,
        "height": 1700,
        "size": 176559,
        "isHung": true
    },
    {
        "id": "project-80-cinematography-and-screen-direction-3-png",
        "title": "Screen Direction & Spatial Axis (Plate 3)",
        "subtitle": "180-degree rule & camera vectors",
        "year": "2024",
        "category": "Cinematography & Screen Direction",
        "tags": [
            "Cinematography",
            "Screen Direction",
            "180-Degree Rule",
            "Axis of Action"
        ],
        "description": "Theoretical and practical exploration of screen direction vectors, eye-line matches, and spatial continuity across reverse angles. Rigorous academic staging for animated sequences.",
        "imagePath": "./assets/Projects/Storyboarding/Cinematography and Screen Direction/Cinematography and Screen Direction-3.png",
        "mediaType": "image",
        "wing": "IV",
        "orientation": "landscape",
        "width": 2200,
        "height": 1700,
        "size": 193016,
        "isHung": false
    },
    {
        "id": "project-81-cinematography-and-screen-direction-4-png",
        "title": "Screen Direction & Spatial Axis (Plate 4)",
        "subtitle": "180-degree rule & camera vectors",
        "year": "2024",
        "category": "Cinematography & Screen Direction",
        "tags": [
            "Cinematography",
            "Screen Direction",
            "180-Degree Rule",
            "Axis of Action"
        ],
        "description": "Theoretical and practical exploration of screen direction vectors, eye-line matches, and spatial continuity across reverse angles. Rigorous academic staging for animated sequences.",
        "imagePath": "./assets/Projects/Storyboarding/Cinematography and Screen Direction/Cinematography and Screen Direction-4.png",
        "mediaType": "image",
        "wing": "IV",
        "orientation": "landscape",
        "width": 2200,
        "height": 1700,
        "size": 157955,
        "isHung": false
    },
    {
        "id": "project-82-continuity-board-1-png",
        "title": "Narrative Continuity (Board 1)",
        "subtitle": "Shot-to-shot spatial progression",
        "year": "2024",
        "category": "Continuity Storyboarding",
        "tags": [
            "Continuity",
            "Storyboard",
            "Narrative Staging",
            "Visual Flow"
        ],
        "description": "Detailed panel sequence analyzing character momentum and transition mechanics. Designed to ensure seamless narrative comprehension between wide establishing masters and tight expressive singles.",
        "imagePath": "./assets/Projects/Storyboarding/Continuity Board/Continuity Board-1.png",
        "mediaType": "image",
        "wing": "IV",
        "orientation": "landscape",
        "width": 2200,
        "height": 1700,
        "size": 14942,
        "isHung": false
    },
    {
        "id": "project-83-continuity-board-2-png",
        "title": "Narrative Continuity (Board 2)",
        "subtitle": "Shot-to-shot spatial progression",
        "year": "2024",
        "category": "Continuity Storyboarding",
        "tags": [
            "Continuity",
            "Storyboard",
            "Narrative Staging",
            "Visual Flow"
        ],
        "description": "Detailed panel sequence analyzing character momentum and transition mechanics. Designed to ensure seamless narrative comprehension between wide establishing masters and tight expressive singles.",
        "imagePath": "./assets/Projects/Storyboarding/Continuity Board/Continuity Board-2.png",
        "mediaType": "image",
        "wing": "IV",
        "orientation": "landscape",
        "width": 2200,
        "height": 1700,
        "size": 188714,
        "isHung": false
    },
    {
        "id": "project-84-continuity-board-3-png",
        "title": "Narrative Continuity (Board 3)",
        "subtitle": "Shot-to-shot spatial progression",
        "year": "2024",
        "category": "Continuity Storyboarding",
        "tags": [
            "Continuity",
            "Storyboard",
            "Narrative Staging",
            "Visual Flow"
        ],
        "description": "Detailed panel sequence analyzing character momentum and transition mechanics. Designed to ensure seamless narrative comprehension between wide establishing masters and tight expressive singles.",
        "imagePath": "./assets/Projects/Storyboarding/Continuity Board/Continuity Board-3.png",
        "mediaType": "image",
        "wing": "IV",
        "orientation": "landscape",
        "width": 2200,
        "height": 1700,
        "size": 157506,
        "isHung": false
    },
    {
        "id": "project-85-continuity-board-4-png",
        "title": "Narrative Continuity (Board 4)",
        "subtitle": "Shot-to-shot spatial progression",
        "year": "2024",
        "category": "Continuity Storyboarding",
        "tags": [
            "Continuity",
            "Storyboard",
            "Narrative Staging",
            "Visual Flow"
        ],
        "description": "Detailed panel sequence analyzing character momentum and transition mechanics. Designed to ensure seamless narrative comprehension between wide establishing masters and tight expressive singles.",
        "imagePath": "./assets/Projects/Storyboarding/Continuity Board/Continuity Board-4.png",
        "mediaType": "image",
        "wing": "IV",
        "orientation": "landscape",
        "width": 2200,
        "height": 1700,
        "size": 198364,
        "isHung": true
    },
    {
        "id": "project-86-paneling-1-png",
        "title": "Panel Architecture & Rhythm (Plate 1)",
        "subtitle": "Graphic novel & sequential art framing",
        "year": "2024",
        "category": "Paneling & Narrative Composition",
        "tags": [
            "Paneling",
            "Sequential Art",
            "Framing",
            "Rhythm"
        ],
        "description": "Investigates variable panel sizing, diagonal tension lines, and gutter compression to guide the viewer’s ocular progression across complex sequential narrative beats.",
        "imagePath": "./assets/Projects/Storyboarding/Paneling/Paneling-1.png",
        "mediaType": "image",
        "wing": "IV",
        "orientation": "landscape",
        "width": 2200,
        "height": 1700,
        "size": 10984,
        "isHung": false
    },
    {
        "id": "project-87-paneling-2-png",
        "title": "Panel Architecture & Rhythm (Plate 2)",
        "subtitle": "Graphic novel & sequential art framing",
        "year": "2024",
        "category": "Paneling & Narrative Composition",
        "tags": [
            "Paneling",
            "Sequential Art",
            "Framing",
            "Rhythm"
        ],
        "description": "Investigates variable panel sizing, diagonal tension lines, and gutter compression to guide the viewer’s ocular progression across complex sequential narrative beats.",
        "imagePath": "./assets/Projects/Storyboarding/Paneling/Paneling-2.png",
        "mediaType": "image",
        "wing": "IV",
        "orientation": "landscape",
        "width": 2200,
        "height": 1700,
        "size": 202517,
        "isHung": false
    },
    {
        "id": "project-88-paneling-3-png",
        "title": "Panel Architecture & Rhythm (Plate 3)",
        "subtitle": "Graphic novel & sequential art framing",
        "year": "2024",
        "category": "Paneling & Narrative Composition",
        "tags": [
            "Paneling",
            "Sequential Art",
            "Framing",
            "Rhythm"
        ],
        "description": "Investigates variable panel sizing, diagonal tension lines, and gutter compression to guide the viewer’s ocular progression across complex sequential narrative beats.",
        "imagePath": "./assets/Projects/Storyboarding/Paneling/Paneling-3.png",
        "mediaType": "image",
        "wing": "IV",
        "orientation": "landscape",
        "width": 2200,
        "height": 1700,
        "size": 121054,
        "isHung": true
    },
    {
        "id": "project-89-the-wind-rises-story-boarding-3-png",
        "title": "The Wind Rises: Sequence Breakdown (Sheet 3)",
        "subtitle": "Cinematic pacing & staging study after Hayao Miyazaki",
        "year": "2024",
        "category": "Masterwork Storyboard Analysis",
        "tags": [
            "Storyboarding",
            "Studio Ghibli",
            "Cinematography",
            "Visual Pacing",
            "Direction"
        ],
        "description": "High-fidelity cinematic board studying the emotional geography, focal-length shifts, and temporal staging of Studio Ghibli’s \"The Wind Rises\". Focuses on subtextual character blocking and visual rhythm.",
        "imagePath": "./assets/Projects/Storyboarding/The Wind Rises Story Boarding/The Wind Rises Story Boarding-3.png",
        "mediaType": "image",
        "wing": "IV",
        "orientation": "portrait",
        "width": 7085,
        "height": 9169,
        "size": 862917,
        "isHung": true
    },
    {
        "id": "project-90-the-wind-rises-story-boarding-4-png",
        "title": "The Wind Rises: Sequence Breakdown (Sheet 4)",
        "subtitle": "Cinematic pacing & staging study after Hayao Miyazaki",
        "year": "2024",
        "category": "Masterwork Storyboard Analysis",
        "tags": [
            "Storyboarding",
            "Studio Ghibli",
            "Cinematography",
            "Visual Pacing",
            "Direction"
        ],
        "description": "High-fidelity cinematic board studying the emotional geography, focal-length shifts, and temporal staging of Studio Ghibli’s \"The Wind Rises\". Focuses on subtextual character blocking and visual rhythm.",
        "imagePath": "./assets/Projects/Storyboarding/The Wind Rises Story Boarding/The Wind Rises Story Boarding-4.png",
        "mediaType": "image",
        "wing": "IV",
        "orientation": "portrait",
        "width": 7085,
        "height": 9169,
        "size": 919741,
        "isHung": true
    },
    {
        "id": "project-91-the-wind-rises-story-boarding-5-png",
        "title": "The Wind Rises: Sequence Breakdown (Sheet 5)",
        "subtitle": "Cinematic pacing & staging study after Hayao Miyazaki",
        "year": "2024",
        "category": "Masterwork Storyboard Analysis",
        "tags": [
            "Storyboarding",
            "Studio Ghibli",
            "Cinematography",
            "Visual Pacing",
            "Direction"
        ],
        "description": "High-fidelity cinematic board studying the emotional geography, focal-length shifts, and temporal staging of Studio Ghibli’s \"The Wind Rises\". Focuses on subtextual character blocking and visual rhythm.",
        "imagePath": "./assets/Projects/Storyboarding/The Wind Rises Story Boarding/The Wind Rises Story Boarding-5.png",
        "mediaType": "image",
        "wing": "IV",
        "orientation": "portrait",
        "width": 7085,
        "height": 9169,
        "size": 973902,
        "isHung": false
    },
    {
        "id": "project-92-b859c124-original-jpg",
        "title": "Traditional Study on Paper (b859c124_o)",
        "subtitle": "Graphite, gouache & observational life drawing",
        "year": "2023–2024",
        "category": "Traditional Works on Paper",
        "tags": [
            "Traditional Art",
            "Graphite",
            "Gouache",
            "Life Drawing",
            "CamScanner"
        ],
        "description": "Authentic fine arts studio plates scanned from sketchbook and paper archives. Features expressive cross-hatching, structural planar analysis, and observational tonal modeling.",
        "imagePath": "./assets/Projects/Traditional Illustrations/b859c124_original.jpg",
        "mediaType": "image",
        "wing": "I",
        "orientation": "portrait",
        "width": 1019,
        "height": 1440,
        "size": 303514,
        "isHung": false
    },
    {
        "id": "project-93-camscanner-11-07-2023-17-05-1-jpg",
        "title": "Traditional Study on Paper (CamScanner)",
        "subtitle": "Graphite, gouache & observational life drawing",
        "year": "2023–2024",
        "category": "Traditional Works on Paper",
        "tags": [
            "Traditional Art",
            "Graphite",
            "Gouache",
            "Life Drawing",
            "CamScanner"
        ],
        "description": "Authentic fine arts studio plates scanned from sketchbook and paper archives. Features expressive cross-hatching, structural planar analysis, and observational tonal modeling.",
        "imagePath": "./assets/Projects/Traditional Illustrations/CamScanner_11-07-2023_17.05_1.jpg",
        "mediaType": "image",
        "wing": "I",
        "orientation": "portrait",
        "width": 1568,
        "height": 2368,
        "size": 222616,
        "isHung": false
    },
    {
        "id": "project-94-camscanner-12-05-2023-18-06-1-jpg",
        "title": "Traditional Study on Paper (CamScanner)",
        "subtitle": "Graphite, gouache & observational life drawing",
        "year": "2023–2024",
        "category": "Traditional Works on Paper",
        "tags": [
            "Traditional Art",
            "Graphite",
            "Gouache",
            "Life Drawing",
            "CamScanner"
        ],
        "description": "Authentic fine arts studio plates scanned from sketchbook and paper archives. Features expressive cross-hatching, structural planar analysis, and observational tonal modeling.",
        "imagePath": "./assets/Projects/Traditional Illustrations/CamScanner_12-05-2023_18.06_1.jpg",
        "mediaType": "image",
        "wing": "I",
        "orientation": "portrait",
        "width": 2340,
        "height": 3572,
        "size": 567374,
        "isHung": false
    },
    {
        "id": "project-95-camscanner-12-07-2023-23-14-1-jpg",
        "title": "Traditional Study on Paper (CamScanner)",
        "subtitle": "Graphite, gouache & observational life drawing",
        "year": "2023–2024",
        "category": "Traditional Works on Paper",
        "tags": [
            "Traditional Art",
            "Graphite",
            "Gouache",
            "Life Drawing",
            "CamScanner"
        ],
        "description": "Authentic fine arts studio plates scanned from sketchbook and paper archives. Features expressive cross-hatching, structural planar analysis, and observational tonal modeling.",
        "imagePath": "./assets/Projects/Traditional Illustrations/CamScanner_12-07-2023_23.14_1.jpg",
        "mediaType": "image",
        "wing": "I",
        "orientation": "portrait",
        "width": 2200,
        "height": 3372,
        "size": 721896,
        "isHung": true
    },
    {
        "id": "project-96-camscanner-12-09-2023-15-30-1-jpg",
        "title": "Traditional Study on Paper (CamScanner)",
        "subtitle": "Graphite, gouache & observational life drawing",
        "year": "2023–2024",
        "category": "Traditional Works on Paper",
        "tags": [
            "Traditional Art",
            "Graphite",
            "Gouache",
            "Life Drawing",
            "CamScanner"
        ],
        "description": "Authentic fine arts studio plates scanned from sketchbook and paper archives. Features expressive cross-hatching, structural planar analysis, and observational tonal modeling.",
        "imagePath": "./assets/Projects/Traditional Illustrations/CamScanner_12-09-2023_15.30_1.jpg",
        "mediaType": "image",
        "wing": "I",
        "orientation": "portrait",
        "width": 2084,
        "height": 3200,
        "size": 623788,
        "isHung": false
    }
]
};

/* ==========================================================================
   §4  ENGINE — nothing below needs editing to customise content.
   ========================================================================== */
// import * as THREE from 'three';
// import { PointerLockControls } from 'three/addons/controls/PointerLockControls.js';
// import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
// import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';

/* --------------------------------------------------------------------------
   4.1  Small math / random helpers
   -------------------------------------------------------------------------- */
const TAU = Math.PI * 2;
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const lerp = (a, b, t) => a + (b - a) * t;
const easeInOutCubic = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
const V3 = (x = 0, y = 0, z = 0) => new THREE.Vector3(x, y, z);
const $ = (id) => document.getElementById(id);

function rng(seed) {
  let s = (seed >>> 0) || 0x9e3779b9;
  return () => {
    s ^= s << 13; s >>>= 0;
    s ^= s >>> 17;
    s ^= s << 5; s >>>= 0;
    return s / 4294967296;
  };
}
function hashString(str) {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) h = Math.imul(h ^ str.charCodeAt(i), 16777619);
  return h >>> 0;
}
/** Periodic (tileable) value noise + fBm. Period p is in lattice units. */
function makeNoise(seed) {
  const r = rng(seed), N = 256, g = new Float32Array(N * N);
  for (let i = 0; i < N * N; i++) g[i] = r();
  const at = (x, y, p) => { x = ((x % p) + p) % p; y = ((y % p) + p) % p; return g[(y & 255) * N + (x & 255)]; };
  function noise(x, y, p = 256) {
    const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi;
    const u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf);
    const a = at(xi, yi, p), b = at(xi + 1, yi, p), c = at(xi, yi + 1, p), d = at(xi + 1, yi + 1, p);
    return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v;
  }
  function fbm(x, y, oct = 4, p = 256) {
    let s = 0, amp = 0.5, f = 1, norm = 0;
    for (let o = 0; o < oct; o++) { s += amp * noise(x * f, y * f, p * f); norm += amp; amp *= 0.5; f *= 2; }
    return s / norm;
  }
  return { noise, fbm };
}
function makeCanvas(w, h) {
  const c = document.createElement('canvas');
  c.width = w; c.height = h;
  return [c, c.getContext('2d')];
}
const rgba = (r, g, b, a = 1) => `rgba(${r | 0},${g | 0},${b | 0},${a})`;

/* --------------------------------------------------------------------------
   4.2  Procedural canvas textures (instant fallbacks for every image asset)
   -------------------------------------------------------------------------- */
const ProcTex = {
  /** Neoclassical checkered cream / terracotta marble — 4×4 tiles, seamless. */
  checkeredMarble(S = 512) {
    const [c, ctx] = makeCanvas(S, S);
    const img = ctx.createImageData(S, S), d = img.data;
    const { fbm } = makeNoise(1337);
    const tiles = 4, ts = S / tiles;
    const cream = [251, 255, 254], terra = [163, 50, 11];
    const tileRnd = [];
    const tr = rng(77);
    for (let i = 0; i < tiles * tiles; i++) tileRnd.push([tr(), tr(), tr()]);
    for (let y = 0; y < S; y++) {
      for (let x = 0; x < S; x++) {
        const tx = (x / ts) | 0, ty = (y / ts) | 0, odd = (tx + ty) & 1;
        const base = odd ? terra : cream, tRand = tileRnd[ty * tiles + tx];
        const u = x / S, v = y / S;
        const t = fbm(u * 8, v * 8, 4, 8);
        const ang = tRand[0] * Math.PI;
        const m = Math.abs(Math.sin((u * Math.cos(ang) + v * Math.sin(ang)) * 14 + t * 9 + tRand[1] * 10));
        const vein = Math.pow(1 - m, 9) * 0.9 + Math.pow(1 - Math.abs(Math.sin(u * 40 + t * 22)), 30) * 0.25;
        const cloud = 0.9 + fbm(u * 16 + tRand[2] * 3, v * 16, 3, 16) * 0.2;
        let r, g, b;
        if (odd) { r = base[0] * cloud + vein * 70; g = base[1] * cloud + vein * 55; b = base[2] * cloud + vein * 40; }
        else { const k = 1 - vein * 0.38; r = base[0] * cloud * k; g = base[1] * cloud * k; b = base[2] * cloud * k; }
        const ex = Math.min(x % ts, ts - 1 - (x % ts)), ey = Math.min(y % ts, ts - 1 - (y % ts));
        const edge = Math.min(ex, ey);
        if (edge < 1.2) { r = 0; g = 21; b = 20; }
        else if (edge < 3) { r *= 1.04; g *= 1.04; b *= 1.04; }
        const i = (y * S + x) * 4;
        d[i] = clamp(r, 0, 255); d[i + 1] = clamp(g, 0, 255); d[i + 2] = clamp(b, 0, 255); d[i + 3] = 255;
      }
    }
    ctx.putImageData(img, 0, 0);
    return c;
  },

  /** Warm polished herringbone parquet — exact lattice so the tile is seamless. */
  herringbone(S = 512) {
    const [c, ctx] = makeCanvas(S, S);
    const W = 32, n = 4, L = W * n, P = S / W; // P = 16 lattice units per tile
    ctx.fillStyle = '#001514'; ctx.fillRect(0, 0, S, S);
    const palette = [[163, 50, 11], [142, 42, 8], [185, 58, 14], [130, 36, 6], [175, 54, 12], [155, 46, 10]];
    const plank = (px, py, horizontal) => {
      const kx = ((px % P) + P) % P, ky = ((py % P) + P) % P;
      const r = rng(hashString(`${kx}:${ky}:${horizontal}`));
      const x = px * W, y = py * W, w = horizontal ? L : W, h = horizontal ? W : L;
      if (x > S || y > S || x + w < 0 || y + h < 0) return;
      const col = palette[(r() * palette.length) | 0], k = 0.88 + r() * 0.2;
      ctx.save();
      ctx.beginPath(); ctx.rect(x + 0.8, y + 0.8, w - 1.6, h - 1.6); ctx.clip();
      const g = horizontal ? ctx.createLinearGradient(x, y, x + w, y) : ctx.createLinearGradient(x, y, x, y + h);
      g.addColorStop(0, rgba(col[0] * k * 0.92, col[1] * k * 0.92, col[2] * k * 0.92));
      g.addColorStop(0.5, rgba(col[0] * k * 1.06, col[1] * k * 1.06, col[2] * k * 1.06));
      g.addColorStop(1, rgba(col[0] * k * 0.95, col[1] * k * 0.95, col[2] * k * 0.95));
      ctx.fillStyle = g; ctx.fillRect(x, y, w, h);
      // grain
      for (let i = 0; i < 14; i++) {
        const off = r() * (horizontal ? h : w), amp = 0.6 + r() * 1.6, freq = 0.02 + r() * 0.05, ph = r() * TAU;
        ctx.strokeStyle = r() > 0.5 ? 'rgba(0,21,20,0.35)' : 'rgba(230,175,46,0.18)';
        ctx.lineWidth = 0.6 + r() * 1.1;
        ctx.beginPath();
        for (let s = 0; s <= (horizontal ? w : h); s += 4) {
          const o = off + Math.sin(s * freq + ph) * amp;
          if (horizontal) (s === 0 ? ctx.moveTo(x + s, y + o) : ctx.lineTo(x + s, y + o));
          else (s === 0 ? ctx.moveTo(x + o, y + s) : ctx.lineTo(x + o, y + s));
        }
        ctx.stroke();
      }
      if (r() > 0.7) { // occasional knot
        ctx.fillStyle = 'rgba(70,36,16,0.35)';
        ctx.beginPath(); ctx.ellipse(x + w * (0.2 + r() * 0.6), y + h * (0.2 + r() * 0.6), 3 + r() * 3, 1.5 + r() * 2, horizontal ? 0 : Math.PI / 2, 0, TAU); ctx.fill();
      }
      ctx.restore();
    };
    for (let j = -8; j <= 8; j++) {
      for (let i = -24; i <= 40; i++) {
        const px = i + n * j, py = i - n * j;
        if (px < -n - 1 || px > P + 1 || py < -n - 1 || py > P + 1) continue;
        plank(px, py, true);
        plank(px, py + 1, false);
      }
    }
    return c;
  },

  /** Soft plaster (grayscale, multiplied by each wing's wall colour). */
  plaster(S = 256) {
    const [c, ctx] = makeCanvas(S, S);
    const img = ctx.createImageData(S, S), d = img.data, { fbm } = makeNoise(42);
    for (let y = 0; y < S; y++) for (let x = 0; x < S; x++) {
      const v = 0.86 + fbm(x / S * 8, y / S * 8, 4, 8) * 0.14;
      const i = (y * S + x) * 4; d[i] = d[i + 1] = d[i + 2] = v * 255; d[i + 3] = 255;
    }
    ctx.putImageData(img, 0, 0);
    return c;
  },

  /** Subtle damask wall-silk for the Classical Wing. */
  damask(S = 512) {
    const [c, ctx] = makeCanvas(S, S);
    ctx.fillStyle = '#6b0504'; ctx.fillRect(0, 0, S, S);
    ctx.drawImage(ProcTex.plaster(S), 0, 0);
    const motif = (cx, cy, s) => {
      ctx.save(); ctx.translate(cx, cy);
      ctx.fillStyle = 'rgba(230,175,46,0.22)'; ctx.strokeStyle = 'rgba(230,175,46,0.28)'; ctx.lineWidth = 2;
      for (let k = 0; k < 4; k++) {
        ctx.save(); ctx.rotate(k * Math.PI / 2);
        ctx.beginPath(); ctx.moveTo(0, -s * 0.08);
        ctx.bezierCurveTo(s * 0.18, -s * 0.2, s * 0.12, -s * 0.42, 0, -s * 0.46);
        ctx.bezierCurveTo(-s * 0.12, -s * 0.42, -s * 0.18, -s * 0.2, 0, -s * 0.08);
        ctx.fill();
        ctx.beginPath(); ctx.moveTo(s * 0.06, -s * 0.06);
        ctx.quadraticCurveTo(s * 0.32, -s * 0.12, s * 0.34, -s * 0.34); ctx.stroke();
        ctx.restore();
      }
      ctx.beginPath(); ctx.arc(0, 0, s * 0.07, 0, TAU); ctx.fill();
      ctx.restore();
    };
    const cell = S / 2;
    for (let y = -1; y <= 2; y++) for (let x = -1; x <= 2; x++) {
      motif(x * cell + cell / 2, y * cell + cell / 2, cell * 0.8);
      ctx.fillStyle = 'rgba(255,240,220,0.14)';
      ctx.beginPath(); ctx.arc(x * cell, y * cell, cell * 0.05, 0, TAU); ctx.fill();
    }
    ctx.strokeStyle = 'rgba(255,240,220,0.07)'; ctx.lineWidth = 1.5;
    for (let k = -2; k <= 4; k++) {
      ctx.beginPath(); ctx.moveTo(k * cell, 0); ctx.lineTo(k * cell + S, S); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(k * cell, S); ctx.lineTo(k * cell + S, 0); ctx.stroke();
    }
    return c;
  },

  /** Polished white statuary marble (sculptures, pedestals). */
  whiteMarble(S = 512, tint = [251, 255, 254], veinColor = [190, 155, 100]) {
    const [c, ctx] = makeCanvas(S, S);
    const img = ctx.createImageData(S, S), d = img.data, { fbm } = makeNoise(9001);
    for (let y = 0; y < S; y++) for (let x = 0; x < S; x++) {
      const u = x / S, v = y / S;
      const t = fbm(u * 6, v * 6, 5, 6);
      const m = Math.abs(Math.sin((u * 3 + v * 2) * TAU + t * 10));
      const vein = Math.pow(1 - m, 14);
      const cloud = 0.93 + fbm(u * 12, v * 12, 3, 12) * 0.1;
      const i = (y * S + x) * 4;
      for (let k = 0; k < 3; k++) d[i + k] = clamp(lerp(tint[k] * cloud, veinColor[k], vein * 0.7), 0, 255);
      d[i + 3] = 255;
    }
    ctx.putImageData(img, 0, 0);
    return c;
  },

  /** Coffered ceiling panel (recessed square with rosette). */
  coffer(S = 512, base = [251, 255, 254], rosette = '#e6af2e') {
    const [c, ctx] = makeCanvas(S, S);
    const [r, g, b] = base;
    ctx.fillStyle = rgba(r, g, b); ctx.fillRect(0, 0, S, S);
    const steps = 4, m = S * 0.1;
    for (let k = 0; k < steps; k++) {
      const inset = m + k * S * 0.045, sz = S - inset * 2;
      const shade = 1 - (k + 1) * 0.07;
      ctx.fillStyle = rgba(r * shade, g * shade, b * shade); ctx.fillRect(inset, inset, sz, sz);
      ctx.fillStyle = 'rgba(255,250,240,0.18)';
      ctx.fillRect(inset, inset, sz, 4); ctx.fillRect(inset, inset, 4, sz);
      ctx.fillStyle = 'rgba(40,25,10,0.18)';
      ctx.fillRect(inset, inset + sz - 4, sz, 4); ctx.fillRect(inset + sz - 4, inset, 4, sz);
    }
    ctx.save(); ctx.translate(S / 2, S / 2);
    ctx.fillStyle = rosette;
    for (let p = 0; p < 8; p++) {
      ctx.rotate(Math.PI / 4);
      ctx.beginPath(); ctx.ellipse(0, -S * 0.07, S * 0.022, S * 0.06, 0, 0, TAU); ctx.fill();
    }
    ctx.beginPath(); ctx.arc(0, 0, S * 0.035, 0, TAU); ctx.fillStyle = '#e6c37e'; ctx.fill();
    ctx.restore();
    ctx.strokeStyle = 'rgba(120,90,50,0.35)'; ctx.lineWidth = 3; ctx.strokeRect(1.5, 1.5, S - 3, S - 3);
    return c;
  }
};

/* --------------------------------------------------------------------------
   4.3  Procedural paintings — each config fallbackStyle has a painter
   -------------------------------------------------------------------------- */
function painterlyPass(ctx, w, h, r, { count, len, width, jitter, alpha = 0.55, angle = null }) {
  const src = ctx.getImageData(0, 0, w, h).data;
  ctx.lineCap = 'round';
  for (let i = 0; i < count; i++) {
    const px = r() * w, py = r() * h;
    const idx = ((py | 0) * w + (px | 0)) * 4;
    const j = 1 + (r() - 0.5) * jitter;
    ctx.strokeStyle = rgba(src[idx] * j, src[idx + 1] * j, src[idx + 2] * j, alpha);
    ctx.lineWidth = width * (0.5 + r());
    const a = angle === null ? r() * Math.PI : angle + (r() - 0.5) * 0.6;
    const l = len * (0.5 + r());
    ctx.beginPath();
    ctx.moveTo(px - Math.cos(a) * l / 2, py - Math.sin(a) * l / 2);
    ctx.lineTo(px + Math.cos(a) * l / 2, py + Math.sin(a) * l / 2);
    ctx.stroke();
  }
}
function canvasFinish(ctx, w, h, vignette = 0.45) {
  const g = ctx.createRadialGradient(w / 2, h / 2, Math.min(w, h) * 0.3, w / 2, h / 2, Math.max(w, h) * 0.75);
  g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, `rgba(8,5,2,${vignette})`);
  ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
  ctx.globalAlpha = 0.035; ctx.fillStyle = '#fff';
  for (let x = 0; x < w; x += 3) ctx.fillRect(x, 0, 1, h);
  ctx.fillStyle = '#000';
  for (let y = 0; y < h; y += 3) ctx.fillRect(0, y, w, 1);
  ctx.globalAlpha = 1;
}
function softGlow(ctx, x, y, rad, color, alpha = 1) {
  const g = ctx.createRadialGradient(x, y, 0, x, y, rad);
  g.addColorStop(0, color); g.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.save(); ctx.globalAlpha = alpha; ctx.globalCompositeOperation = 'lighter';
  ctx.fillStyle = g; ctx.fillRect(x - rad, y - rad, rad * 2, rad * 2); ctx.restore();
}
const Painters = {
  courtyard(ctx, w, h, r) {
    let g = ctx.createLinearGradient(0, 0, 0, h * 0.6);
    g.addColorStop(0, '#f8e2a8'); g.addColorStop(1, '#d4913f');
    ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = '#7d4f28'; ctx.fillRect(0, h * 0.2, w, h * 0.5);
    for (let i = 0; i < 5; i++) {
      const ax = w * (0.1 + i * 0.2), aw = w * 0.11, top = h * 0.36, bot = h * 0.7;
      ctx.fillStyle = '#2e1b0e';
      ctx.beginPath(); ctx.moveTo(ax - aw / 2, bot); ctx.lineTo(ax - aw / 2, top);
      ctx.arc(ax, top, aw / 2, Math.PI, 0); ctx.lineTo(ax + aw / 2, bot); ctx.fill();
      softGlow(ctx, ax, top + h * 0.12, aw * 0.6, 'rgba(255,190,110,0.35)');
    }
    g = ctx.createLinearGradient(0, h * 0.68, 0, h);
    g.addColorStop(0, '#7a5530'); g.addColorStop(1, '#22150b');
    ctx.fillStyle = g; ctx.fillRect(0, h * 0.68, w, h * 0.32);
    ctx.strokeStyle = 'rgba(30,18,8,0.35)'; ctx.lineWidth = 2;
    for (let i = -6; i <= 6; i++) { ctx.beginPath(); ctx.moveTo(w / 2 + i * w * 0.02, h * 0.68); ctx.lineTo(w / 2 + i * w * 0.2, h); ctx.stroke(); }
    for (let i = 0; i < 6; i++) {
      const cx = w * (0.02 + i * 0.192), cw = w * 0.055;
      const cg = ctx.createLinearGradient(cx - cw / 2, 0, cx + cw / 2, 0);
      cg.addColorStop(0, '#f3dcb0'); cg.addColorStop(0.45, '#d9b37a'); cg.addColorStop(1, '#5a3a1c');
      ctx.fillStyle = cg; ctx.fillRect(cx - cw / 2, h * 0.14, cw, h * 0.6);
      ctx.fillStyle = '#e8cc96'; ctx.fillRect(cx - cw * 0.8, h * 0.12, cw * 1.6, h * 0.03); ctx.fillRect(cx - cw * 0.75, h * 0.72, cw * 1.5, h * 0.03);
    }
    ctx.fillStyle = '#3c2814'; ctx.beginPath(); ctx.ellipse(w * 0.5, h * 0.84, w * 0.16, h * 0.045, 0, 0, TAU); ctx.fill();
    ctx.fillStyle = '#c9a26a'; ctx.beginPath(); ctx.ellipse(w * 0.5, h * 0.825, w * 0.15, h * 0.035, 0, 0, TAU); ctx.fill();
    ctx.fillStyle = '#d6b27a'; ctx.fillRect(w * 0.49, h * 0.7, w * 0.02, h * 0.12);
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    for (let i = 0; i < 6; i++) {
      const x0 = w * (0.05 + r() * 0.2), spread = w * (0.04 + r() * 0.05), x1 = w * (0.35 + i * 0.11);
      const rg = ctx.createLinearGradient(x0, 0, x1, h);
      rg.addColorStop(0, 'rgba(255,214,140,0.30)'); rg.addColorStop(1, 'rgba(255,200,120,0)');
      ctx.fillStyle = rg; ctx.beginPath(); ctx.moveTo(x0, -10); ctx.lineTo(x0 + spread, -10); ctx.lineTo(x1 + spread * 2.5, h); ctx.lineTo(x1, h); ctx.fill();
    }
    ctx.restore();
    const vg = ctx.createRadialGradient(w * 0.42, h * 0.45, w * 0.1, w * 0.5, h * 0.5, w * 0.7);
    vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(10,5,2,0.8)');
    ctx.fillStyle = vg; ctx.fillRect(0, 0, w, h);
  },
  seascape(ctx, w, h, r) {
    const hz = h * 0.58;
    let g = ctx.createLinearGradient(0, 0, 0, hz);
    g.addColorStop(0, '#26303e'); g.addColorStop(0.55, '#6b5a58'); g.addColorStop(1, '#eaa75a');
    ctx.fillStyle = g; ctx.fillRect(0, 0, w, hz);
    for (let i = 0; i < 26; i++) {
      ctx.fillStyle = r() > 0.5 ? 'rgba(240,170,110,0.12)' : 'rgba(60,64,80,0.18)';
      ctx.beginPath(); ctx.ellipse(r() * w, hz * (0.15 + r() * 0.6), w * (0.08 + r() * 0.2), h * (0.01 + r() * 0.03), 0, 0, TAU); ctx.fill();
    }
    softGlow(ctx, w * 0.6, hz, w * 0.45, 'rgba(255,190,110,0.85)');
    softGlow(ctx, w * 0.6, hz, w * 0.08, 'rgba(255,240,200,1)');
    g = ctx.createLinearGradient(0, hz, 0, h);
    g.addColorStop(0, '#4a4648'); g.addColorStop(0.3, '#2a2e36'); g.addColorStop(1, '#10141b');
    ctx.fillStyle = g; ctx.fillRect(0, hz, w, h - hz);
    for (let i = 0; i < 160; i++) {
      const y = hz + Math.pow(r(), 1.6) * (h - hz), spread = 0.04 + (y - hz) / (h - hz) * 0.25;
      const x = w * 0.6 + (r() - 0.5) * w * spread * 2;
      ctx.strokeStyle = `rgba(255,${180 + r() * 50},${100 + r() * 50},${0.5 * (1 - (y - hz) / (h - hz))})`;
      ctx.lineWidth = 1 + r() * 2.5; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + w * (0.01 + r() * 0.04), y); ctx.stroke();
    }
    ctx.fillStyle = 'rgba(90,80,90,0.7)'; ctx.beginPath(); ctx.moveTo(0, hz);
    for (let x = 0; x <= w * 0.35; x += w * 0.02) ctx.lineTo(x, hz - Math.sin(x / w * 9) * h * 0.02 - h * 0.025 * (1 - x / (w * 0.35)));
    ctx.lineTo(w * 0.35, hz); ctx.fill();
    ctx.fillStyle = '#181c22'; ctx.beginPath(); ctx.moveTo(w * 0.66, h);
    let y = h * 0.75;
    for (let x = w * 0.66; x <= w; x += w * 0.015) { y = Math.max(h * 0.24, y - r() * h * 0.05 + h * 0.012); ctx.lineTo(x, y); }
    ctx.lineTo(w, h); ctx.fill();
    ctx.strokeStyle = 'rgba(240,160,90,0.35)'; ctx.lineWidth = 3; ctx.stroke();
  },
  abstract(ctx, w, h, r) {
    ctx.fillStyle = '#1e1c1b'; ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = '#2c2a29'; ctx.fillRect(w * 0.55, 0, w * 0.45, h * 0.62);
    ctx.fillStyle = '#b5532e'; ctx.fillRect(w * 0.1, h * 0.38, w * 0.52, h * 0.5);
    ctx.save(); ctx.beginPath(); ctx.rect(0, 0, w, h * 0.38); ctx.clip();
    ctx.fillStyle = '#cf6c3d'; ctx.beginPath(); ctx.arc(w * 0.36, h * 0.38, w * 0.26, 0, TAU); ctx.fill(); ctx.restore();
    ctx.fillStyle = '#e9dcc4'; ctx.fillRect(w * 0.66, h * 0.66, w * 0.2, h * 0.04);
    ctx.fillStyle = '#121110'; ctx.fillRect(w * 0.62, h * 0.38, w * 0.06, h * 0.5);
    const gx = w * 0.7, gw = w * 0.05;
    const gg = ctx.createLinearGradient(gx, 0, gx + gw, 0);
    gg.addColorStop(0, '#b88a3a'); gg.addColorStop(0.5, '#f4d690'); gg.addColorStop(1, '#a87a2c');
    ctx.fillStyle = gg; ctx.fillRect(gx, h * 0.08, gw, h * 0.52);
    for (let i = 0; i < 300; i++) { ctx.fillStyle = `rgba(${200 + r() * 55},${160 + r() * 60},${80 + r() * 40},${0.3 + r() * 0.5})`; ctx.fillRect(gx + r() * gw, h * 0.08 + r() * h * 0.52, 1 + r() * 4, 1 + r() * 3); }
    ctx.strokeStyle = 'rgba(233,220,196,0.4)'; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(w * 0.08, h * 0.92); ctx.lineTo(w * 0.92, h * 0.92); ctx.moveTo(w * 0.86, h * 0.06); ctx.lineTo(w * 0.86, h * 0.95); ctx.stroke();
    const img = ctx.getImageData(0, 0, w, h), d = img.data;
    for (let i = 0; i < d.length; i += 4) { const n = (r() - 0.5) * 14; d[i] += n; d[i + 1] += n; d[i + 2] += n; }
    ctx.putImageData(img, 0, 0);
  },
  stilllife(ctx, w, h, r) {
    ctx.fillStyle = '#0c0907'; ctx.fillRect(0, 0, w, h);
    softGlow(ctx, w * 0.45, h * 0.42, w * 0.6, 'rgba(120,78,38,0.55)');
    let g = ctx.createLinearGradient(0, h * 0.72, 0, h);
    g.addColorStop(0, '#4a2e18'); g.addColorStop(0.08, '#2a190d'); g.addColorStop(1, '#0d0805');
    ctx.fillStyle = g; ctx.fillRect(0, h * 0.72, w, h * 0.28);
    const vx = w * 0.46;
    g = ctx.createLinearGradient(vx - w * 0.12, 0, vx + w * 0.12, 0);
    g.addColorStop(0, '#11160d'); g.addColorStop(0.35, '#55664a'); g.addColorStop(1, '#0c0f08');
    ctx.fillStyle = g; ctx.beginPath();
    ctx.moveTo(vx - w * 0.05, h * 0.73); ctx.bezierCurveTo(vx - w * 0.16, h * 0.66, vx - w * 0.14, h * 0.5, vx - w * 0.05, h * 0.47);
    ctx.lineTo(vx + w * 0.05, h * 0.47); ctx.bezierCurveTo(vx + w * 0.14, h * 0.5, vx + w * 0.16, h * 0.66, vx + w * 0.05, h * 0.73); ctx.fill();
    for (let i = 0; i < 16; i++) {
      ctx.save(); ctx.translate(vx + (r() - 0.5) * w * 0.5, h * (0.3 + r() * 0.25)); ctx.rotate(r() * TAU);
      ctx.fillStyle = r() > 0.5 ? '#2f4a26' : '#1f3318';
      ctx.beginPath(); ctx.ellipse(0, 0, w * 0.06, w * 0.018, 0, 0, TAU); ctx.fill(); ctx.restore();
    }
    const pal = [[232, 199, 181], [196, 90, 74], [241, 227, 200], [155, 47, 53], [231, 168, 106]];
    for (let i = 0; i < 15; i++) {
      const fx = vx + (r() + r() - 1) * w * 0.22, fy = h * 0.3 + (r() + r() - 1) * h * 0.13, fr = w * (0.035 + r() * 0.05);
      const c = pal[(r() * pal.length) | 0];
      const fg = ctx.createRadialGradient(fx - fr * 0.3, fy - fr * 0.3, fr * 0.1, fx, fy, fr);
      fg.addColorStop(0, rgba(c[0] * 1.1, c[1] * 1.1, c[2] * 1.1)); fg.addColorStop(1, rgba(c[0] * 0.35, c[1] * 0.35, c[2] * 0.35));
      ctx.fillStyle = fg; ctx.beginPath(); ctx.arc(fx, fy, fr, 0, TAU); ctx.fill();
      ctx.strokeStyle = rgba(c[0] * 0.5, c[1] * 0.5, c[2] * 0.5, 0.6); ctx.lineWidth = 1.5;
      for (let p = 0; p < 6; p++) { const a = r() * TAU; ctx.beginPath(); ctx.arc(fx, fy, fr * (0.3 + r() * 0.6), a, a + 1.2); ctx.stroke(); }
    }
    const fruit = (x, y, rad, c) => {
      const fg = ctx.createRadialGradient(x - rad * 0.35, y - rad * 0.35, rad * 0.1, x, y, rad);
      fg.addColorStop(0, c[0]); fg.addColorStop(1, c[1]); ctx.fillStyle = fg;
      ctx.beginPath(); ctx.arc(x, y, rad, 0, TAU); ctx.fill();
    };
    fruit(w * 0.72, h * 0.76, w * 0.05, ['#8a3a52', '#2a0f18']);
    fruit(w * 0.8, h * 0.78, w * 0.04, ['#9a4a5e', '#2a0f18']);
    fruit(w * 0.22, h * 0.77, w * 0.055, ['#f2c35a', '#5a3a0a']);
  },
  gallery(ctx, w, h, r) {
    const vx = w * 0.5, vy = h * 0.5;
    let g = ctx.createLinearGradient(0, 0, 0, vy);
    g.addColorStop(0, '#6a4a2c'); g.addColorStop(1, '#d9b98a');
    ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = '#e6d2ae'; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(vx - w * 0.08, vy - h * 0.12); ctx.lineTo(vx - w * 0.08, vy + h * 0.08); ctx.lineTo(0, h); ctx.fill();
    ctx.fillStyle = '#cfb48a'; ctx.beginPath(); ctx.moveTo(w, 0); ctx.lineTo(vx + w * 0.08, vy - h * 0.12); ctx.lineTo(vx + w * 0.08, vy + h * 0.08); ctx.lineTo(w, h); ctx.fill();
    g = ctx.createLinearGradient(0, vy, 0, h);
    g.addColorStop(0, '#b47a40'); g.addColorStop(1, '#6a3e1c');
    ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(0, h); ctx.lineTo(vx - w * 0.08, vy + h * 0.08); ctx.lineTo(vx + w * 0.08, vy + h * 0.08); ctx.lineTo(w, h); ctx.fill();
    softGlow(ctx, vx, vy - h * 0.02, w * 0.12, 'rgba(255,236,190,1)');
    for (let i = 0; i < 6; i++) {
      const t = Math.pow(0.72, i), x0 = vx - (vx) * t, top = vy - (vy * 0.85) * t, bot = vy + (h - vy) * 0.55 * t;
      ctx.fillStyle = 'rgba(70,40,20,0.75)'; ctx.fillRect(x0 + w * 0.03 * t, top + (bot - top) * 0.3, w * 0.07 * t, (bot - top) * 0.35);
      ctx.strokeStyle = 'rgba(214,170,90,0.9)'; ctx.lineWidth = 2 * t + 0.5; ctx.strokeRect(x0 + w * 0.03 * t, top + (bot - top) * 0.3, w * 0.07 * t, (bot - top) * 0.35);
      const x1 = w - x0 - w * 0.1 * t;
      ctx.fillStyle = 'rgba(255,230,170,0.85)'; ctx.fillRect(x1, top + (bot - top) * 0.15, w * 0.06 * t, (bot - top) * 0.55);
    }
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    for (let i = 0; i < 5; i++) {
      const t = Math.pow(0.72, i), x1 = w - (vx) * (1 - (1 - t)) * 0.9;
      const sg = ctx.createLinearGradient(x1, 0, x1 - w * 0.3 * t, h);
      sg.addColorStop(0, 'rgba(255,214,150,0.22)'); sg.addColorStop(1, 'rgba(255,214,150,0)');
      ctx.fillStyle = sg; ctx.beginPath(); ctx.moveTo(x1, vy - h * 0.2 * t); ctx.lineTo(x1 + w * 0.04 * t, vy - h * 0.2 * t); ctx.lineTo(x1 - w * 0.25 * t, h); ctx.lineTo(x1 - w * 0.36 * t, h); ctx.fill();
    }
    ctx.restore();
  },
  sculpture(ctx, w, h, r) {
    const g = ctx.createRadialGradient(w * 0.5, h * 0.4, w * 0.05, w * 0.5, h * 0.5, w * 0.8);
    g.addColorStop(0, '#5f5a54'); g.addColorStop(1, '#141210');
    ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = '#25221f'; ctx.fillRect(w * 0.25, h * 0.84, w * 0.5, h * 0.16);
    ctx.fillStyle = 'rgba(0,0,0,0.35)'; ctx.beginPath(); ctx.ellipse(w * 0.56, h * 0.84, w * 0.3, h * 0.025, 0, 0, TAU); ctx.fill();
    const bust = () => {
      ctx.beginPath(); ctx.ellipse(w * 0.5, h * 0.36, w * 0.17, h * 0.17, 0, 0, TAU);
      ctx.moveTo(w * 0.42, h * 0.5); ctx.lineTo(w * 0.58, h * 0.5); ctx.lineTo(w * 0.6, h * 0.62); ctx.lineTo(w * 0.4, h * 0.62); ctx.closePath();
      ctx.moveTo(w * 0.2, h * 0.84); ctx.bezierCurveTo(w * 0.2, h * 0.66, w * 0.34, h * 0.6, w * 0.5, h * 0.6);
      ctx.bezierCurveTo(w * 0.66, h * 0.6, w * 0.8, h * 0.66, w * 0.8, h * 0.84); ctx.closePath();
    };
    ctx.save(); ctx.beginPath(); ctx.rect(0, 0, w * 0.5, h); ctx.clip(); bust();
    let ag = ctx.createRadialGradient(w * 0.38, h * 0.3, w * 0.02, w * 0.45, h * 0.5, w * 0.45);
    ag.addColorStop(0, '#fbf6ec'); ag.addColorStop(0.6, '#d8d0c2'); ag.addColorStop(1, '#8c8478');
    ctx.fillStyle = ag; ctx.fill(); ctx.restore();
    ctx.save(); ctx.beginPath(); ctx.rect(w * 0.5, 0, w * 0.5, h); ctx.clip(); bust();
    ag = ctx.createLinearGradient(w * 0.5, 0, w * 0.8, 0);
    ag.addColorStop(0, '#d9a45a'); ag.addColorStop(0.3, '#8a5a28'); ag.addColorStop(0.7, '#3a220e'); ag.addColorStop(1, '#1a0f06');
    ctx.fillStyle = ag; ctx.fill(); ctx.clip();
    ctx.strokeStyle = 'rgba(255,220,160,0.25)'; ctx.lineWidth = 1;
    for (let i = 0; i < 80; i++) { const y = r() * h; ctx.beginPath(); ctx.moveTo(w * 0.5, y); ctx.lineTo(w * 0.9, y + (r() - 0.5) * 6); ctx.stroke(); }
    ctx.restore();
    ctx.fillStyle = 'rgba(60,50,40,0.25)';
    ctx.beginPath(); ctx.ellipse(w * 0.44, h * 0.33, w * 0.03, h * 0.012, 0, 0, TAU); ctx.fill();
    ctx.beginPath(); ctx.ellipse(w * 0.47, h * 0.42, w * 0.03, h * 0.008, 0, 0, TAU); ctx.fill();
    ctx.strokeStyle = '#e8c27a'; ctx.lineWidth = 2.5;
    ctx.beginPath(); ctx.moveTo(w * 0.5, h * 0.18); ctx.lineTo(w * 0.5, h * 0.84); ctx.stroke();
  },
  geometric(ctx, w, h, r) {
    ctx.fillStyle = '#efe6d4'; ctx.fillRect(0, 0, w, h);
    const cols = 6, rows = 4, cw = w / cols, ch = h / rows;
    const pal = ['#c9542f', '#1f3a5a', '#d9a432', '#1a1a1a', '#7a8c6e', '#efe6d4'];
    ctx.strokeStyle = 'rgba(30,30,30,0.12)'; ctx.lineWidth = 1;
    for (let i = 1; i < cols; i++) { ctx.beginPath(); ctx.moveTo(i * cw, 0); ctx.lineTo(i * cw, h); ctx.stroke(); }
    for (let j = 1; j < rows; j++) { ctx.beginPath(); ctx.moveTo(0, j * ch); ctx.lineTo(w, j * ch); ctx.stroke(); }
    for (let j = 0; j < rows; j++) for (let i = 0; i < cols; i++) {
      const x = i * cw, y = j * ch, type = (r() * 6) | 0, c = pal[(r() * 5) | 0];
      ctx.fillStyle = c; ctx.save(); ctx.translate(x + cw / 2, y + ch / 2); ctx.rotate(((r() * 4) | 0) * Math.PI / 2);
      const s = Math.min(cw, ch) * 0.42;
      if (type === 0) { ctx.beginPath(); ctx.arc(0, 0, s, 0, TAU); ctx.fill(); }
      else if (type === 1) { ctx.beginPath(); ctx.moveTo(-s, s); ctx.arc(-s, s, s * 2, -Math.PI / 2, 0); ctx.closePath(); ctx.fill(); }
      else if (type === 2) { ctx.fillRect(-s, -s * 0.25, s * 2, s * 0.5); }
      else if (type === 3) { ctx.beginPath(); ctx.arc(0, 0, s, 0, Math.PI); ctx.fill(); }
      else if (type === 4) { ctx.lineWidth = s * 0.18; ctx.strokeStyle = c; ctx.beginPath(); ctx.arc(0, 0, s * 0.8, 0, TAU); ctx.stroke(); }
      else { for (let k = 0; k < 3; k++) { ctx.beginPath(); ctx.arc(-s * 0.6 + k * s * 0.6, 0, s * 0.22, 0, TAU); ctx.fill(); } }
      ctx.restore();
    }
    ctx.fillStyle = '#c9542f'; ctx.beginPath(); ctx.arc(w * 0.68, h * 0.42, h * 0.3, 0, TAU); ctx.globalAlpha = 0.85; ctx.fill(); ctx.globalAlpha = 1;
    ctx.fillStyle = '#1a1a1a'; ctx.fillRect(w * 0.1, h * 0.78, w * 0.8, h * 0.015);
  },
  nocturne(ctx, w, h, r) {
    const hz = h * 0.62;
    let g = ctx.createLinearGradient(0, 0, 0, hz);
    g.addColorStop(0, '#050914'); g.addColorStop(0.7, '#17264a'); g.addColorStop(1, '#2d3d62');
    ctx.fillStyle = g; ctx.fillRect(0, 0, w, hz);
    for (let i = 0; i < 260; i++) { ctx.fillStyle = `rgba(255,250,230,${r() * 0.8})`; ctx.fillRect(r() * w, r() * hz * 0.85, r() * 2 + 0.5, r() * 2 + 0.5); }
    softGlow(ctx, w * 0.68, h * 0.2, w * 0.35, 'rgba(160,180,230,0.55)');
    ctx.fillStyle = '#f4ecd2'; ctx.beginPath(); ctx.arc(w * 0.68, h * 0.2, w * 0.06, 0, TAU); ctx.fill();
    g = ctx.createLinearGradient(0, hz, 0, h);
    g.addColorStop(0, '#16223e'); g.addColorStop(1, '#03060d');
    ctx.fillStyle = g; ctx.fillRect(0, hz, w, h - hz);
    ctx.fillStyle = '#070b16';
    let x = 0;
    while (x < w * 0.55) { const bw = w * (0.03 + r() * 0.06), bh = h * (0.03 + r() * 0.1); ctx.fillRect(x, hz - bh, bw, bh); for (let k = 0; k < 3; k++) if (r() > 0.5) { ctx.fillStyle = 'rgba(255,190,90,0.9)'; ctx.fillRect(x + r() * bw * 0.8, hz - bh + r() * bh * 0.8, 3, 4); ctx.fillStyle = '#070b16'; } x += bw; }
    for (let i = 0; i < 110; i++) {
      const y = hz + r() * (h - hz), xx = w * 0.68 + (r() - 0.5) * w * 0.12 * (1 + (y - hz) / (h - hz));
      ctx.strokeStyle = `rgba(220,225,240,${0.45 * (1 - (y - hz) / (h - hz))})`; ctx.lineWidth = 1 + r() * 2;
      ctx.beginPath(); ctx.moveTo(xx, y); ctx.lineTo(xx + w * 0.03, y); ctx.stroke();
    }
    ctx.fillStyle = '#05070d'; ctx.beginPath(); ctx.moveTo(w * 0.18, h * 0.7); ctx.lineTo(w * 0.42, h * 0.7); ctx.lineTo(w * 0.38, h * 0.74); ctx.lineTo(w * 0.22, h * 0.74); ctx.fill();
    ctx.fillRect(w * 0.29, h * 0.52, 3, h * 0.18);
    softGlow(ctx, w * 0.33, h * 0.67, w * 0.12, 'rgba(255,200,110,0.9)');
    ctx.fillStyle = '#ffe2a0'; ctx.beginPath(); ctx.arc(w * 0.33, h * 0.67, 5, 0, TAU); ctx.fill();
    for (let i = 0; i < 40; i++) { const y = h * 0.75 + r() * h * 0.22; ctx.strokeStyle = `rgba(255,190,100,${0.4 * (1 - (y - h * 0.75) / (h * 0.22))})`; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(w * 0.33 + (r() - 0.5) * 30, y); ctx.lineTo(w * 0.33 + (r() - 0.5) * 30 + 14, y); ctx.stroke(); }
  }
};
const PainterlyOptions = {
  courtyard: { count: 7000, len: 14, width: 4, jitter: 0.25 },
  seascape: { count: 6000, len: 18, width: 4, jitter: 0.2, angle: 0 },
  stilllife: { count: 5000, len: 10, width: 4, jitter: 0.2 },
  gallery: { count: 11000, len: 9, width: 5, jitter: 0.35, alpha: 0.7 },
  sculpture: { count: 2500, len: 8, width: 3, jitter: 0.12, alpha: 0.35 },
  nocturne: { count: 4500, len: 12, width: 3.5, jitter: 0.3, angle: 0 }
};
function paintArtwork(style, orientation, seed) {
  const w = orientation === 'portrait' ? 768 : 1024, h = orientation === 'portrait' ? 1024 : 768;
  const [c, ctx] = makeCanvas(w, h);
  const r = rng(seed);
  (Painters[style] || Painters.abstract)(ctx, w, h, r);
  if (PainterlyOptions[style]) painterlyPass(ctx, w, h, r, PainterlyOptions[style]);
  canvasFinish(ctx, w, h, style === 'geometric' ? 0.18 : 0.4);
  return c;
}

/* --------------------------------------------------------------------------
   4.4  Renderer, scene, camera
   -------------------------------------------------------------------------- */
const stage = $('stage');
const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.75));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 0.88;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
stage.appendChild(renderer.domElement);
const MAX_ANISO = renderer.capabilities.getMaxAnisotropy();

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x001514);
scene.fog = new THREE.Fog(0x001514, 16, 52);
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
scene.environmentIntensity = 0.12;

const EYE_HEIGHT = 1.7;
const camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 0.15, 120);
camera.position.set(0, 3, 6);

/* --------------------------------------------------------------------------
   4.5  Texture management — load files, fall back to canvases instantly
   -------------------------------------------------------------------------- */
const loadTracker = { total: 0, done: 0, ok: 0 };
function updateLoadStatus() {
  const el = $('loadStatus'), txt = $('loadText');
  if (loadTracker.done < loadTracker.total) {
    txt.textContent = `Hanging the collection… ${loadTracker.done}/${loadTracker.total}`;
  } else {
    el.classList.add('done');
    const fallback = loadTracker.total - loadTracker.ok;
    txt.textContent = fallback > 0
      ? `Galleries open · ${fallback} work${fallback > 1 ? 's' : ''} rendered procedurally`
      : 'Galleries open';
  }
}
const texLoader = new THREE.TextureLoader();
/**
 * Creates a texture backed by a procedural canvas immediately, then swaps in
 * the image file at `path` (if any) once it loads. Errors keep the fallback.
 */
function managedTexture(canvas, path, { repeat = false, onLoad = null } = {}) {
  const tex = new THREE.CanvasTexture(canvas);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = MAX_ANISO;
  if (repeat) tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  if (path) {
    loadTracker.total++;
    texLoader.load(path, (loaded) => {
      loaded.colorSpace = THREE.SRGBColorSpace;
      loaded.anisotropy = MAX_ANISO;
      if (repeat) {
        loaded.wrapS = loaded.wrapT = THREE.RepeatWrapping;
        loaded.repeat.copy(tex.repeat);
      }
      tex.image = loaded.image;
      tex.needsUpdate = true;
      loadTracker.done++; loadTracker.ok++;
      if (onLoad) onLoad(loaded.image);
      updateLoadStatus();
    }, undefined, () => {
      loadTracker.done++;
      updateLoadStatus();
    });
  }
  return tex;
}

/* Canvas text textures are re-drawn once the web fonts are available. */
const textTextures = [];
function textTexture(w, h, draw) {
  const [c, ctx] = makeCanvas(w, h);
  draw(ctx, w, h);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = MAX_ANISO;
  textTextures.push({ ctx, w, h, draw, t });
  return t;
}
function spacedText(ctx, text, x, y, spacing, align = 'center') {
  const chars = [...text];
  const widths = chars.map((ch) => ctx.measureText(ch).width);
  const total = widths.reduce((a, b) => a + b, 0) + spacing * (chars.length - 1);
  let cx = align === 'center' ? x - total / 2 : align === 'right' ? x - total : x;
  const prev = ctx.textAlign; ctx.textAlign = 'left';
  chars.forEach((ch, i) => { ctx.fillText(ch, cx, y); cx += widths[i] + spacing; });
  ctx.textAlign = prev;
  return total;
}
const SERIF = "'Cormorant Garamond', 'Times New Roman', serif";
const SANS = "'Plus Jakarta Sans', 'Segoe UI', sans-serif";
function wrapText(ctx, text, x, y, maxW, lineH) {
  const words = text.split(' ');
  let line = '';
  for (const word of words) {
    const test = line ? line + ' ' + word : word;
    if (ctx.measureText(test).width > maxW && line) { ctx.fillText(line, x, y); line = word; y += lineH; }
    else line = test;
  }
  if (line) ctx.fillText(line, x, y);
  return y;
}

/* --------------------------------------------------------------------------
   4.6  Materials
   -------------------------------------------------------------------------- */
const M_CHECKER = managedTexture(ProcTex.checkeredMarble(512), EUNOIA_CONFIG.textures?.floorMarble, { repeat: true });
M_CHECKER.repeat.set(7, 7);

const M_HERRING = managedTexture(ProcTex.herringbone(512), EUNOIA_CONFIG.textures?.floorWood, { repeat: true });
M_HERRING.repeat.set(6, 6);

const T_PLASTER = new THREE.CanvasTexture(ProcTex.plaster(256));
T_PLASTER.wrapS = T_PLASTER.wrapT = THREE.RepeatWrapping;
T_PLASTER.repeat.set(6, 3);
T_PLASTER.anisotropy = MAX_ANISO;

const T_DAMASK = new THREE.CanvasTexture(ProcTex.damask(512));
T_DAMASK.wrapS = T_DAMASK.wrapT = THREE.RepeatWrapping;
T_DAMASK.repeat.set(8, 4);
T_DAMASK.anisotropy = MAX_ANISO;

const T_WHITE_MARBLE = new THREE.CanvasTexture(ProcTex.whiteMarble(512));
T_WHITE_MARBLE.wrapS = T_WHITE_MARBLE.wrapT = THREE.RepeatWrapping;
T_WHITE_MARBLE.repeat.set(2, 2);
T_WHITE_MARBLE.anisotropy = MAX_ANISO;

const T_COFFER_ROT = new THREE.CanvasTexture(ProcTex.coffer(512, [251, 255, 254], '#e6af2e'));
T_COFFER_ROT.wrapS = T_COFFER_ROT.wrapT = THREE.RepeatWrapping;
T_COFFER_ROT.repeat.set(6, 6);
T_COFFER_ROT.anisotropy = MAX_ANISO;

const Mat = {
  floorRotunda: new THREE.MeshStandardMaterial({ map: M_CHECKER, roughness: 0.22, metalness: 0.05 }),
  floorWingI:   new THREE.MeshStandardMaterial({ map: M_HERRING, roughness: 0.32, metalness: 0.04 }),
  floorWingII:  new THREE.MeshStandardMaterial({ map: M_CHECKER, roughness: 0.18, metalness: 0.05 }),
  floorWingIII: new THREE.MeshStandardMaterial({ map: M_HERRING, roughness: 0.40, metalness: 0.04 }),

  wallRotunda:  new THREE.MeshStandardMaterial({ color: 0xfbfffe, map: T_PLASTER, roughness: 0.85 }),
  ceilingRot:   new THREE.MeshStandardMaterial({ map: T_COFFER_ROT, roughness: 0.65 }),
  archTrim:     new THREE.MeshStandardMaterial({ color: 0xfbfffe, roughness: 0.55 }),

  wallWingI:    new THREE.MeshStandardMaterial({ color: 0x6b0504, map: T_DAMASK, roughness: 0.62 }), // BLOOD RED
  trimWingI:    new THREE.MeshStandardMaterial({ color: 0x400302, roughness: 0.5 }), // Deep bloodwood
  ceilingWingI: new THREE.MeshStandardMaterial({ color: 0xfbfffe, map: T_COFFER_ROT, roughness: 0.65 }),

  wallWingII:   new THREE.MeshStandardMaterial({ color: 0xfbfffe, map: T_PLASTER, roughness: 0.88 }), // WHITE
  trimWingII:   new THREE.MeshStandardMaterial({ color: 0x001514, roughness: 0.45 }), // RICH BLACK
  ceilingWingII:new THREE.MeshStandardMaterial({ color: 0xfbfffe, roughness: 0.75 }),

  wallWingIII:  new THREE.MeshStandardMaterial({ color: 0x001514, map: T_PLASTER, roughness: 0.92 }), // RICH BLACK
  trimWingIII:  new THREE.MeshStandardMaterial({ color: 0x051d1c, roughness: 0.5 }), // RICH BLACK
  ceilingWingIII:new THREE.MeshStandardMaterial({ color: 0x001514, roughness: 0.85 }),

  flutedColumn: new THREE.MeshStandardMaterial({ color: 0xfbfffe, map: T_WHITE_MARBLE, roughness: 0.30, metalness: 0.03 }),
  pedestal:     new THREE.MeshStandardMaterial({ color: 0x001514, roughness: 0.28, metalness: 0.15 }), // RICH BLACK
  goldLeaf:     new THREE.MeshStandardMaterial({ color: 0xe6af2e, roughness: 0.25, metalness: 0.88 }), // XANTHOUS
  darkWood:     new THREE.MeshStandardMaterial({ color: 0xa3320b, roughness: 0.45, metalness: 0.05 }), // BROWN
  bronze:       new THREE.MeshStandardMaterial({ color: 0xb88628, roughness: 0.32, metalness: 0.82 }), // Xanthous Bronze
  blackVelvet:  new THREE.MeshStandardMaterial({ color: 0x001514, roughness: 0.88 }), // RICH BLACK
  crimsonVelvet:new THREE.MeshStandardMaterial({ color: 0x6b0504, roughness: 0.85 }), // BLOOD RED
  alabaster:    new THREE.MeshStandardMaterial({ color: 0xfbfffe, map: T_WHITE_MARBLE, roughness: 0.25, metalness: 0.05 }) // WHITE
};

/* --------------------------------------------------------------------------
   4.7  Collider system (AABB + Cylinder against player sphere)
   -------------------------------------------------------------------------- */
const Colliders = [];
function addBoxCollider(cx, cz, hx, hz) {
  Colliders.push({ type: 'box', minX: cx - hx, maxX: cx + hx, minZ: cz - hz, maxZ: cz + hz });
}
function addRotatedBoxCollider(cx, cz, hx, hz, rotY) {
  Colliders.push({ type: 'obb', cx, cz, hx, hz, rotY, cos: Math.cos(rotY), sin: Math.sin(rotY) });
}
function addCylCollider(cx, cz, r) {
  Colliders.push({ type: 'cyl', cx, cz, r });
}
function addWallSegment(x1, z1, x2, z2) {
  Colliders.push({ type: 'segment', x1, z1, x2, z2 });
}
const PLAYER_R = 0.45;
function resolveCollision(pos) {
  for (let iter = 0; iter < 4; iter++) {
    for (const c of Colliders) {
      if (c.type === 'box') {
        const nx = clamp(pos.x, c.minX, c.maxX), nz = clamp(pos.z, c.minZ, c.maxZ);
        const dx = pos.x - nx, dz = pos.z - nz, d2 = dx * dx + dz * dz;
        if (d2 < PLAYER_R * PLAYER_R) {
          const d = Math.sqrt(d2);
          if (d > 0.0001) {
            pos.x = nx + (dx / d) * PLAYER_R;
            pos.z = nz + (dz / d) * PLAYER_R;
          } else {
            const left = Math.abs(pos.x - c.minX), right = Math.abs(pos.x - c.maxX);
            const top = Math.abs(pos.z - c.minZ), bot = Math.abs(pos.z - c.maxZ);
            const m = Math.min(left, right, top, bot);
            if (m === left) pos.x = c.minX - PLAYER_R;
            else if (m === right) pos.x = c.maxX + PLAYER_R;
            else if (m === top) pos.z = c.minZ - PLAYER_R;
            else pos.z = c.maxZ + PLAYER_R;
          }
        }
      } else if (c.type === 'obb') {
        // Transform point to box local coordinates:
        // Forward: [dx] = [cos  sin] [lx]
        //          [dz]   [-sin cos] [lz]
        // Inverse: lx = dx * cos - dz * sin
        //          lz = dx * sin + dz * cos
        const dx = pos.x - c.cx, dz = pos.z - c.cz;
        const lx = dx * c.cos - dz * c.sin;
        const lz = dx * c.sin + dz * c.cos;
        const clx = clamp(lx, -c.hx, c.hx);
        const clz = clamp(lz, -c.hz, c.hz);
        const diffX = lx - clx, diffZ = lz - clz;
        const d2 = diffX * diffX + diffZ * diffZ;
        if (d2 < PLAYER_R * PLAYER_R) {
          const d = Math.sqrt(d2);
          let pushLX, pushLZ;
          if (d > 0.0001) {
            pushLX = clx + (diffX / d) * PLAYER_R;
            pushLZ = clz + (diffZ / d) * PLAYER_R;
          } else {
            const dLeft = Math.abs(lx - (-c.hx)), dRight = Math.abs(lx - c.hx);
            const dTop = Math.abs(lz - (-c.hz)), dBot = Math.abs(lz - c.hz);
            const m = Math.min(dLeft, dRight, dTop, dBot);
            pushLX = lx; pushLZ = lz;
            if (m === dLeft) pushLX = -c.hx - PLAYER_R;
            else if (m === dRight) pushLX = c.hx + PLAYER_R;
            else if (m === dTop) pushLZ = -c.hz - PLAYER_R;
            else pushLZ = c.hz + PLAYER_R;
          }
          // Transform local push back to world coordinates
          pos.x = c.cx + pushLX * c.cos + pushLZ * c.sin;
          pos.z = c.cz - pushLX * c.sin + pushLZ * c.cos;
        }
      } else if (c.type === 'cyl') {
        const dx = pos.x - c.cx, dz = pos.z - c.cz, d2 = dx * dx + dz * dz;
        const minD = c.r + PLAYER_R;
        if (d2 < minD * minD) {
          const d = Math.max(0.0001, Math.sqrt(d2));
          pos.x = c.cx + (dx / d) * minD;
          pos.z = c.cz + (dz / d) * minD;
        }
      } else if (c.type === 'segment') {
        // Line segment collision test
        const vx = c.x2 - c.x1, vz = c.z2 - c.z1;
        const len2 = vx * vx + vz * vz;
        let t = 0;
        if (len2 > 0.00001) {
          t = ((pos.x - c.x1) * vx + (pos.z - c.z1) * vz) / len2;
          t = clamp(t, 0, 1);
        }
        const nx = c.x1 + t * vx, nz = c.z1 + t * vz;
        const dx = pos.x - nx, dz = pos.z - nz;
        const d2 = dx * dx + dz * dz;
        if (d2 < PLAYER_R * PLAYER_R) {
          const d = Math.sqrt(d2);
          if (d > 0.0001) {
            pos.x = nx + (dx / d) * PLAYER_R;
            pos.z = nz + (dz / d) * PLAYER_R;
          } else {
            // Normal to segment
            const normX = -vz / Math.sqrt(len2), normZ = vx / Math.sqrt(len2);
            pos.x = nx + normX * PLAYER_R;
            pos.z = nz + normZ * PLAYER_R;
          }
        }
      }
    }
  }
}

/* --------------------------------------------------------------------------
   4.8  Geometry builders (museum props & architectural features)
   -------------------------------------------------------------------------- */
function buildFlutedColumn(h = 6.0, r = 0.42) {
  const g = new THREE.Group();
  const plinth = new THREE.Mesh(new THREE.BoxGeometry(r * 2.7, 0.22, r * 2.7), Mat.archTrim);
  plinth.position.y = 0.11; plinth.castShadow = true; plinth.receiveShadow = true;
  const torus = new THREE.Mesh(new THREE.CylinderGeometry(r * 1.25, r * 1.35, 0.2, 24), Mat.flutedColumn);
  torus.position.y = 0.32;
  const shaftH = h - 0.9;
  const flutes = 20, curves = [];
  for (let i = 0; i < flutes; i++) {
    const a0 = (i / flutes) * TAU, a1 = ((i + 1) / flutes) * TAU, mid = (a0 + a1) / 2;
    curves.push(new THREE.Vector2(Math.cos(a0) * r, Math.sin(a0) * r));
    const flR = r * 0.94;
    curves.push(new THREE.Vector2(Math.cos(mid) * flR, Math.sin(mid) * flR));
  }
  const shape = new THREE.Shape(curves);
  const shaft = new THREE.Mesh(new THREE.ExtrudeGeometry(shape, { depth: shaftH, bevelEnabled: false }), Mat.flutedColumn);
  shaft.rotation.x = -Math.PI / 2; shaft.position.y = 0.42; shaft.castShadow = true; shaft.receiveShadow = true;
  const cap = new THREE.Mesh(new THREE.BoxGeometry(r * 2.7, 0.25, r * 2.7), Mat.archTrim);
  cap.position.y = h - 0.125;
  const echinus = new THREE.Mesh(new THREE.CylinderGeometry(r * 1.3, r, 0.22, 24), Mat.flutedColumn);
  echinus.position.y = h - 0.35;
  g.add(plinth, torus, shaft, echinus, cap);
  return g;
}

function buildMuseumBench(matWood = Mat.darkWood, matCushion = Mat.crimsonVelvet) {
  const g = new THREE.Group();
  const seatL = 3.4, seatW = 0.95, seatH = 0.48;
  const base = new THREE.Mesh(new RoundedBoxGeometry(seatL, 0.08, seatW, 4, 0.02), matWood);
  base.position.y = seatH - 0.12; base.castShadow = true; base.receiveShadow = true;
  const cushion = new THREE.Mesh(new RoundedBoxGeometry(seatL - 0.1, 0.12, seatW - 0.1, 5, 0.04), matCushion);
  cushion.position.y = seatH - 0.02; cushion.castShadow = true; cushion.receiveShadow = true;
  const legG = new THREE.CylinderGeometry(0.04, 0.03, seatH - 0.16, 12);
  const legPositions = [
    [-seatL / 2 + 0.25, -seatW / 2 + 0.15],
    [-seatL / 2 + 0.25,  seatW / 2 - 0.15],
    [ seatL / 2 - 0.25, -seatW / 2 + 0.15],
    [ seatL / 2 - 0.25,  seatW / 2 - 0.15]
  ];
  legPositions.forEach(([x, z]) => {
    const leg = new THREE.Mesh(legG, Mat.bronze);
    leg.position.set(x, (seatH - 0.16) / 2, z); leg.castShadow = true; g.add(leg);
  });
  const rail = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, seatL - 0.5, 8), Mat.bronze);
  rail.rotation.z = Math.PI / 2; rail.position.y = 0.14;
  g.add(base, cushion, rail);
  return g;
}

function buildTrackLight(len = 16) {
  const g = new THREE.Group();
  const rail = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.04, len), Mat.pedestal);
  rail.position.y = 5.2;
  g.add(rail);
  const heads = Math.floor(len / 2.6);
  for (let i = 0; i <= heads; i++) {
    const z = -len / 2 + 1.2 + i * 2.6;
    const can = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.07, 0.18, 12), Mat.pedestal);
    can.rotation.x = Math.PI / 4; can.position.set(0, 5.1, z);
    const bulb = new THREE.Mesh(new THREE.CircleGeometry(0.04, 12), new THREE.MeshBasicMaterial({ color: 0xffe2a4 }));
    bulb.rotation.x = Math.PI / 4; bulb.position.set(0, 5.04, z + 0.06);
    g.add(can, bulb);
  }
  return g;
}

function buildWallPortal(key, label, sub, wallMat) {
  const g = new THREE.Group();

  const doorHalfW = 1.50; // clear opening from -1.50 to +1.50 (3.0m wide)
  const doorH = 3.20;     // clear opening height 3.20m
  const jambW = 0.35;     // jamb casing from 1.50 to 1.85 (35cm wide)
  const jambX = doorHalfW + jambW / 2; // 1.675
  const casingHalfW = doorHalfW + jambW; // 1.85 (outer edge of doorframe casing)

  // Fluted jamb pilasters flanking the doorway (depth 0.48: projects 6cm beyond walls)
  const jambG = new THREE.BoxGeometry(jambW, doorH, 0.48);
  const jL = new THREE.Mesh(jambG, Mat.archTrim), jR = new THREE.Mesh(jambG, Mat.archTrim);
  jL.position.set(-jambX, doorH / 2, 0);
  jR.position.set(jambX, doorH / 2, 0);
  jL.castShadow = true; jR.castShadow = true;

  // Lintel / Architrave spanning above the doorway across both jambs
  const lintelH = 0.22;
  const lintel = new THREE.Mesh(new RoundedBoxGeometry(casingHalfW * 2, lintelH, 0.48, 3, 0.02), Mat.archTrim);
  lintel.position.set(0, doorH + lintelH / 2, 0);
  lintel.castShadow = true;

  // Entablature Frieze (Sign band backing both plaques)
  const friezeH = 0.80;
  const friezeY = doorH + lintelH + friezeH / 2; // 3.82
  const frieze = new THREE.Mesh(new RoundedBoxGeometry(casingHalfW * 2, friezeH, 0.44, 3, 0.02), Mat.archTrim);
  frieze.position.set(0, friezeY, 0);
  frieze.castShadow = true;

  // Classical molded cornice crown above the frieze
  const corniceH = 0.18;
  const cornice = new THREE.Mesh(new RoundedBoxGeometry(casingHalfW * 2, corniceH, 0.50, 3, 0.02), Mat.archTrim);
  cornice.position.set(0, doorH + lintelH + friezeH + corniceH / 2, 0); // 4.31
  cornice.castShadow = true;

  // Solid return walls flanking the portal from corridor wall (-3.5) to casing edge (-1.85)
  const retW = (WING_W / 2) - casingHalfW; // 3.50 - 1.85 = 1.65m
  const retGeom = new THREE.BoxGeometry(retW, H_WING, 0.36); // depth 0.36
  const retL = new THREE.Mesh(retGeom, wallMat || Mat.wallRotunda);
  retL.position.set(-WING_W / 2 + retW / 2, H_WING / 2, 0); // center -2.675
  retL.castShadow = true; retL.receiveShadow = true;

  const retR = new THREE.Mesh(retGeom, wallMat || Mat.wallRotunda);
  retR.position.set(WING_W / 2 - retW / 2, H_WING / 2, 0); // center +2.675
  retR.castShadow = true; retR.receiveShadow = true;

  // Central attic wall between cornice and rotunda ceiling (between -1.85 and +1.85)
  const atticBottom = doorH + lintelH + friezeH + corniceH; // 4.40
  const atticH = H_ROT - atticBottom; // 6.40 - 4.40 = 2.00m
  const attic = new THREE.Mesh(new THREE.BoxGeometry(casingHalfW * 2, atticH, 0.36), wallMat || Mat.wallRotunda);
  attic.position.set(0, atticBottom + atticH / 2, 0);
  attic.castShadow = true; attic.receiveShadow = true;

  // 1. INWARD SIGN (Facing the Grand Rotunda as visitors enter the wing)
  const inSignTex = textTexture(1024, 256, (ctx, w, h) => {
    ctx.fillStyle = '#001514'; ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = '#e6af2e'; ctx.lineWidth = 5; ctx.strokeRect(10, 10, w - 20, h - 20);
    ctx.strokeStyle = 'rgba(230,175,46,0.45)'; ctx.lineWidth = 1.5; ctx.strokeRect(18, 18, w - 36, h - 36);
    ctx.fillStyle = '#e6af2e'; ctx.font = `600 22px ${SANS}`;
    spacedText(ctx, `WING ${key}`.toUpperCase(), w / 2, 52, 6);
    ctx.fillStyle = '#fbfffe'; ctx.font = `600 46px ${SERIF}`;
    spacedText(ctx, label.toUpperCase(), w / 2, 112, 7);
    ctx.strokeStyle = 'rgba(230,175,46,0.55)'; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(w * 0.22, 138); ctx.lineTo(w * 0.78, 138); ctx.stroke();
    ctx.fillStyle = '#dbe4e2'; ctx.font = `italic 24px ${SERIF}`; ctx.textAlign = 'center';
    ctx.fillText(sub, w / 2, 182);
    ctx.fillStyle = '#e6af2e'; ctx.font = `500 15px ${SANS}`;
    ctx.fillText('◆  EUNOIA GALLERIES  ◆', w / 2, 222);
  });
  const signMatIn = new THREE.MeshStandardMaterial({ map: inSignTex, roughness: 0.35, metalness: 0.1 });
  const signIn = new THREE.Mesh(new THREE.PlaneGeometry(2.8, 0.68), signMatIn);
  signIn.position.set(0, friezeY, -0.222);
  signIn.rotation.y = Math.PI; // Face outward into the Grand Rotunda (-Z)

  // 2. OUTWARD SIGN (Facing into the wing as visitors exit back to Grand Rotunda)
  const outSignTex = textTexture(1024, 256, (ctx, w, h) => {
    ctx.fillStyle = '#001514'; ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = '#e6af2e'; ctx.lineWidth = 5; ctx.strokeRect(10, 10, w - 20, h - 20);
    ctx.strokeStyle = 'rgba(230,175,46,0.45)'; ctx.lineWidth = 1.5; ctx.strokeRect(18, 18, w - 36, h - 36);
    ctx.fillStyle = '#e6af2e'; ctx.font = `600 22px ${SANS}`;
    spacedText(ctx, 'CENTRAL FOYER'.toUpperCase(), w / 2, 52, 6);
    ctx.fillStyle = '#fbfffe'; ctx.font = `600 46px ${SERIF}`;
    spacedText(ctx, 'GRAND ROTUNDA', w / 2, 112, 7);
    ctx.strokeStyle = 'rgba(230,175,46,0.55)'; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(w * 0.22, 138); ctx.lineTo(w * 0.78, 138); ctx.stroke();
    ctx.fillStyle = '#dbe4e2'; ctx.font = `italic 24px ${SERIF}`; ctx.textAlign = 'center';
    ctx.fillText('Sculpture Court · Information & Wing Directory', w / 2, 182);
    ctx.fillStyle = '#e6af2e'; ctx.font = `500 15px ${SANS}`;
    ctx.fillText('← RETURN TO FOYER →', w / 2, 222);
  });
  const signMatOut = new THREE.MeshStandardMaterial({ map: outSignTex, roughness: 0.35, metalness: 0.1 });
  const signOut = new THREE.Mesh(new THREE.PlaneGeometry(2.8, 0.68), signMatOut);
  signOut.position.set(0, friezeY, 0.222);
  signOut.rotation.y = 0; // Face inward into the Wing corridor (+Z)

  // Subtle warm gallery accent lights for both entrance and exit signs
  const entrySignLight = new THREE.PointLight(0xffe4a0, 2.5, 5, 1.3);
  entrySignLight.position.set(0, 4.3, -1.2);
  const exitSignLight = new THREE.PointLight(0xffe4a0, 2.5, 5, 1.3);
  exitSignLight.position.set(0, 4.3, 1.2);

  g.add(lintel, frieze, cornice, jL, jR, retL, retR, attic, signIn, signOut, entrySignLight, exitSignLight);
  return g;
}

/* --------------------------------------------------------------------------
   4.9  MUSEUM ARCHITECTURE
   -------------------------------------------------------------------------- */
const H_ROT = 6.4, R_ROT = 8.5;
const WING_W = 7.0, WING_L = 26.0, H_WING = 5.4;

function buildArchitecture() {
  const root = new THREE.Group();

  /* --- 1. Grand Rotunda --- */
  const rotFloor = new THREE.Mesh(new THREE.CylinderGeometry(R_ROT, R_ROT, 0.4, 48), Mat.floorRotunda);
  rotFloor.position.y = -0.2; rotFloor.receiveShadow = true; root.add(rotFloor);

  const rotCeil = new THREE.Mesh(new THREE.CylinderGeometry(R_ROT, R_ROT, 0.3, 48), Mat.ceilingRot);
  rotCeil.position.y = H_ROT + 0.15; root.add(rotCeil);

  // Rotunda walls: 16-sided polygon with openings into the 3 wings & entrance niche
  const segments = 16, dTheta = TAU / segments;
  for (let i = 0; i < segments; i++) {
    const a0 = i * dTheta, a1 = (i + 1) * dTheta, mid = (a0 + a1) / 2;
    // Wing openings: i=0 (East +X, Wing I), i=4 (North +Z, Wing II), i=8 (West -X, Wing III)
    const isWingI = (i === 0 || i === segments - 1);
    const isWingII = (i === 4 || i === 3);
    const isWingIII = (i === 8 || i === 7);
    if (isWingI || isWingII || isWingIII) {
      // Clear doorway opening into wings (portal archway provided cleanly by buildWallPortal)
      continue;
    }
    const chord = 2 * R_ROT * Math.sin(dTheta / 2);
    const wallSeg = new THREE.Mesh(new THREE.BoxGeometry(chord * 1.02, H_ROT, 0.4), Mat.wallRotunda);
    wallSeg.position.set(Math.cos(mid) * R_ROT, H_ROT / 2, Math.sin(mid) * R_ROT);
    wallSeg.rotation.y = -mid + Math.PI / 2;
    wallSeg.castShadow = true; wallSeg.receiveShadow = true; root.add(wallSeg);

    // Continuous line-segment collider for each solid rotunda wall
    const p1x = Math.cos(a0) * (R_ROT - 0.2), p1z = Math.sin(a0) * (R_ROT - 0.2);
    const p2x = Math.cos(a1) * (R_ROT - 0.2), p2z = Math.sin(a1) * (R_ROT - 0.2);
    addWallSegment(p1x, p1z, p2x, p2z);
  }

  // 8 peristyle fluted columns flanking portals and foyer
  const R_COLS = 5.8;
  const colAngles = [
    Math.PI / 6, 2 * Math.PI / 6,
    4 * Math.PI / 6, 5 * Math.PI / 6,
    7 * Math.PI / 6, 8 * Math.PI / 6,
    10 * Math.PI / 6, 11 * Math.PI / 6
  ];
  colAngles.forEach((a) => {
    const col = buildFlutedColumn(H_ROT, 0.38);
    const cx = Math.cos(a) * R_COLS, cz = Math.sin(a) * R_COLS;
    col.position.set(cx, 0, cz); root.add(col);
    addCylCollider(cx, cz, 0.55);
  });

  // Central sculpture pedestal + abstract classical sculpture
  const ped = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 1.3, 1.1, 32), Mat.pedestal);
  ped.position.set(0, 0.55, 0); ped.castShadow = true; ped.receiveShadow = true; root.add(ped);
  addCylCollider(0, 0, 1.28);

  const plinthTop = new THREE.Mesh(new THREE.CylinderGeometry(1.26, 1.26, 0.08, 32), Mat.goldLeaf);
  plinthTop.position.set(0, 1.14, 0); root.add(plinthTop);

  // Modernist alabaster / bronze torsion sculpture atop the pedestal
  const sculpG = new THREE.Group();
  sculpG.position.set(0, 1.18, 0);
  const ring1 = new THREE.Mesh(new THREE.TorusGeometry(0.7, 0.08, 16, 64), Mat.goldLeaf);
  ring1.position.y = 1.0; ring1.rotation.set(0.6, 0.4, 0); ring1.castShadow = true;
  const ring2 = new THREE.Mesh(new THREE.TorusGeometry(0.55, 0.07, 16, 64), Mat.alabaster);
  ring2.position.y = 1.0; ring2.rotation.set(-0.5, 0.9, 0.3); ring2.castShadow = true;
  const coreOrb = new THREE.Mesh(new THREE.SphereGeometry(0.32, 32, 32), Mat.flutedColumn);
  coreOrb.position.y = 1.0; coreOrb.castShadow = true;
  const stem = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.18, 0.7, 16), Mat.pedestal);
  stem.position.y = 0.35; stem.castShadow = true;
  sculpG.add(ring1, ring2, coreOrb, stem); root.add(sculpG);

  // Welcome directory plaque on the south wall (-Z) facing the player entering
  const dirTex = textTexture(1024, 512, (ctx, w, h) => {
    ctx.fillStyle = '#001514'; ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = '#e6af2e'; ctx.lineWidth = 6; ctx.strokeRect(10, 10, w - 20, h - 20);
    ctx.fillStyle = '#e6af2e'; ctx.font = `600 24px ${SANS}`;
    spacedText(ctx, EUNOIA_CONFIG.site.overline.toUpperCase(), w / 2, 54, 4);
    ctx.fillStyle = '#fbfffe'; ctx.font = `600 70px ${SERIF}`;
    spacedText(ctx, EUNOIA_CONFIG.site.title, w / 2, 128, 12);
    ctx.strokeStyle = 'rgba(230,175,46,0.55)'; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(w * 0.18, 154); ctx.lineTo(w * 0.82, 154); ctx.stroke();
    ctx.fillStyle = '#dbe4e2'; ctx.font = `italic 26px ${SERIF}`; ctx.textAlign = 'center';
    ctx.fillText(EUNOIA_CONFIG.site.tagline, w / 2, 196);

    ctx.font = `500 18px ${SANS}`;
    ctx.fillStyle = '#e6af2e'; ctx.fillText('← Wing III · The Nocturne & Astrophotography Gallery (32 Works)', w / 2, 260);
    ctx.fillStyle = '#fbfffe'; ctx.fillText('↑ Wing II · 3D Virtual Worlds & CGI (27 Works) → leads to Wing IV', w / 2, 305);
    ctx.fillStyle = '#e6af2e'; ctx.fillText('Wing I · The Classical & Fine Arts Wing (12 Works) →', w / 2, 350);
    ctx.fillStyle = '#ffc94d'; ctx.fillText('★ Wing IV · The Kinematic Pavilion (2D Animation Video & Storyboards · 25 Works)', w / 2, 395);

    ctx.fillStyle = '#8b9c9a'; ctx.font = `400 16px ${SANS}`;
    ctx.fillText('[WASD] Walk  ·  [LMB] Inspect Art & Watch Video  ·  [TAB] Full 96-Piece Index', w / 2, 460);
  });
  const dirPlaque = new THREE.Mesh(new THREE.PlaneGeometry(3.6, 1.8), new THREE.MeshStandardMaterial({ map: dirTex, roughness: 0.3 }));
  dirPlaque.position.set(0, 2.2, -R_ROT + 0.3);
  root.add(dirPlaque);

  /* --- 2. Build the three connected wings --- */
  function buildWing({ key, label, subtitle, floorMat, wallMat, trimMat, ceilMat, length, rotY, ox, oz }) {
    const wing = new THREE.Group();
    wing.position.set(ox, 0, oz);
    wing.rotation.y = rotY;

    // Floor starts at 0.35 to avoid z-fighting with rotunda floor
    const floorStart = 0.35;
    const floorLen = length - floorStart;
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(WING_W, floorLen), floorMat);
    floor.rotation.x = -Math.PI / 2;
    floor.position.set(0, 0, floorStart + floorLen / 2);
    floor.receiveShadow = true;

    // Wing ceiling at H_WING (5.4m), 1.0m below rotunda ceiling (6.4m)
    const ceil = new THREE.Mesh(new THREE.PlaneGeometry(WING_W, floorLen), ceilMat);
    ceil.rotation.x = Math.PI / 2;
    ceil.position.set(0, H_WING, floorStart + floorLen / 2);

    // Marble threshold plinth capping the transition between rotunda floor and wing floor
    const threshold = new THREE.Mesh(new RoundedBoxGeometry(WING_W + 0.1, 0.024, 0.72, 3, 0.01), Mat.archTrim);
    threshold.position.set(0, 0.012, 0.0);
    threshold.receiveShadow = true;
    wing.add(floor, ceil, threshold);

    // Left wall (-X) & Right wall (+X)
    const wallL = new THREE.Mesh(new THREE.PlaneGeometry(length, H_WING), wallMat);
    wallL.rotation.y = Math.PI / 2; wallL.position.set(-WING_W / 2, H_WING / 2, length / 2);
    wallL.castShadow = true; wallL.receiveShadow = true;
    const wallR = new THREE.Mesh(new THREE.PlaneGeometry(length, H_WING), wallMat);
    wallR.rotation.y = -Math.PI / 2; wallR.position.set(WING_W / 2, H_WING / 2, length / 2);
    wallR.castShadow = true; wallR.receiveShadow = true;
    wing.add(wallL, wallR);

    // End Wall / Portal: Wing II opens into Wing IV; Wing I & III have solid back walls
    if (key === 'II') {
      // Triumphal portal opening into Wing IV (clear opening 3.6m wide, 3.6m high)
      const pW = (WING_W - 3.6) / 2; // 1.7m left and right
      const retEndL = new THREE.Mesh(new THREE.BoxGeometry(pW, H_WING, 0.4), wallMat);
      retEndL.position.set(-WING_W / 2 + pW / 2, H_WING / 2, length);
      const retEndR = new THREE.Mesh(new THREE.BoxGeometry(pW, H_WING, 0.4), wallMat);
      retEndR.position.set(WING_W / 2 - pW / 2, H_WING / 2, length);
      const atticEnd = new THREE.Mesh(new THREE.BoxGeometry(3.6, H_WING - 3.6, 0.4), wallMat);
      atticEnd.position.set(0, 3.6 + (H_WING - 3.6) / 2, length);

      // Portal Header Sign leading into Wing IV
      const toWingIVTex = textTexture(1024, 256, (ctx, w, h) => {
        ctx.fillStyle = '#001514'; ctx.fillRect(0, 0, w, h);
        ctx.strokeStyle = '#e6af2e'; ctx.lineWidth = 5; ctx.strokeRect(10, 10, w - 20, h - 20);
        ctx.fillStyle = '#e6af2e'; ctx.font = `600 22px ${SANS}`;
        spacedText(ctx, 'WING IV · THE KINEMATIC PAVILION', w / 2, 56, 5);
        ctx.fillStyle = '#fbfffe'; ctx.font = `600 44px ${SERIF}`;
        spacedText(ctx, '2D ANIMATION & STORYBOARDS', w / 2, 118, 6);
        ctx.fillStyle = '#dbe4e2'; ctx.font = `italic 22px ${SERIF}`; ctx.textAlign = 'center';
        ctx.fillText('Kinematic Momentum · The Wind Rises · Applied Design', w / 2, 180);
        ctx.fillStyle = '#e6af2e'; ctx.font = `500 15px ${SANS}`;
        ctx.fillText('ENTER PAVILION →', w / 2, 222);
      });
      const toWingIVSign = new THREE.Mesh(new THREE.PlaneGeometry(3.4, 0.75), new THREE.MeshStandardMaterial({ map: toWingIVTex, roughness: 0.35 }));
      toWingIVSign.position.set(0, 3.85, length - 0.22);
      toWingIVSign.rotation.y = Math.PI;

      wing.add(retEndL, retEndR, atticEnd, toWingIVSign);
    } else {
      const wallEnd = new THREE.Mesh(new THREE.PlaneGeometry(WING_W, H_WING), wallMat);
      wallEnd.rotation.y = Math.PI; wallEnd.position.set(0, H_WING / 2, length);
      wallEnd.castShadow = true; wallEnd.receiveShadow = true;
      wing.add(wallEnd);
    }

    // Baseboards & Crown moldings along left & right walls
    const baseMat = trimMat;
    const baseL = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.32, length), baseMat);
    baseL.position.set(-WING_W / 2 + 0.06, 0.16, length / 2);
    const baseR = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.32, length), baseMat);
    baseR.position.set(WING_W / 2 - 0.06, 0.16, length / 2);
    const crownL = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.18, length), Mat.archTrim);
    crownL.position.set(-WING_W / 2 + 0.08, H_WING - 0.09, length / 2);
    const crownR = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.18, length), Mat.archTrim);
    crownR.position.set(WING_W / 2 - 0.08, H_WING - 0.09, length / 2);
    wing.add(baseL, baseR, crownL, crownR);

    if (key !== 'II') {
      const baseEnd = new THREE.Mesh(new THREE.BoxGeometry(WING_W, 0.32, 0.12), baseMat);
      baseEnd.position.set(0, 0.16, length - 0.06);
      const crownEnd = new THREE.Mesh(new THREE.BoxGeometry(WING_W, 0.18, 0.16), Mat.archTrim);
      crownEnd.position.set(0, H_WING - 0.09, length - 0.08);
      wing.add(baseEnd, crownEnd);
    }

    // Entrance portal arch
    const portal = buildWallPortal(key, label, subtitle, wallMat);
    portal.position.set(0, 0, 0); wing.add(portal);

    // End-of-hall accent feature
    if (key === 'I') {
      const consoleTable = new THREE.Mesh(new RoundedBoxGeometry(2.4, 0.9, 0.6, 3, 0.03), Mat.darkWood);
      consoleTable.position.set(0, 0.45, length - 0.4); consoleTable.castShadow = true;
      const urn = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.18, 0.7, 16), Mat.flutedColumn);
      urn.position.set(0, 1.25, length - 0.4); urn.castShadow = true;
      wing.add(consoleTable, urn);
      const ctPos = new THREE.Vector3(0, 0, length - 0.4).applyAxisAngle(V3(0, 1, 0), rotY).add(V3(ox, 0, oz));
      addRotatedBoxCollider(ctPos.x, ctPos.z, 1.35, 0.45, rotY);
    } else if (key === 'II') {
      const track = buildTrackLight(length - 3);
      track.position.set(0, 0, length / 2); wing.add(track);
    } else if (key === 'III') {
      const noctPed = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.45, 1.0, 24), Mat.pedestal);
      noctPed.position.set(0, 0.5, length - 0.8);
      const orb = new THREE.Mesh(new THREE.SphereGeometry(0.28, 24, 24), Mat.goldLeaf);
      orb.position.set(0, 1.28, length - 0.8);
      wing.add(noctPed, orb);
      const npPos = new THREE.Vector3(0, 0, length - 0.8).applyAxisAngle(V3(0, 1, 0), rotY).add(V3(ox, 0, oz));
      addCylCollider(npPos.x, npPos.z, 0.6);
    }

    // Central viewing benches
    const bench1 = buildMuseumBench(key === 'II' ? Mat.pedestal : Mat.darkWood, key === 'I' ? Mat.crimsonVelvet : Mat.blackVelvet);
    bench1.position.set(0, 0, length * 0.4); wing.add(bench1);
    const bench2 = buildMuseumBench(key === 'II' ? Mat.pedestal : Mat.darkWood, key === 'I' ? Mat.crimsonVelvet : Mat.blackVelvet);
    bench2.position.set(0, 0, length * 0.76); wing.add(bench2);

    root.add(wing);

    // Continuous wall segment colliders for Left, Right, and End walls
    const hw = WING_W / 2;
    const pL1 = new THREE.Vector3(-hw, 0, 0).applyAxisAngle(V3(0, 1, 0), rotY).add(V3(ox, 0, oz));
    const pL2 = new THREE.Vector3(-hw, 0, length).applyAxisAngle(V3(0, 1, 0), rotY).add(V3(ox, 0, oz));
    addWallSegment(pL1.x, pL1.z, pL2.x, pL2.z);

    const pR1 = new THREE.Vector3(hw, 0, 0).applyAxisAngle(V3(0, 1, 0), rotY).add(V3(ox, 0, oz));
    const pR2 = new THREE.Vector3(hw, 0, length).applyAxisAngle(V3(0, 1, 0), rotY).add(V3(ox, 0, oz));
    addWallSegment(pR1.x, pR1.z, pR2.x, pR2.z);

    if (key !== 'II') {
      addWallSegment(pL2.x, pL2.z, pR2.x, pR2.z);
    } else {
      // Flanking portal return walls (opening from -1.8 to +1.8)
      const pPortEndL = new THREE.Vector3(-1.8, 0, length).applyAxisAngle(V3(0, 1, 0), rotY).add(V3(ox, 0, oz));
      const pPortEndR = new THREE.Vector3(1.8, 0, length).applyAxisAngle(V3(0, 1, 0), rotY).add(V3(ox, 0, oz));
      addWallSegment(pL2.x, pL2.z, pPortEndL.x, pPortEndL.z);
      addWallSegment(pPortEndR.x, pPortEndR.z, pR2.x, pR2.z);
    }

    // Entrance portal return wall colliders (flanking the doorway)
    const pPortL = new THREE.Vector3(-1.50, 0, 0).applyAxisAngle(V3(0, 1, 0), rotY).add(V3(ox, 0, oz));
    const pPortR = new THREE.Vector3(1.50, 0, 0).applyAxisAngle(V3(0, 1, 0), rotY).add(V3(ox, 0, oz));
    addWallSegment(pL1.x, pL1.z, pPortL.x, pPortL.z);
    addWallSegment(pPortR.x, pPortR.z, pR1.x, pR1.z);

    // Bench oriented box colliders (seatL=3.4, seatW=0.95 -> halfL=1.75, halfW=0.55)
    const b1Pos = new THREE.Vector3(0, 0, length * 0.4).applyAxisAngle(V3(0, 1, 0), rotY).add(V3(ox, 0, oz));
    addRotatedBoxCollider(b1Pos.x, b1Pos.z, 1.75, 0.55, rotY);
    const b2Pos = new THREE.Vector3(0, 0, length * 0.76).applyAxisAngle(V3(0, 1, 0), rotY).add(V3(ox, 0, oz));
    addRotatedBoxCollider(b2Pos.x, b2Pos.z, 1.75, 0.55, rotY);

    return wing;
  }

  // Wing I (East, along +X axis)
  buildWing({
    key: 'I',
    label: EUNOIA_CONFIG.wings.I.name,
    subtitle: EUNOIA_CONFIG.wings.I.blurb,
    floorMat: Mat.floorWingI, wallMat: Mat.wallWingI, trimMat: Mat.trimWingI, ceilMat: Mat.ceilingWingI,
    length: WING_L, rotY: Math.PI / 2, ox: R_ROT - 0.2, oz: 0
  });

  // Wing II (North, along +Z axis)
  buildWing({
    key: 'II',
    label: EUNOIA_CONFIG.wings.II.name,
    subtitle: EUNOIA_CONFIG.wings.II.blurb,
    floorMat: Mat.floorWingII, wallMat: Mat.wallWingII, trimMat: Mat.trimWingII, ceilMat: Mat.ceilingWingII,
    length: WING_L, rotY: 0, ox: 0, oz: R_ROT - 0.2
  });

  // Wing III (West, along -X axis)
  buildWing({
    key: 'III',
    label: EUNOIA_CONFIG.wings.III.name,
    subtitle: EUNOIA_CONFIG.wings.III.blurb,
    floorMat: Mat.floorWingIII, wallMat: Mat.wallWingIII, trimMat: Mat.trimWingIII, ceilMat: Mat.ceilingWingIII,
    length: WING_L, rotY: -Math.PI / 2, ox: -(R_ROT - 0.2), oz: 0
  });

  /* --- 3. Wing IV: The Kinematic Pavilion (Grand Transverse Hall) --- */
  function buildWingIV() {
    const pav = new THREE.Group();
    const pavW = 22.0, pavD = 11.0, pavH = 5.6;
    const startZ = (R_ROT - 0.2) + WING_L; // 8.3 + 26.0 = 34.3m
    pav.position.set(0, 0, startZ);

    // Floor (Warm Brown Herringbone Parquet)
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(pavW, pavD), Mat.floorWingI);
    floor.rotation.x = -Math.PI / 2; floor.position.set(0, 0, pavD / 2);
    floor.receiveShadow = true; pav.add(floor);

    // Ceiling (Coffered White with Xanthous rosettes)
    const ceil = new THREE.Mesh(new THREE.PlaneGeometry(pavW, pavD), Mat.ceilingWingI);
    ceil.rotation.x = Math.PI / 2; ceil.position.set(0, pavH, pavD / 2);
    pav.add(ceil);

    // North Wall (Back wall facing visitor entering from Wing II)
    const wallN = new THREE.Mesh(new THREE.PlaneGeometry(pavW, pavH), Mat.wallWingII);
    wallN.rotation.y = Math.PI; wallN.position.set(0, pavH / 2, pavD);
    wallN.receiveShadow = true; pav.add(wallN);

    // West Wall (-X) & East Wall (+X)
    const wallW = new THREE.Mesh(new THREE.PlaneGeometry(pavD, pavH), Mat.wallWingII);
    wallW.rotation.y = Math.PI / 2; wallW.position.set(-pavW / 2, pavH / 2, pavD / 2);
    wallW.receiveShadow = true; pav.add(wallW);

    const wallE = new THREE.Mesh(new THREE.PlaneGeometry(pavD, pavH), Mat.wallWingII);
    wallE.rotation.y = -Math.PI / 2; wallE.position.set(pavW / 2, pavH / 2, pavD / 2);
    wallE.receiveShadow = true; pav.add(wallE);

    // South Wall (Flanking the entrance portal from Wing II)
    const southSectW = (pavW - 3.6) / 2; // 9.2m left and right
    const wallSL = new THREE.Mesh(new THREE.PlaneGeometry(southSectW, pavH), Mat.wallWingII);
    wallSL.position.set(-pavW / 2 + southSectW / 2, pavH / 2, 0);
    const wallSR = new THREE.Mesh(new THREE.PlaneGeometry(southSectW, pavH), Mat.wallWingII);
    wallSR.position.set(pavW / 2 - southSectW / 2, pavH / 2, 0);
    const wallSTop = new THREE.Mesh(new THREE.PlaneGeometry(3.6, pavH - 3.6), Mat.wallWingII);
    wallSTop.position.set(0, 3.6 + (pavH - 3.6) / 2, 0);
    pav.add(wallSL, wallSR, wallSTop);

    // Return Sign facing inside Wing IV looking back towards Wing II & Rotunda
    const retSignTex = textTexture(1024, 256, (ctx, w, h) => {
      ctx.fillStyle = '#001514'; ctx.fillRect(0, 0, w, h);
      ctx.strokeStyle = '#e6af2e'; ctx.lineWidth = 5; ctx.strokeRect(10, 10, w - 20, h - 20);
      ctx.fillStyle = '#e6af2e'; ctx.font = `600 22px ${SANS}`;
      spacedText(ctx, 'TO WING II · 3D VIRTUAL WORLDS', w / 2, 56, 5);
      ctx.fillStyle = '#fbfffe'; ctx.font = `600 44px ${SERIF}`;
      spacedText(ctx, '← GRAND ROTUNDA & GALLERIES', w / 2, 118, 6);
      ctx.fillStyle = '#dbe4e2'; ctx.font = `italic 22px ${SERIF}`; ctx.textAlign = 'center';
      ctx.fillText('Spatial Architecture · Character Topology · Sculpture Court', w / 2, 180);
      ctx.fillStyle = '#e6af2e'; ctx.font = `500 15px ${SANS}`;
      ctx.fillText('MAIN GALLERY ACCESS', w / 2, 222);
    });
    const retSign = new THREE.Mesh(new THREE.PlaneGeometry(3.4, 0.75), new THREE.MeshStandardMaterial({ map: retSignTex, roughness: 0.35 }));
    retSign.position.set(0, 3.85, 0.22);
    pav.add(retSign);

    // Architectural Trim & Baseboards
    const baseMat = Mat.trimWingII;
    const bN = new THREE.Mesh(new THREE.BoxGeometry(pavW, 0.32, 0.12), baseMat);
    bN.position.set(0, 0.16, pavD - 0.06);
    const bW = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.32, pavD), baseMat);
    bW.position.set(-pavW / 2 + 0.06, 0.16, pavD / 2);
    const bE = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.32, pavD), baseMat);
    bE.position.set(pavW / 2 - 0.06, 0.16, pavD / 2);
    pav.add(bN, bW, bE);

    // Central Viewing Bench facing the 2D Animation Video Canvas
    const benchPav = buildMuseumBench(Mat.darkWood, Mat.crimsonVelvet);
    benchPav.position.set(0, 0, 5.5);
    pav.add(benchPav);
    addRotatedBoxCollider(0, startZ + 5.5, 1.75, 0.55, 0);

    // Overhead chandelier / track light fixtures
    const track1 = buildTrackLight(18);
    track1.position.set(0, 0, 3.0);
    const track2 = buildTrackLight(18);
    track2.position.set(0, 0, 8.0);
    pav.add(track1, track2);

    // Perimeter colliders for Wing IV
    addWallSegment(-pavW / 2, startZ + pavD, pavW / 2, startZ + pavD); // North wall
    addWallSegment(-pavW / 2, startZ, -pavW / 2, startZ + pavD);        // West wall
    addWallSegment(pavW / 2, startZ, pavW / 2, startZ + pavD);         // East wall
    addWallSegment(-pavW / 2, startZ, -1.8, startZ);                   // South wall left
    addWallSegment(1.8, startZ, pavW / 2, startZ);                    // South wall right

    root.add(pav);
  }

  buildWingIV();

  scene.add(root);
}

/* --------------------------------------------------------------------------
   4.10  FRAMES, EXHIBIT HANGING & INTERACTIVE OBJECTS
   -------------------------------------------------------------------------- */
const exhibitMeshes = [];      // For raycasting
const exhibitDataMap = new Map(); // Mesh UUID -> Exhibit Data & Teleport target

function buildPictureFrame(exhibit, width, height) {
  const group = new THREE.Group();

  // Aspect ratio based dimensions
  const isLandscape = exhibit.orientation === 'landscape';
  const artW = isLandscape ? 3.0 : 2.2;
  const artH = isLandscape ? 2.25 : 2.93;
  const frameBorder = 0.22;
  const frameDepth = 0.14;

  // Frame outer border
  const outerW = artW + frameBorder * 2;
  const outerH = artH + frameBorder * 2;

  let frameMat = Mat.goldLeaf;
  if (exhibit.wing === 'II') frameMat = Mat.darkWood;
  if (exhibit.wing === 'III') frameMat = Mat.pedestal;

  const frameBack = new THREE.Mesh(
    new RoundedBoxGeometry(outerW, outerH, frameDepth, 4, 0.03),
    frameMat
  );
  frameBack.castShadow = true;
  frameBack.receiveShadow = true;
  group.add(frameBack);

  // Inner beveled liner / slip
  const linerMat = exhibit.wing === 'II' ? Mat.goldLeaf : Mat.alabaster;
  const liner = new THREE.Mesh(
    new RoundedBoxGeometry(artW + 0.08, artH + 0.08, frameDepth + 0.02, 3, 0.01),
    linerMat
  );
  group.add(liner);

  // Artwork Canvas texture & fallback
  let artMat;
  if (exhibit.mediaType === 'video') {
    const video = document.createElement('video');
    video.src = exhibit.imagePath;
    video.crossOrigin = 'anonymous';
    video.loop = true;
    video.muted = true;
    video.playsInline = true;
    video.autoplay = true;
    video.setAttribute('webkit-playsinline', 'true');
    video.play().catch(() => {});

    const videoTex = new THREE.VideoTexture(video);
    videoTex.colorSpace = THREE.SRGBColorSpace;
    videoTex.minFilter = THREE.LinearFilter;
    videoTex.magFilter = THREE.LinearFilter;

    // Glowing video canvas surface
    artMat = new THREE.MeshBasicMaterial({ map: videoTex });
  } else {
    const fallbackCanvas = paintArtwork('gallery', exhibit.orientation, hashString(exhibit.id));
    const fallbackTex = new THREE.CanvasTexture(fallbackCanvas);
    fallbackTex.colorSpace = THREE.SRGBColorSpace;
    fallbackTex.anisotropy = MAX_ANISO;
    artMat = new THREE.MeshStandardMaterial({
      map: fallbackTex,
      roughness: 0.45,
      metalness: 0.05
    });

    if (exhibit.imagePath) {
      loadTracker.total++;
      texLoader.load(
        exhibit.imagePath,
        (loadedTex) => {
          loadedTex.colorSpace = THREE.SRGBColorSpace;
          loadedTex.anisotropy = MAX_ANISO;
          artMat.map = loadedTex;
          artMat.needsUpdate = true;
          fallbackTex.dispose();
          loadTracker.done++;
          loadTracker.ok++;
          updateLoadStatus();
        },
        undefined,
        (err) => {
          console.warn('Failed to load artwork image:', exhibit.imagePath, err);
          loadTracker.done++;
          updateLoadStatus();
        }
      );
    }
  }

  const artCanvasMesh = new THREE.Mesh(
    new THREE.PlaneGeometry(artW, artH),
    artMat
  );
  artCanvasMesh.position.z = frameDepth / 2 + 0.015;
  artCanvasMesh.castShadow = false;
  artCanvasMesh.receiveShadow = true;
  group.add(artCanvasMesh);

  // Attach data to interactive mesh
  artCanvasMesh.userData = { exhibit, group };
  exhibitMeshes.push(artCanvasMesh);
  exhibitDataMap.set(artCanvasMesh.uuid, exhibit);

  // Museum Wall Plaque beneath painting
  const plaqueTex = textTexture(512, 192, (ctx, w, h) => {
    ctx.fillStyle = '#001514';
    ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = '#e6af2e';
    ctx.lineWidth = 4;
    ctx.strokeRect(6, 6, w - 12, h - 12);
    ctx.fillStyle = '#e6af2e';
    ctx.font = `600 22px ${SANS}`;
    ctx.textAlign = 'center';
    ctx.fillText(`${exhibit.category.toUpperCase()} · ${exhibit.year}`, w / 2, 42);
    ctx.fillStyle = '#fbfffe';
    ctx.font = `600 32px ${SERIF}`;
    wrapText(ctx, exhibit.title, w / 2, 88, w - 40, 36);
    ctx.fillStyle = '#dbe4e2';
    ctx.font = `italic 20px ${SERIF}`;
    ctx.fillText(exhibit.subtitle || '', w / 2, 154);
  });

  const plaqueMesh = new THREE.Mesh(
    new THREE.PlaneGeometry(0.7, 0.28),
    new THREE.MeshStandardMaterial({ map: plaqueTex, roughness: 0.35 })
  );
  plaqueMesh.position.set(0, -artH / 2 - 0.34, frameDepth / 2);
  group.add(plaqueMesh);

  // Dedicated warm spotlight pointing at artwork
  const spot = new THREE.SpotLight(0xffe4a0, 55, 9, Math.PI / 5, 0.55, 1.2);
  spot.position.set(0, artH / 2 + 1.2, 2.2);
  spot.target = artCanvasMesh;
  spot.castShadow = false;
  group.add(spot);
  group.add(spot.target);

  // Small brass light fixture geometry above frame
  const fixtureBar = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 0.6, 8), Mat.bronze);
  fixtureBar.rotation.z = Math.PI / 2;
  fixtureBar.position.set(0, artH / 2 + 0.32, 0.35);
  const fixtureHood = new THREE.Mesh(new RoundedBoxGeometry(0.7, 0.06, 0.12, 3, 0.01), Mat.bronze);
  fixtureHood.position.set(0, artH / 2 + 0.35, 0.35);
  const stemL = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.01, 0.35, 8), Mat.bronze);
  stemL.rotation.x = Math.PI / 3; stemL.position.set(-0.25, artH / 2 + 0.18, 0.18);
  const stemR = stemL.clone(); stemR.position.x = 0.25;
  group.add(fixtureBar, fixtureHood, stemL, stemR);

  return { group, artCanvasMesh, artW, artH };
}

function layoutExhibits() {
  const wingExhibits = { I: [], II: [], III: [], IV: [] };
  EUNOIA_CONFIG.exhibits.forEach((ex) => {
    if (ex.isHung && wingExhibits[ex.wing]) {
      wingExhibits[ex.wing].push(ex);
    }
  });

  const wingConfigs = {
    I:   { rotY: Math.PI / 2,  ox: R_ROT - 0.2, oz: 0 },
    II:  { rotY: 0,            ox: 0,           oz: R_ROT - 0.2 },
    III: { rotY: -Math.PI / 2, ox: -(R_ROT - 0.2), oz: 0 },
    IV:  { rotY: 0,            ox: 0,           oz: (R_ROT - 0.2) + WING_L }
  };

  // Layout Wings I, II, III (Linear galleries)
  ['I', 'II', 'III'].forEach((wingKey) => {
    const cfg = wingConfigs[wingKey];
    const list = wingExhibits[wingKey] || [];

    list.forEach((ex, idx) => {
      const { group, artCanvasMesh } = buildPictureFrame(ex);
      const side = idx % 2 === 0 ? -1 : 1; // -1: left wall, 1: right wall
      const wallOffset = (WING_W / 2) - 0.14;
      const xLocal = side * wallOffset;
      const zLocal = 4.2 + Math.floor(idx / 2) * 5.6; // Spaced 5.6m apart along 26m hall
      const yLocal = 2.4;

      group.position.set(xLocal, yLocal, zLocal);
      group.rotation.y = side === -1 ? Math.PI / 2 : -Math.PI / 2;

      const worldGroup = new THREE.Group();
      worldGroup.position.set(cfg.ox, 0, cfg.oz);
      worldGroup.rotation.y = cfg.rotY;
      worldGroup.add(group);
      scene.add(worldGroup);

      const localViewPos = new THREE.Vector3(side * (wallOffset - 2.6), EYE_HEIGHT, zLocal);
      const worldViewPos = localViewPos.clone().applyAxisAngle(V3(0, 1, 0), cfg.rotY).add(V3(cfg.ox, 0, cfg.oz));
      const localArtPos = new THREE.Vector3(xLocal, yLocal, zLocal);
      const worldArtPos = localArtPos.clone().applyAxisAngle(V3(0, 1, 0), cfg.rotY).add(V3(cfg.ox, 0, cfg.oz));

      ex.teleportPos = worldViewPos;
      ex.lookTarget = worldArtPos;
    });
  });

  // Layout Wing IV: The Kinematic Pavilion (Grand Transverse Hall)
  const pavCfg = wingConfigs.IV;
  const listIV = wingExhibits.IV || [];
  const pavW = 22.0, pavD = 11.0;

  listIV.forEach((ex, idx) => {
    const { group, artCanvasMesh } = buildPictureFrame(ex);
    let xLocal = 0, yLocal = 2.5, zLocal = 0, rotYLocal = 0;
    let localViewPos = new THREE.Vector3();

    if (idx === 0) {
      // CENTERPIECE: 2D Animation Video Canvas on North Wall
      xLocal = 0; yLocal = 2.8; zLocal = pavD - 0.16; rotYLocal = Math.PI;
      localViewPos.set(0, EYE_HEIGHT, pavD - 3.8);
    } else if (idx === 1) {
      // The Wind Rises Storyboard Sheet 3 (North Wall Left)
      xLocal = -5.8; yLocal = 2.6; zLocal = pavD - 0.16; rotYLocal = Math.PI;
      localViewPos.set(-5.8, EYE_HEIGHT, pavD - 3.0);
    } else if (idx === 2) {
      // The Wind Rises Storyboard Sheet 4 (North Wall Right)
      xLocal = 5.8; yLocal = 2.6; zLocal = pavD - 0.16; rotYLocal = Math.PI;
      localViewPos.set(5.8, EYE_HEIGHT, pavD - 3.0);
    } else if (idx === 3) {
      // Cinematography Plate 2 (West Wall)
      xLocal = -pavW / 2 + 0.16; yLocal = 2.4; zLocal = 3.6; rotYLocal = Math.PI / 2;
      localViewPos.set(-pavW / 2 + 2.8, EYE_HEIGHT, 3.6);
    } else if (idx === 4) {
      // Continuity Board 4 (West Wall)
      xLocal = -pavW / 2 + 0.16; yLocal = 2.4; zLocal = 8.0; rotYLocal = Math.PI / 2;
      localViewPos.set(-pavW / 2 + 2.8, EYE_HEIGHT, 8.0);
    } else if (idx === 5) {
      // Paneling 3 (East Wall)
      xLocal = pavW / 2 - 0.16; yLocal = 2.4; zLocal = 3.6; rotYLocal = -Math.PI / 2;
      localViewPos.set(pavW / 2 - 2.8, EYE_HEIGHT, 3.6);
    } else if (idx === 6) {
      // Atelier Jacquard Lanyard Edition (East Wall)
      xLocal = pavW / 2 - 0.16; yLocal = 2.4; zLocal = 8.0; rotYLocal = -Math.PI / 2;
      localViewPos.set(pavW / 2 - 2.8, EYE_HEIGHT, 8.0);
    } else if (idx === 7) {
      // Chess Que Poster (South Wall Left of Entrance)
      xLocal = -5.5; yLocal = 2.4; zLocal = 0.16; rotYLocal = 0;
      localViewPos.set(-5.5, EYE_HEIGHT, 2.8);
    }

    group.position.set(xLocal, yLocal, zLocal);
    group.rotation.y = rotYLocal;

    const worldGroup = new THREE.Group();
    worldGroup.position.set(pavCfg.ox, 0, pavCfg.oz);
    worldGroup.rotation.y = pavCfg.rotY;
    worldGroup.add(group);
    scene.add(worldGroup);

    const worldViewPos = localViewPos.clone().applyAxisAngle(V3(0, 1, 0), pavCfg.rotY).add(V3(pavCfg.ox, 0, pavCfg.oz));
    const localArtPos = new THREE.Vector3(xLocal, yLocal, zLocal);
    const worldArtPos = localArtPos.clone().applyAxisAngle(V3(0, 1, 0), pavCfg.rotY).add(V3(pavCfg.ox, 0, pavCfg.oz));

    ex.teleportPos = worldViewPos;
    ex.lookTarget = worldArtPos;
  });
}

/* --------------------------------------------------------------------------
   4.11  LIGHTING PIPELINE
   -------------------------------------------------------------------------- */
function buildLighting() {
  // Low ambient baseline with subtle warm/cool gradation - moody and gloomy gallery atmosphere
  const hemi = new THREE.HemisphereLight(0xdcd0bc, 0x000808, 0.12);
  scene.add(hemi);

  const amb = new THREE.AmbientLight(0xfbf2e4, 0.05);
  scene.add(amb);

  // Grand Rotunda central skylight chandelier illumination - soft moody beam
  const rotundaSun = new THREE.SpotLight(0xffeaad, 42, 22, Math.PI / 3.2, 0.65, 1.2);
  rotundaSun.position.set(0, H_ROT + 1.2, 0);
  rotundaSun.target.position.set(0, 0, 0);
  rotundaSun.castShadow = true;
  rotundaSun.shadow.mapSize.width = 1024;
  rotundaSun.shadow.mapSize.height = 1024;
  rotundaSun.shadow.bias = -0.0004;
  scene.add(rotundaSun);
  scene.add(rotundaSun.target);

  // Rotunda subtle warm perimeter accent lights
  for (let i = 0; i < 4; i++) {
    const a = (i / 4) * TAU + Math.PI / 4;
    const pl = new THREE.PointLight(0xffd599, 2.8, 8, 1.4);
    pl.position.set(Math.cos(a) * 5.2, 4.2, Math.sin(a) * 5.2);
    scene.add(pl);
  }

  // Hallway ambient fills across all four wings - soft and atmospheric
  const wings = [
    { rotY: Math.PI / 2,  ox: R_ROT - 0.2, oz: 0, color: 0xffd8b0, intensity: 3.8 }, // Wing I (Blood Red & Warm Gold)
    { rotY: 0,            ox: 0,           oz: R_ROT - 0.2, color: 0xf5f0e6, intensity: 4.2 }, // Wing II (White Alabaster)
    { rotY: -Math.PI / 2, ox: -(R_ROT - 0.2), oz: 0, color: 0x90a8d4, intensity: 2.2 }  // Wing III (Nocturne Slate)
  ];

  wings.forEach(({ rotY, ox, oz, color, intensity }) => {
    [6, 13, 20].forEach((dist) => {
      const pos = new THREE.Vector3(0, 4.5, dist).applyAxisAngle(V3(0, 1, 0), rotY).add(V3(ox, 0, oz));
      const light = new THREE.PointLight(color, intensity, 12, 1.5);
      light.position.copy(pos);
      scene.add(light);
    });
  });

  // Wing IV (The Kinematic Pavilion) dedicated cinema ambient lights
  const pavStartZ = (R_ROT - 0.2) + WING_L; // 34.3m
  [
    { x: -5.5, z: pavStartZ + 4.5, color: 0xffe4a0, int: 4.5 },
    { x:  5.5, z: pavStartZ + 4.5, color: 0xffe4a0, int: 4.5 },
    { x: -5.5, z: pavStartZ + 8.5, color: 0xffd8b0, int: 4.0 },
    { x:  5.5, z: pavStartZ + 8.5, color: 0xffd8b0, int: 4.0 }
  ].forEach(p => {
    const pl = new THREE.PointLight(p.color, p.int, 14, 1.4);
    pl.position.set(p.x, 4.8, p.z);
    scene.add(pl);
  });
}

/* --------------------------------------------------------------------------
   4.12  PROCEDURAL WEB AUDIO (Footsteps + Gallery Ambience)
   -------------------------------------------------------------------------- */
let audioCtx = null;
let isMuted = false;
let ambienceGain = null;
let footstepGain = null;

function initAudio() {
  if (audioCtx) return;
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    audioCtx = new AudioContext();

    // Master ambience
    const ambOsc1 = audioCtx.createOscillator();
    const ambOsc2 = audioCtx.createOscillator();
    ambOsc1.type = 'sine'; ambOsc1.frequency.setValueAtTime(54, audioCtx.currentTime);
    ambOsc2.type = 'triangle'; ambOsc2.frequency.setValueAtTime(108, audioCtx.currentTime);

    const filter = audioCtx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(260, audioCtx.currentTime);

    ambienceGain = audioCtx.createGain();
    ambienceGain.gain.setValueAtTime(0.035, audioCtx.currentTime);

    ambOsc1.connect(filter);
    ambOsc2.connect(filter);
    filter.connect(ambienceGain);
    ambienceGain.connect(audioCtx.destination);

    ambOsc1.start();
    ambOsc2.start();

    // Footstep sub-chain
    footstepGain = audioCtx.createGain();
    footstepGain.gain.setValueAtTime(0.08, audioCtx.currentTime);
    footstepGain.connect(audioCtx.destination);
  } catch (e) {
    console.warn('Web Audio not supported or blocked:', e);
  }
}

function playFootstep() {
  if (!audioCtx || isMuted || audioCtx.state !== 'running') return;
  try {
    const t = audioCtx.currentTime;
    const osc = audioCtx.createOscillator();
    const g = audioCtx.createGain();
    const filter = audioCtx.createBiquadFilter();

    osc.type = 'sine';
    osc.frequency.setValueAtTime(80, t);
    osc.frequency.exponentialRampToValueAtTime(32, t + 0.09);

    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(160, t);

    g.gain.setValueAtTime(0.08, t);
    g.gain.exponentialRampToValueAtTime(0.0001, t + 0.09);

    osc.connect(filter);
    filter.connect(g);
    g.connect(footstepGain);

    osc.start(t);
    osc.stop(t + 0.095);
  } catch (_) {}
}

function toggleSound() {
  isMuted = !isMuted;
  if (audioCtx) {
    if (isMuted) {
      if (ambienceGain) ambienceGain.gain.setTargetAtTime(0, audioCtx.currentTime, 0.05);
      if (footstepGain) footstepGain.gain.setTargetAtTime(0, audioCtx.currentTime, 0.05);
    } else {
      if (audioCtx.state === 'suspended') audioCtx.resume();
      if (ambienceGain) ambienceGain.gain.setTargetAtTime(0.035, audioCtx.currentTime, 0.05);
      if (footstepGain) footstepGain.gain.setTargetAtTime(0.08, audioCtx.currentTime, 0.05);
    }
  }
  $('icoSoundOn').classList.toggle('hidden', isMuted);
  $('icoSoundOff').classList.toggle('hidden', !isMuted);
  $('btnSound').setAttribute('aria-pressed', (!isMuted).toString());
}
$('btnSound').addEventListener('click', toggleSound);

/* --------------------------------------------------------------------------
   4.13  FIRST-PERSON CONTROLLER & INPUT HANDLING
   -------------------------------------------------------------------------- */
const controls = new PointerLockControls(camera, renderer.domElement);
let isControlsLocked = false;
let isInspecting = false;
let isLobbyActive = true;
let isCatalogOpen = false;

// Movement state
const moveState = { forward: false, backward: false, left: false, right: false, sprint: false };
const velocity = new THREE.Vector3();
const direction = new THREE.Vector3();
let bobTimer = 0;
let lastFootstepBob = 0;

// Camera inspection interpolation
let inspectLerp = null; // { startPos, endPos, startQuat, endQuat, t, duration, onComplete }

controls.addEventListener('lock', () => {
  isControlsLocked = true;
  $('resume').classList.add('hidden');
});
controls.addEventListener('unlock', () => {
  isControlsLocked = false;
  if (!isLobbyActive && !isInspecting && !isCatalogOpen) {
    $('resume').classList.remove('hidden');
  }
});

// Resume overlay click
$('resume').addEventListener('click', () => {
  initAudio();
  if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume();
  try { controls.lock(); } catch (e) {}
});

// Keyboard events
window.addEventListener('keydown', (e) => {
  if (e.code === 'KeyW' || e.code === 'ArrowUp') moveState.forward = true;
  if (e.code === 'KeyS' || e.code === 'ArrowDown') moveState.backward = true;
  if (e.code === 'KeyA' || e.code === 'ArrowLeft') moveState.left = true;
  if (e.code === 'KeyD' || e.code === 'ArrowRight') moveState.right = true;
  if (e.code === 'ShiftLeft' || e.code === 'ShiftRight') moveState.sprint = true;

  if (e.code === 'Tab') {
    e.preventDefault();
    toggleCatalog();
  }
  if (e.code === 'KeyM') {
    toggleSound();
  }
  if (e.code === 'Escape') {
    if (isCatalogOpen) {
      toggleCatalog(false);
    } else if (isInspecting) {
      exitInspection();
    } else if (!isLobbyActive) {
      openLobby();
    }
  }
});

window.addEventListener('keyup', (e) => {
  if (e.code === 'KeyW' || e.code === 'ArrowUp') moveState.forward = false;
  if (e.code === 'KeyS' || e.code === 'ArrowDown') moveState.backward = false;
  if (e.code === 'KeyA' || e.code === 'ArrowLeft') moveState.left = false;
  if (e.code === 'KeyD' || e.code === 'ArrowRight') moveState.right = false;
  if (e.code === 'ShiftLeft' || e.code === 'ShiftRight') moveState.sprint = false;
});

/* --------------------------------------------------------------------------
   4.14  RAYCASTING & INSPECTION MODE
   -------------------------------------------------------------------------- */
const raycaster = new THREE.Raycaster();
const screenCenter = new THREE.Vector2(0, 0);
let hoveredExhibitMesh = null;

function updateRaycast() {
  if (!isControlsLocked || isInspecting || isCatalogOpen) {
    $('reticle').classList.remove('active');
    $('prompt').classList.remove('show');
    hoveredExhibitMesh = null;
    return;
  }

  raycaster.setFromCamera(screenCenter, camera);
  raycaster.far = 6.5;
  const intersects = raycaster.intersectObjects(exhibitMeshes, false);

  if (intersects.length > 0) {
    const hit = intersects[0].object;
    hoveredExhibitMesh = hit;
    const exhibit = hit.userData.exhibit;
    $('reticle').classList.add('active');
    $('prompt').classList.add('show');
    $('promptTitle').textContent = exhibit.title;
  } else {
    $('reticle').classList.remove('active');
    $('prompt').classList.remove('show');
    hoveredExhibitMesh = null;
  }
}

// Click to inspect
window.addEventListener('mousedown', (e) => {
  if (e.button === 0 && isControlsLocked && hoveredExhibitMesh && !isInspecting) {
    inspectExhibit(hoveredExhibitMesh.userData.exhibit, hoveredExhibitMesh);
  }
});

function inspectExhibit(exhibit, mesh) {
  isInspecting = true;
  document.body.classList.add('is-inspecting');
  controls.unlock();

  // Populate Curator Plaque UI
  const plqImg = $('plqImg');
  const plqVid = $('plqVideo');

  if (exhibit.mediaType === 'video') {
    plqImg.classList.add('hidden');
    plqVid.classList.remove('hidden');
    plqVid.src = exhibit.imagePath;
    plqVid.play().catch(() => {});
  } else {
    plqVid.classList.add('hidden');
    plqVid.pause();
    plqImg.classList.remove('hidden');
    plqImg.src = exhibit.imagePath;
    plqImg.alt = exhibit.title;
  }
  $('plqNo').textContent = `Exhibit ${exhibit.id}`;
  $('plqWing').textContent = EUNOIA_CONFIG.wings[exhibit.wing]?.name || `Wing ${exhibit.wing}`;
  $('plqWing').className = 'badge wing-' + exhibit.wing;
  $('plqTitle').textContent = exhibit.title;
  $('plqSubtitle').textContent = exhibit.subtitle || '';
  $('plqYear').textContent = exhibit.year;
  $('plqCategory').textContent = exhibit.category;

  const tagsContainer = $('plqTags');
  tagsContainer.innerHTML = '';
  (exhibit.tags || []).forEach((t) => {
    const tag = document.createElement('span');
    tag.className = 'tag';
    tag.textContent = t;
    tagsContainer.appendChild(tag);
  });

  $('plqDesc').textContent = exhibit.description;

  const linksContainer = $('plqLinks');
  linksContainer.innerHTML = '';
  (exhibit.links || []).forEach((l) => {
    const a = document.createElement('a');
    a.className = 'btn btn-ghost btn-small';
    a.href = l.url;
    a.target = '_blank';
    a.rel = 'noopener noreferrer';
    a.textContent = l.label;
    linksContainer.appendChild(a);
  });

  $('plaque').classList.add('open');
  $('plaque').setAttribute('aria-hidden', 'false');

  // Smooth lerp camera to framed inspect target
  const startPos = camera.position.clone();
  const startQuat = camera.quaternion.clone();

  const targetPos = getExhibitTeleportPos(exhibit).clone();
  const lookTarget = getExhibitLookTarget(exhibit);
  const tempCam = camera.clone();
  tempCam.position.copy(targetPos);
  tempCam.lookAt(lookTarget);
  const targetQuat = tempCam.quaternion.clone();

  inspectLerp = {
    startPos, endPos: targetPos,
    startQuat, endQuat: targetQuat,
    t: 0, duration: 1.1,
    onComplete: null
  };
}

function exitInspection() {
  if (!isInspecting) return;
  isInspecting = false;
  inspectLerp = null;
  document.body.classList.remove('is-inspecting');
  $('plaque').classList.remove('open');
  $('plaque').setAttribute('aria-hidden', 'true');

  const plqVid = $('plqVideo');
  if (plqVid) plqVid.pause();

  initAudio();
  if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume();
  camera.rotation.setFromQuaternion(camera.quaternion, 'YXZ');
  try { controls.lock(); } catch (e) {}
  updateCurrentWingCaption(camera.position);
}
$('plqClose').addEventListener('click', exitInspection);

/* --------------------------------------------------------------------------
   4.15  TELEPORT & QUICK EXHIBITION INDEX (Catalog)
   -------------------------------------------------------------------------- */
function getExhibitTeleportPos(exhibit) {
  if (exhibit.teleportPos) return exhibit.teleportPos;
  const hungInWing = EUNOIA_CONFIG.exhibits.find(e => e.wing === exhibit.wing && e.teleportPos);
  if (hungInWing) return hungInWing.teleportPos;
  return new THREE.Vector3(0, EYE_HEIGHT, -4.5);
}

function getExhibitLookTarget(exhibit) {
  if (exhibit.lookTarget) return exhibit.lookTarget;
  const hungInWing = EUNOIA_CONFIG.exhibits.find(e => e.wing === exhibit.wing && e.lookTarget);
  if (hungInWing) return hungInWing.lookTarget;
  return new THREE.Vector3(0, EYE_HEIGHT, 0);
}

function teleportToExhibit(exhibitOrId) {
  const exhibit = typeof exhibitOrId === 'string'
    ? EUNOIA_CONFIG.exhibits.find(e => e.id === exhibitOrId)
    : exhibitOrId;
  if (!exhibit) return;
  inspectLerp = null;
  const fade = $('fade');
  fade.classList.add('on');

  const targetPos = getExhibitTeleportPos(exhibit);
  const targetLook = getExhibitLookTarget(exhibit);

  setTimeout(() => {
    camera.position.copy(targetPos);
    camera.lookAt(targetLook);
    camera.rotation.setFromQuaternion(camera.quaternion, 'YXZ');

    if (controls.object) controls.object.position.copy(targetPos);
    updateCurrentWingCaption(targetPos);

    setTimeout(() => {
      fade.classList.remove('on');
      if (isCatalogOpen) toggleCatalog(false);
      inspectExhibit(exhibit);
    }, 150);
  }, 320);
}

function toggleCatalog(force) {
  isCatalogOpen = force !== undefined ? force : !isCatalogOpen;
  $('catalog').classList.toggle('open', isCatalogOpen);
  $('catalog').setAttribute('aria-hidden', (!isCatalogOpen).toString());

  if (isCatalogOpen) {
    if (isControlsLocked) controls.unlock();
  } else {
    if (!isLobbyActive && !isInspecting) {
      try { controls.lock(); } catch (e) {}
    }
  }
}
$('btnIndex').addEventListener('click', () => toggleCatalog(true));
$('catClose').addEventListener('click', () => toggleCatalog(false));

// Populate 2D Catalog
function initCatalog() {
  const filtersNav = $('catFilters');
  const grid = $('catGrid');
  filtersNav.innerHTML = '';
  grid.innerHTML = '';

  const wings = [
    { id: 'ALL', name: 'All Works (96)' },
    { id: 'I',   name: 'Wing I · Fine Arts (12)' },
    { id: 'II',  name: 'Wing II · 3D CGI (27)' },
    { id: 'III', name: 'Wing III · Nocturne (32)' },
    { id: 'IV',  name: 'Wing IV · Kinematic (25)' }
  ];

  let activeWing = 'ALL';

  function renderGrid() {
    grid.innerHTML = '';
    const items = activeWing === 'ALL'
      ? EUNOIA_CONFIG.exhibits
      : EUNOIA_CONFIG.exhibits.filter((e) => e.wing === activeWing);

    items.forEach((ex) => {
      const card = document.createElement('article');
      card.className = 'card';

      const thumb = document.createElement('div');
      thumb.className = 'card-thumb';

      if (ex.mediaType === 'video') {
        const vid = document.createElement('video');
        vid.src = ex.imagePath;
        vid.muted = true;
        vid.loop = true;
        vid.autoplay = true;
        vid.playsInline = true;
        vid.style.width = '100%';
        vid.style.height = '100%';
        vid.style.objectFit = 'cover';
        thumb.appendChild(vid);
        const vBadge = document.createElement('span');
        vBadge.className = 'no';
        vBadge.style.background = '#e6af2e';
        vBadge.style.color = '#001514';
        vBadge.style.fontWeight = '700';
        vBadge.textContent = '▶ 2D ANIMATION';
        thumb.appendChild(vBadge);
      } else {
        const img = document.createElement('img');
        img.src = ex.imagePath;
        img.alt = ex.title;
        img.loading = 'lazy';
        thumb.appendChild(img);
        const no = document.createElement('span');
        no.className = 'no';
        no.textContent = `Wing ${ex.wing}`;
        thumb.appendChild(no);
      }

      thumb.addEventListener('click', () => {
        teleportToExhibit(ex);
      });

      const body = document.createElement('div');
      body.className = 'card-body';
      body.innerHTML = `
        <span class="card-wing">${EUNOIA_CONFIG.wings[ex.wing]?.name || 'Wing ' + ex.wing}</span>
        <h3 class="card-title">${ex.title}</h3>
        <span class="card-meta">${ex.category} · ${ex.year}</span>
        <div class="card-actions">
          <button class="btn btn-gold btn-small btn-teleport">Teleport to Painting</button>
        </div>
      `;

      body.querySelector('.btn-teleport').addEventListener('click', () => {
        teleportToExhibit(ex);
      });

      card.appendChild(thumb);
      card.appendChild(body);
      grid.appendChild(card);
    });
  }

  wings.forEach((w) => {
    const btn = document.createElement('button');
    btn.className = `chip ${w.id === activeWing ? 'active' : ''}`;
    btn.textContent = w.name;
    btn.addEventListener('click', () => {
      activeWing = w.id;
      filtersNav.querySelectorAll('.chip').forEach((c) => c.classList.remove('active'));
      btn.classList.add('active');
      renderGrid();
    });
    filtersNav.appendChild(btn);
  });

  renderGrid();
}

/* --------------------------------------------------------------------------
   4.16  LOBBY & APPLICATION FLOW
   -------------------------------------------------------------------------- */
function initLobbyUI() {
  $('lobbyTitle').textContent = EUNOIA_CONFIG.site.title;
  $('lobbyOverline').textContent = EUNOIA_CONFIG.site.overline;
  $('lobbyTagline').textContent = EUNOIA_CONFIG.site.tagline;
  $('lobbySub').textContent = EUNOIA_CONFIG.site.intro;
  $('hudTitle').textContent = EUNOIA_CONFIG.site.title;

  const linksContainer = $('lobbyLinks');
  linksContainer.innerHTML = '';
  (EUNOIA_CONFIG.links || []).forEach((l) => {
    const a = document.createElement('a');
    a.href = l.url;
    a.target = '_blank';
    a.rel = 'noopener noreferrer';
    a.textContent = l.label;
    linksContainer.appendChild(a);
  });

  // Touch device check
  if ('ontouchstart' in window || navigator.maxTouchPoints > 0) {
    $('touchNote').classList.remove('hidden');
  }

  $('btnEnter').addEventListener('click', enterExhibition);
  $('btnCatalog').addEventListener('click', () => {
    enterExhibition();
    setTimeout(() => toggleCatalog(true), 350);
  });
}

function enterExhibition() {
  initAudio();
  if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume();

  isLobbyActive = false;
  $('lobby').classList.add('out');
  document.body.classList.add('in-gallery');

  // Spawn player in Grand Rotunda facing the central sculpture and north arch
  camera.position.set(0, EYE_HEIGHT, -4.5);
  camera.lookAt(0, EYE_HEIGHT, 4.0);
  camera.rotation.setFromQuaternion(camera.quaternion, 'YXZ');
  if (controls.object) controls.object.position.set(0, EYE_HEIGHT, -4.5);
  velocity.set(0, 0, 0);

  try { controls.lock(); } catch (e) {}
}

function openLobby() {
  isLobbyActive = true;
  document.body.classList.remove('in-gallery');
  $('lobby').classList.remove('out');
  controls.unlock();
}

/* --------------------------------------------------------------------------
   4.17  ANIMATION & RENDER LOOP
   -------------------------------------------------------------------------- */
const clock = new THREE.Clock();
let rotundaOrbitAngle = 0;
let lastRoomCheck = 0;
let frameCount = 0;
let lastFpsTime = performance.now();
const hudFpsEl = $('hudFps');

function updateCurrentWingCaption(pos) {
  const locEl = $('hudLoc');
  const cap = $('roomCaption');
  const capNum = $('capNum');
  const capTitle = $('capTitle');

  let wingName = 'Grand Rotunda';
  let wingNum = 'Entrance';

  if (pos.x > 7.5) {
    wingName = EUNOIA_CONFIG.wings.I.name;
    wingNum = 'Wing I';
  } else if (pos.x < -7.5) {
    wingName = EUNOIA_CONFIG.wings.III.name;
    wingNum = 'Wing III';
  } else if (pos.z > 33.5) {
    wingName = EUNOIA_CONFIG.wings.IV.name;
    wingNum = 'Wing IV';
  } else if (pos.z > 7.5) {
    wingName = EUNOIA_CONFIG.wings.II.name;
    wingNum = 'Wing II';
  }

  locEl.textContent = wingName;
  if (capTitle.textContent !== wingName) {
    capTitle.textContent = wingName;
    capNum.textContent = wingNum;
    cap.classList.add('show');
    clearTimeout(cap._timer);
    cap._timer = setTimeout(() => cap.classList.remove('show'), 3200);
  }
}

function animate() {
  requestAnimationFrame(animate);

  const delta = Math.min(clock.getDelta(), 0.1);

  // 1. Lobby Slow Camera Orbit
  if (isLobbyActive) {
    rotundaOrbitAngle += delta * 0.12;
    const orbR = 4.8;
    camera.position.set(
      Math.sin(rotundaOrbitAngle) * orbR,
      2.5 + Math.sin(rotundaOrbitAngle * 0.5) * 0.3,
      Math.cos(rotundaOrbitAngle) * orbR
    );
    camera.lookAt(0, 1.8, 0);
    renderer.render(scene, camera);
    return;
  }

  // 2. Camera Interpolation for Inspection
  if (inspectLerp) {
    inspectLerp.t += delta / inspectLerp.duration;
    const progress = clamp(inspectLerp.t, 0, 1);
    const ease = easeInOutCubic(progress);

    camera.position.lerpVectors(inspectLerp.startPos, inspectLerp.endPos, ease);
    camera.quaternion.slerpQuaternions(inspectLerp.startQuat, inspectLerp.endQuat, ease);

    if (progress >= 1) {
      camera.rotation.setFromQuaternion(camera.quaternion, 'YXZ');
      if (inspectLerp.onComplete) inspectLerp.onComplete();
      inspectLerp = null;
    }
    renderer.render(scene, camera);
    return;
  }

  // 3. First-Person Physics & Movement
  if (isControlsLocked) {
    const moveSpeed = moveState.sprint ? 5.8 : 3.4;
    const damping = 9.0;

    velocity.x -= velocity.x * damping * delta;
    velocity.z -= velocity.z * damping * delta;

    direction.z = Number(moveState.forward) - Number(moveState.backward);
    direction.x = Number(moveState.right) - Number(moveState.left);
    direction.normalize();

    if (moveState.forward || moveState.backward) {
      velocity.z -= direction.z * moveSpeed * 8.0 * delta;
    }
    if (moveState.left || moveState.right) {
      velocity.x += direction.x * moveSpeed * 8.0 * delta;
    }

    controls.moveRight(velocity.x * delta);
    controls.moveForward(-velocity.z * delta);

    // Collision detection & sliding
    const playerPos = camera.position;
    resolveCollision(playerPos);

    // Head-bobbing & Footstep audio trigger
    const speed = Math.hypot(velocity.x, velocity.z);
    if (speed > 0.4) {
      bobTimer += delta * (moveState.sprint ? 14 : 9.5);
      const bobY = Math.sin(bobTimer) * 0.045;
      camera.position.y = EYE_HEIGHT + bobY;

      if (Math.sin(bobTimer) < -0.85 && lastFootstepBob >= -0.85) {
        playFootstep();
      }
      lastFootstepBob = Math.sin(bobTimer);
    } else {
      camera.position.y = lerp(camera.position.y, EYE_HEIGHT, delta * 6);
      bobTimer = 0;
    }

    // Room caption update periodically
    lastRoomCheck += delta;
    if (lastRoomCheck > 0.4) {
      lastRoomCheck = 0;
      updateCurrentWingCaption(camera.position);
    }
  }

  // 4. Raycasting
  updateRaycast();

  // 5. Render Scene
  renderer.render(scene, camera);

  // 6. FPS Counter
  frameCount++;
  const now = performance.now();
  if (now - lastFpsTime >= 500) {
    const fps = Math.round((frameCount * 1000) / (now - lastFpsTime));
    if (hudFpsEl) hudFpsEl.textContent = `${fps} FPS`;
    frameCount = 0;
    lastFpsTime = now;
  }
}

/* --------------------------------------------------------------------------
   4.18  RESIZE HANDLER & BOOTSTRAP
   -------------------------------------------------------------------------- */
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.75));
});

// Re-draw text textures once web fonts load to guarantee pristine typography
if (document.fonts) {
  document.fonts.ready.then(() => {
    textTextures.forEach(({ ctx, w, h, draw, t }) => {
      ctx.clearRect(0, 0, w, h);
      draw(ctx, w, h);
      t.needsUpdate = true;
    });
  });
}

// Bootstrap entire museum
buildArchitecture();
layoutExhibits();
buildLighting();
initCatalog();
initLobbyUI();
updateLoadStatus();

// Expose public API for inspection and testing
window.EUNOIA_CONFIG = EUNOIA_CONFIG;
window.teleportToExhibit = teleportToExhibit;
window.enterExhibition = enterExhibition;
window.exitInspection = exitInspection;
window.camera = camera;
window.controls = controls;
window.scene = scene;
window.exhibitMeshes = exhibitMeshes;
window.loadTracker = loadTracker;
window.THREE = THREE;

animate();
  