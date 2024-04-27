import os
import random

import numpy as np
import soundfile as sf
import torch

from .pipeline import build_model, super_resolution

torch.set_float32_matmul_precision("high")

class Predictor:
    def setup(self, model_name="basic", device="auto"):
        self.model_name = model_name
        self.device = device
        self.audiosr = build_model(model_name=self.model_name, device=self.device)

    def predict(self,
        input_file="example/music.wav",
        sr=48000,
        ddim_steps=50,
        guidance_scale=3.5,
        seed=None
    ):
        """Run a single prediction on the model"""
        if seed is None:
            seed = random.randint(0, 2**32 - 1)
            print(f"Setting seed to: {seed}")

        waveform = super_resolution(
            self.audiosr,
            input_file,
            seed=seed,
            guidance_scale=guidance_scale,
            ddim_steps=ddim_steps,
            latent_t_per_second=12.8
        )
        out_wav = (waveform[0] * 32767).astype(np.int16).T
        out_path = os.path.join(os.path.dirname(input_file), f"{os.path.splitext(os.path.basename(input_file))[0]}" + "_output.wav")
        sf.write(out_path, data=out_wav, samplerate=sr)

def start_predict(input_file, sr=48000, ddim_steps=50, guidance_scale=3.5, model_name="basic", device="auto", seed=None):
    p = Predictor()
    p.setup(model_name, device)
    out = p.predict(
        input_file,
        sr=sr,
        ddim_steps=ddim_steps,
        guidance_scale=guidance_scale,
        seed=seed
    )