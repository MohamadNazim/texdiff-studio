import os
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from vector_store import TextileMotifStore

class TexDiffEvaluator:
    def __init__(self, clip_model_id: str = "openai/clip-vit-base-patch32"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = CLIPModel.from_pretrained(clip_model_id).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(clip_model_id)
        self.motif_store = TextileMotifStore()

    def evaluate_retrieval(self):
        tests = [
            ("hand printed lotus vines madder red", "Andhra Kalamkari"),
            ("kanchipuram gold zari border temple rekku", "Kanchipuram Zari Brocade"),
            ("madurai sungudi tie dye ring dots", "Madurai Sungudi")
        ]
        hits = 0
        for q, expected in tests:
            res = self.motif_store.auto_expand_prompt(q)
            if res["matched_style"].lower() == expected.lower():
                hits += 1
        return hits / len(tests)

if __name__ == "__main__":
    evaluator = TexDiffEvaluator()
    acc = evaluator.evaluate_retrieval()
    print(f"[Benchmark] Retrieval Accuracy: {acc * 100:.1f}%")
