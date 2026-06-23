# Image generation prompts

## Master reference

Use case: stylized-concept
Asset type: Windows desktop-pet master character reference
Input image: `D:\Desktop\Osaka\osaka.png` is the primary identity reference for Ayumu Kasuga / Osaka.
Primary request: Create a faithful chibi desktop-pet version of Osaka for local personal use. Preserve her recognizable black-brown straight hair, soft vacant delayed-reaction gaze, tiny mouth, simple red-brown and light school-uniform color feeling, harmless sincerity, and natural slow half-beat personality.
Style: 2.5D soft vinyl figure, 2.1–2.3 heads tall, large round head, small soft body, short rounded arms, bun-like feet, smooth forms, clean silhouette, soft ambient occlusion.
Pose: neutral full-body standing idle pose, front three-quarter view, arms relaxed, vacant forward gaze, tiny neutral mouth.
Backdrop: perfectly flat solid #00FF00 chroma-key background with no shadow, gradient, texture, floor, reflection, or lighting variation.
Constraints: same Osaka identity as the input; generous padding; no #00FF00 on the character; no cast shadow; no contact shadow; no text; no watermark; no logo; no extra character.
Avoid: realism, detailed hair strands, glamorous anime illustration, sharp clever expression, hyperactivity, battle pose, accessories, animal ears, weapons, background scenery.

## State key poses

Every state prompt must repeat the master invariants above and use both `osaka.png` and `reference\osaka_pet_master.png` as identity references. Change only the required pose, face, and permitted small prop. Preserve hairstyle, face placement, outfit, proportions, palette, material, camera, scale, and line quality exactly.

- idle: vacant standing pose, tiny delayed blink and slight head tilt.
- happy: first confused pause, then hands at chest and two soft toy-like hops.
- shy: slight shrink, lowered head, faint blush, awkward tiny nod.
- cry: small blue tears, tiny downturned/w mouth, restrained sobbing.
- surprised: small upward pop, round eyes, tiny o mouth, confused pause.
- clicked: frozen stare, slowly raised short hand, tiny nonverbal question bubble.
- drag: arms raised, legs dangling, soft sway, confused but not frightened. The generated external hand lifting the character is explicitly accepted by the user for this state.
- sleep: curled side-lying pose, closed eyes, small zzz.
- study: seated reading a tiny notebook, slow nod, page turn, brief daydream.
- thinking: head tilt, vacant gaze, tiny question mark or cloud.
- eating: hold a small rice ball, observe it, slow bites, satisfied sway.
