import pipeline
import torch
from PIL import Image

pipe = pipeline.TexDiffPipeline()
prompt = "2D flat CAD textile print, seamless repeat tile, emerald green and metallic gold zari floral jaal with sacred peacock buta motifs for royal banarasi silk saree, intricate brocade weave, orthogonal top-down flat lay view, continuous surface pattern, crisp vector line contours, production textile swatch"
neg = "human, person, model, dress, saree photo, 3D perspective, blurry edges, folded fabric, mannequin, face, shadows, realistic person, photorealistic body, garment mockup, limbs, wrinkles, cloth folds"

print("Generating test tile for: emerald green and gold banarasi...")
img = pipe.generate(
    prompt=prompt,
    negative_prompt=neg,
    num_inference_steps=2,
    guidance_scale=0.0,
    seed=12345,
    seamless=True
)

img.save("outputs/test_green_gold_banarasi.png")
print("Saved outputs/test_green_gold_banarasi.png successfully!")
