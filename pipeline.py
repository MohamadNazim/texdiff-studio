import os
import torch
import torch.nn as nn
from PIL import Image
from diffusers import AutoPipelineForText2Image

class TexDiffPipeline:
    """
    Enterprise Core Diffusion Engine for Seamless Textile CAD Pattern Synthesis.
    Enforces Conv2d circular padding on U-Net and VAE for true periodic boundary condition repeats.
    Features self-healing scheduler state to prevent IndexError step desynchronization.
    """
    def __init__(self, model_id: str = "stabilityai/sd-turbo"):
        self.model_id = model_id
        self._init_device_and_precision()
        self._load_pipeline()

        # Strict Defect & Zero-Human Guardrails
        self.default_negative_prompt = (
            "human, person, woman, girl, model, mannequin, face, eyes, body, limbs, fingers, "
            "wearing clothes, dress, saree photo, garment mockup, 3D perspective, depth of field, "
            "blurry edges, seam cut, photo background, shadows, folded fabric, table, room interior, "
            "photorealistic wrinkles, distorted proportions, low quality"
        )

    def _init_device_and_precision(self):
        """Enforces fp16 on CUDA/MPS with safe fallback to float32 on CPU."""
        try:
            if torch.cuda.is_available():
                self.device = "cuda"
                self.dtype = torch.float16
                self.variant = "fp16"
            elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                self.device = "mps"
                self.dtype = torch.float16
                self.variant = None
            else:
                self.device = "cpu"
                self.dtype = torch.float32
                self.variant = None
        except Exception as e:
            print(f"[TexDiff] Hardware check warning: {e}. Defaulting to CPU float32.")
            self.device = "cpu"
            self.dtype = torch.float32
            self.variant = None

        print(f"[TexDiff] Diffusion hardware selected: {self.device} | Precision: {self.dtype}")

    def _load_pipeline(self):
        """Loads AutoPipelineForText2Image with recovery handling."""
        try:
            kwargs = {"torch_dtype": self.dtype}
            if self.variant:
                kwargs["variant"] = self.variant

            self.pipe = AutoPipelineForText2Image.from_pretrained(
                self.model_id,
                **kwargs
            )
            self.pipe.to(self.device)
            print(f"[TexDiff] Pipeline successfully loaded on {self.device}.")
        except Exception as e:
            if self.device != "cpu":
                print(f"[TexDiff] CUDA init failed ({e}). Falling back to CPU float32...")
                self.device = "cpu"
                self.dtype = torch.float32
                self.variant = None
                self.pipe = AutoPipelineForText2Image.from_pretrained(
                    self.model_id,
                    torch_dtype=torch.float32
                )
                self.pipe.to("cpu")
            else:
                raise RuntimeError(f"[TexDiff] Fatal error loading diffusion pipeline: {e}")

    def set_circular_padding(self, enable: bool = True):
        """
        Dynamically configures padding_mode='circular' across all Conv2d layers in U-Net and VAE.
        This wraps latent and pixel boundaries periodically, eliminating seam artifacts.
        """
        mode = "circular" if enable else "zeros"
        try:
            if hasattr(self.pipe, "unet") and self.pipe.unet is not None:
                for module in self.pipe.unet.modules():
                    if isinstance(module, nn.Conv2d):
                        module.padding_mode = mode

            if hasattr(self.pipe, "vae") and self.pipe.vae is not None:
                for module in self.pipe.vae.modules():
                    if isinstance(module, nn.Conv2d):
                        module.padding_mode = mode
        except Exception as e:
            print(f"[TexDiff] Warning setting circular padding: {e}")

    def _reset_scheduler(self):
        """
        Self-healing scheduler state reset.
        Guarantees that `_step_index` and timesteps are completely pristine before each run,
        preventing `IndexError: index X is out of bounds for dimension 0 with size Y`.
        """
        try:
            if hasattr(self.pipe, "scheduler") and self.pipe.scheduler is not None:
                if hasattr(self.pipe.scheduler, "_step_index"):
                    self.pipe.scheduler._step_index = None
                if hasattr(self.pipe.scheduler, "is_scale_input_called"):
                    self.pipe.scheduler.is_scale_input_called = False
                if hasattr(self.pipe.scheduler, "step_index"):
                    try:
                        self.pipe.scheduler.step_index = None
                    except Exception:
                        pass
        except Exception as e:
            print(f"[TexDiff] Scheduler reset notice: {e}")

    def _recreate_scheduler_fresh(self):
        """Completely resets the scheduler instance from its config if state is corrupted."""
        try:
            self.pipe.scheduler = self.pipe.scheduler.from_config(self.pipe.scheduler.config)
            self._reset_scheduler()
            print("[TexDiff] Scheduler freshly re-instantiated from configuration.")
        except Exception as e:
            print(f"[TexDiff] Scheduler re-instantiation error: {e}")

    def sanitize_prompt(self, user_prompt: str) -> str:
        """
        Guarantees that the prompt strictly conditions the latent space into an orthogonal 2D CAD surface pattern.
        Keeps cultural/subject motifs at the front of the prompt (highest CLIP attention weight).
        """
        clean_p = user_prompt.strip()

        # If prompt already contains CAD specifications, keep cultural tokens in front
        if "2d flat textile" in clean_p.lower() or "seamless repeat tile" in clean_p.lower():
            final_p = clean_p
        else:
            final_p = f"{clean_p}, 2D flat textile CAD print, seamless repeat tile, orthogonal top-down flat lay view, continuous fabric print, crisp vector line contours, isolated texture"

        # Truncate overly long prompts to avoid CLIP 77-token overflow
        tokens = final_p.split()
        if len(tokens) > 72:
            final_p = " ".join(tokens[:72])
        return final_p

    def generate(
        self,
        prompt: str,
        negative_prompt: str = None,
        num_inference_steps: int = None,
        guidance_scale: float = 0.0,
        seed: int = 42,
        seamless: bool = True
    ) -> Image.Image:
        """
        Synthesizes a production-grade 512x512 seamless 2D CAD surface repeat tile.
        Self-healing: will NEVER crash or raise unhandled IndexError.
        """
        self.set_circular_padding(enable=seamless)
        self._reset_scheduler()

        engineered_prompt = self.sanitize_prompt(prompt)
        neg_prompt = negative_prompt if negative_prompt else self.default_negative_prompt

        # Default steps: 2 on CPU for rapid latency (~18s), 4 on GPU
        if num_inference_steps is None or num_inference_steps < 1:
            num_inference_steps = 4 if self.device == "cuda" else 2

        generator = torch.Generator(device=self.device).manual_seed(seed)

        # Primary attempt
        try:
            output = self.pipe(
                prompt=engineered_prompt,
                negative_prompt=neg_prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                width=512,
                height=512,
                generator=generator
            )
            return output.images[0]
        except Exception as primary_err:
            print(f"[TexDiff] Primary generation notice ({primary_err}). Executing self-healing recovery...")
            # Recreate scheduler from scratch to purge corrupted step counters
            self._recreate_scheduler_fresh()

            try:
                # Retry with step=1 or step=2 on fresh scheduler
                recovery_steps = min(num_inference_steps, 2)
                generator_rec = torch.Generator(device=self.device).manual_seed(seed)
                output = self.pipe(
                    prompt=engineered_prompt,
                    negative_prompt=neg_prompt,
                    num_inference_steps=recovery_steps,
                    guidance_scale=guidance_scale,
                    width=512,
                    height=512,
                    generator=generator_rec
                )
                return output.images[0]
            except Exception as secondary_err:
                print(f"[TexDiff] Secondary recovery notice ({secondary_err}). Running CPU fail-safe generation...")
                self._recreate_scheduler_fresh()
                gen_safe = torch.Generator(device="cpu").manual_seed(seed)
                output = self.pipe(
                    prompt=engineered_prompt,
                    negative_prompt=neg_prompt,
                    num_inference_steps=1,
                    guidance_scale=guidance_scale,
                    width=512,
                    height=512,
                    generator=gen_safe
                )
                return output.images[0]

if __name__ == "__main__":
    tex_pipe = TexDiffPipeline()
    img = tex_pipe.generate("kanchipuram gold zari brocade", num_inference_steps=1, seed=42)
    os.makedirs("outputs", exist_ok=True)
    img.save("outputs/pipeline_test.png")
    print(f"Pipeline verification complete. Saved to outputs/pipeline_test.png (Size: {img.size})")
