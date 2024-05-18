import os
import random

import numpy as np
import soundfile as sf
import torch
import shutil

from .pipeline import build_model, super_resolution
from .utils import read_audio_file_duration
from .utilities.audio.split_audio import process_audio, merge_audio

torch.set_float32_matmul_precision("high")

class Predictor:
    def setup(self, model_name="basic", device="auto"):
        self.model_name = model_name
        self.device = device
        self.audiosr = build_model(model_name=self.model_name, device=self.device)

    def predict(self,
        input_file="example/music.wav",
        output_file=None,
        sr=48000,
        ddim_steps=50,
        guidance_scale=3.5,
        seed=None
    ):
        """Run a single prediction on the model"""
        if seed is None:
            seed = random.randint(0, 2**32 - 1)
            print(f"Setting seed to: {seed}")
        if read_audio_file_duration(input_file) > 5:
            result, new_dir_path = process_audio(input_file)
            if result == "Error":
                return "Error with Split Audio", None
            dir_path = (
                new_dir_path.strip(" ").strip('"').strip("\n").strip('"').strip(" ")
            )
            if dir_path != "":
                paths = [
                    os.path.join(root, name)
                    for root, _, files in os.walk(dir_path, topdown=False)
                    for name in files
                    if name.endswith(".wav") and root == dir_path
                ]
            try:
                for path in paths:
                    waveform = super_resolution(
                        self.audiosr,
                        path,
                        seed=seed,
                        guidance_scale=guidance_scale,
                        ddim_steps=ddim_steps,
                        latent_t_per_second=12.8
                    )
                    out_wav = (waveform[0] * 32767).astype(np.int16).T
                    sf.write(path, data=out_wav, samplerate=sr)
            except Exception as error:
                print(error)
                return f"Error {error}"
            print("Finished processing segmented audio, now merging audio...")
            merge_timestamps_file = os.path.join(
                os.path.dirname(new_dir_path),
                f"{os.path.basename(input_file).split('.')[0]}_timestamps.txt",
            )
            tgt_sr, audio_opt = merge_audio(merge_timestamps_file)
            os.remove(merge_timestamps_file)
            if not output_file:
                output_file = os.path.join(os.path.dirname(input_file), f"{os.path.splitext(os.path.basename(input_file))[0]}" + "_output.wav")
            sf.write(output_file, audio_opt, tgt_sr, format="WAV")
            shutil.rmtree(new_dir_path)
        else:
            waveform = super_resolution(
                self.audiosr,
                input_file,
                seed=seed,
                guidance_scale=guidance_scale,
                ddim_steps=ddim_steps,
                latent_t_per_second=12.8
            )
            out_wav = (waveform[0] * 32767).astype(np.int16).T
            if not output_file:
                output_file = os.path.join(os.path.dirname(input_file), f"{os.path.splitext(os.path.basename(input_file))[0]}" + "_output.wav")
            sf.write(output_file, data=out_wav, samplerate=sr)

def upscale(input_file, output_file=None, sr=48000, ddim_steps=50, guidance_scale=3.5, model_name="basic", device="auto", seed=None):
    p = Predictor()
    p.setup(model_name, device)
    p.predict(
        input_file,
        output_file,
        sr=sr,
        ddim_steps=ddim_steps,
        guidance_scale=guidance_scale,
        seed=seed
    )