# Phase 2 Starting Kit

This directory contains the Phase 2 starting kit. In this phase, you need to protect a set of video clips of a single identity. The threat scenario covers both *reference-based* and *tuning-based* customization.

In the *reference-based* setting, an attacker samples a random frame from video clips and uses it as the reference input to an image-to-video (I2V) model. In the *tuning-based* setting, the attacker fine-tunes a text-to-video (T2V) model on the entire video set and then generates new videos.

**Data**: Phase 2 uses face-centric video clips, 640×480, 113 frames, 1 identity, 10 clips.

**Evaluation Tracks**: In this phase, each submission is evaluated under three tracks in both the reference-based and tuning-based customization settings:
- **Effectiveness**: the protected video set is evaluated as-is using the known evaluation model (Wan2.2-TI2V-5B).
- **Robustness**: the protected video set is first processed by a temporal attack before evaluation.
- **Transferability**: the protected video set is evaluated using additional hidden video generation models.

**Models**: 
- Phase 2 uses [Wan2.2-TI2V-5B](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B-Diffusers) as the known evaluation model for measuring protection effectiveness in both the reference-based and tuning-based customization settings.
- In this starting kit, [CogVideoX1.5-5B-I2V](https://huggingface.co/zai-org/CogVideoX1.5-5B-I2V) is provided as an example model for evaluating transferability in the reference-based I2V setting. Please note that the official competition evaluation may use different hidden models and will assess transferability in both the reference-based and fine-tuning-based settings.

**Perturbation Budget**: 16/255

## Table of Contents

- [Environment](#environment)
- [Hardware](#hardware)
- [Repository Structure](#repository-structure)
- [Data Preparation](#data-preparation)
- [How to Implement and Run a Protection Method](#how-to-implement-and-run-a-protection-method)
- [How to Evaluate](#how-to-evaluate)
- [Submission](#submission)

## Environment

Clone the repo:

```bash
git clone https://github.com/tmllab/ECCV26_LifeGenIP_starting_kit.git
cd ECCV26_LifeGenIP_starting_kit
git submodule update --init --recursive
cd phase2
```

Set up the environment:

```bash
conda create -n lifegenip python=3.10 -y
conda activate lifegenip

conda install -c conda-forge ffmpeg -y
conda install -c nvidia cudnn=8 -y

pip install --no-cache-dir torch==2.9.1 torchvision==0.24.1 torchaudio==2.9.1 --index-url https://download.pytorch.org/whl/cu128
pip install -r requirements.txt
pip uninstall -y onnxruntime && pip install onnxruntime-gpu==1.17.1
```

Download the I2V model (~32 GB) and set `WAN_MODEL_PATH`:

```bash
huggingface-cli download Wan-AI/Wan2.2-TI2V-5B-Diffusers \
    --local-dir ./models/Wan2.2-TI2V-5B-Diffusers
export WAN_MODEL_PATH=$PWD/models/Wan2.2-TI2V-5B-Diffusers
```

Download the CogVideoX I2V model (~29 GB) and set `COGVIDEOX_I2V_MODEL_PATH`:

```bash
huggingface-cli download zai-org/CogVideoX1.5-5B-I2V \
    --local-dir ./models/CogVideoX1.5-5B-I2V
export COGVIDEOX_I2V_MODEL_PATH=$PWD/models/CogVideoX1.5-5B-I2V
```

## Hardware

A single NVIDIA GPU with ≥ 24 GB VRAM is recommended, e.g., RTX 3090, RTX 4090, A5000, or A6000. Tested on RTX 4090.

## Repository Structure

```
data_preparation/                       # preprocess raw MEAD dataset
protect/
├── run.py                              # entry point
└── methods/
    ├── random_noise.py                 # baseline: uniform L-inf noise
    └── my_method.py                    # your method
eval/                                   # evaluation
utils/
check_submission.py                     # validate submission.zip before upload
data/
├── original/                           # raw data
├── preprocessed/                       # preprocessed video clips
├── protected/<method>/                 # protected video clips
│   ├── submission/                     # lossless, for submission
│   └── preview/                        # lossy, for viewing
├── attacked/<method>/                  # protected clips after temporal attacks
└── generated/<method>/                 # videos generated during evaluation
third_party/                            # external tools used for fine-tuning
```

## Data Preparation

### Download

Follow the download instructions in the [MEAD GitHub repo](https://github.com/uniBruce/Mead). The full dataset is very large (over 400 GB), so you do **not** need all of it. Phase 2 uses a single identity, so in the dataset's [Google Drive](https://github.com/uniBruce/Mead/issues/21#issuecomment-1200418970) or [Baidu Netdisk](https://github.com/uniBruce/Mead/issues/8#issuecomment-966988461) link, open the `M003` folder and download only `video.tar` from it.

> If you run into any download issues, please contact us.

### Prepare the video clips

1. Put the `video.tar` under `data/original/`:

   ```bash
   mkdir -p data/original # place video.tar at: data/original/video.tar
   ```

   > There is no need to untar `video.tar`. `preprocess.py` extracts only the required video clips automatically.

2. Verify the `video.tar` before preprocessing:

   ```bash
   python data_preparation/check.py
   ```

3. Extract and preprocess the video clips:

   ```bash
   python data_preparation/preprocess.py
   ```

   > The required raw video clips are extracted from `video.tar` automatically, saved under `data/original/<id>/`. Preprocessed video clips are written to `data/preprocessed/<id>/<vid>.mp4`.

## How to Implement and Run a Protection Method

### Run a baseline

The kit currently provides one baseline `random_noise`: uniform L∞ noise applied to every frame within the budget.

```bash
python protect/run.py --method random_noise
```

> ⚠️ Two folders are written under `data/protected/<method>/`: `submission/<id>/<vid>.mp4` (lossless) and `preview/<id>/<vid>.mp4` (lossy). The lossless mp4 is pixel-exact, but some players show it with wrong colors, so view the protected video by the `preview/` and submit the `submission/`.

### Implement your own

Edit `protect/methods/my_method.py` and implement the `protect` function, then run `python protect/run.py --method my_method`.

**Constraint.** Each protected video clip must satisfy `L∞ ≤ 16/255` against its original. Over-budget pixels are clipped to the budget before evaluation.

## How to Evaluate

We provide a local evaluation program, which is a public reference implementation for participants to estimate methods locally. It does **not** reproduce the final leaderboard evaluation.


### Run Local Evaluation

```bash
python eval/run.py --method <method_name>
```

> By default, local evaluation runs I2V effectiveness, robustness, and transferability, as well as fine-tuning effectiveness and robustness. A full run takes about **4 hours on a single RTX 4090**. Generated videos are saved to `data/generated/<method>/`, and the reference metric values are saved to `data/results/<method>/results.json`.

> To customize which settings to run, please edit `eval/config.yaml`. Fine-tuning-specific options are in `eval/finetune/models/WAN2.2_5B/config.yaml`. 

For I2V evaluation, the evaluation program samples a frame from protected video clips and feeds it into the I2V pipeline. For fine-tuning evaluation, the evaluation program uses the protected video set to fine-tune the T2V model and then generates videos. The **protected videos** and the **generated videos** are then evaluated using the metrics below.

### Metrics


| Type     | Used For                      | Evaluated On                       | What it measures                                                       | Notes                                                                |
| --------------- | -------------------------- | ---------------------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `face_detection`          | Effectiveness + Robustness + Transferability | Generated videos                   | Face-detection failure rate (FDFR) over generated frames                      | Higher values mean better protection, indicating fewer detectable faces in the generated video. |
| `face_similarity`           | Effectiveness + Robustness + Transferability | Generated videos                   | Identity similarity (ISM) between the generated face and the target identity | Lower values mean better protection. This metric is computed only on frames where a face is detected.    |
| `prompt_following` | Effectiveness + Robustness + Transferability | Generated videos                   | Video-text alignment between the generated video and the text prompt   | Lower values mean better protection, indicating weaker prompt following. |
| `image_quality` | Effectiveness + Robustness + Transferability | Generated videos                   | Visual quality of the generated video                                  | Lower quality means better protection, indicating lower visual quality in the generated video.   |
| `invisibility`  | Invisibility only          | Protected video | Imperceptibility of the protected video compared to the original     | Better invisibility means better imperceptibility. Computed once on the protected video, not on generated videos.   |

> ⚠️ Local metric values are for reference only and may not match the final leaderboard results.

Note that the `invisibility` metric is computed directly between the **protected video** clip and the **original video** clip, while all other metrics are computed based on the **generated videos**.

The final leaderboard follows the same metric types of the local evaluation program, but uses hidden text prompts, a hidden reference-frame sampling strategy, hidden face detectors and encoders (for `face_detection` and `face_similarity`), hidden vision-language models (for `prompt_following`), hidden image-quality models, and hidden temporal attacks. 

Specifically, the local evaluation program provides one public reference temporal attack for robustness evaluation. The final leaderboard evaluates robustness under **three hidden temporal attacks**.


## Submission

Build the archive from your protected output:

```bash
cd data/protected/<your_method>/submission
python -m zipfile -c ../../../../submission.zip M003
```

Before uploading, run the checker. It verifies `submission.zip` structure and every video clip uses the required lossless encoding:

```bash
cd ../../../..
python check_submission.py
```

Submissions that fail this check (wrong structure or encoding) may be rejected, to avoid evaluation issues. 

To submit, register and join our [Codabench competition](https://www.codabench.org/competitions/16817/), then upload `submission.zip` from the **My Submissions** tab.
